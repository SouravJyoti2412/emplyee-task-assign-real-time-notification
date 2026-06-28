from django.urls import re_path
from employee_job_tracking import consumers

websocket_urlpatterns = [
    re_path(r'ws/admin-customer/$', consumers.AdminCustomerConsumer.as_asgi()),
    re_path(r'ws/admin-jobs/$', consumers.AdminJobConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
]