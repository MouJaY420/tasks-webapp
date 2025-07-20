from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/receipt/(?P<household_id>\d+)/$', consumers.ReceiptConsumer.as_asgi()),
]
