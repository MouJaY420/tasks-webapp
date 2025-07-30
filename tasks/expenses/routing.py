from django.urls import re_path
from expenses.consumers import ReceiptConsumer

websocket_urlpatterns = [
    re_path(r'ws/receipt/(?P<household_id>\d+)/$', ReceiptConsumer.as_asgi()),
]
