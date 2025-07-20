from django.db.models.functions import TruncMonth
from django.db.models import Sum
import json
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SharedExpenseForm
from .models import Expense
from main.models import Household
from django.http import HttpResponse
import qrcode
from io import BytesIO
from .utils import get_local_ip
from django.urls import reverse
import pytesseract
from PIL import Image
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@login_required
def household_expenses(request, pk):
    household = get_object_or_404(Household, pk=pk)
    if request.user.household_id != household.pk:
        return redirect('main:household_landing')

    shared = household.shared_expenses.select_related('user').all()

    edit_pk = request.GET.get('edit')
    edit_form = None
    if edit_pk:
        exp_to_edit = get_object_or_404(Expense, pk=edit_pk, household=household)
        # If it’s a GET, show the form; if POST, we’ll handle below
        if request.method == 'GET':
            edit_form = SharedExpenseForm(instance=exp_to_edit)

    if request.method == 'POST':
        # Delete
        if 'delete_expense' in request.POST:
            Expense.objects.filter(pk=request.POST['delete_expense'], household=household).delete()
            return redirect('expenses:household_expenses', pk=pk)

        # Edit
        if 'edit_expense' in request.POST:
            exp = get_object_or_404(Expense, pk=request.POST['edit_expense'], household=household)
            form = SharedExpenseForm(request.POST, instance=exp)
            if form.is_valid():
                form.save()
                return redirect('expenses:household_expenses', pk=pk)
            edit_form = form  # re-render with errors

        # Create
        else:
            form = SharedExpenseForm(request.POST)
            if form.is_valid():
                new = form.save(commit=False)
                new.user = request.user
                new.household = household
                new.save()
                return redirect('expenses:household_expenses', pk=pk)
    else:
        form = SharedExpenseForm(initial={'date': date.today()})

    qs = (
        shared
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('converted_amount'))
        .order_by('month')
    )
    labels = [entry['month'].strftime("%b %Y") for entry in qs]
    data   = [float(entry['total'])             for entry in qs]

    # Add to context
    context = {
        'household': household,
        'shared_expenses': shared,
        'form': form,
        'edit_pk': edit_pk,
        'edit_form': edit_form,
        'chart_labels_json': json.dumps(labels),
        'chart_data_json':   json.dumps(data),
    }
    return render(request, 'expenses/household_expenses.html', context)

def qr_code_view(request):
    ip = get_local_ip()         # Gets LAN IP like 192.168.1.114
    port = request.get_port()   # Typically 8000
    upload_url = reverse('expenses:upload_receipt')
    full_url = f"http://{ip}:{port}{upload_url}"

    # Generate the QR code
    img = qrcode.make(full_url)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return HttpResponse(buffer.read(), content_type="image/png")

def upload_receipt(request):
    if request.method == 'POST' and request.FILES.get('receipt_image'):
        image_file = request.FILES['receipt_image']
        img = Image.open(image_file)
        text = pytesseract.image_to_string(img)
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"receipt_{request.user.household.pk}",
            {
            "type": "receipt_uploaded",
            "text": json.dumps({"status": "uploaded"})
            }
        )

        household = getattr(request.user, 'household', None)
        return render(request, 'expenses/receipt_ocr_preview.html', {
            'extracted_text': text,
            'household': household,
        })

    # If user visits this via QR or mobile browser
    return render(request, 'expenses/receipt_upload_form.html')