from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/admin-customer/$', consumers.AdminCustomerConsumer.as_asgi()),
    re_path(r'ws/admin-jobs/$', consumers.AdminJobConsumer.as_asgi()),
]