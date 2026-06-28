from django.conf import settings
from django.conf.urls.static import static
from app.urls import *

from django.contrib import admin
from django.urls import path , include
from employee_job_tracking.views.render_views import notification , notification2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('employee_job_tracking.urls')),
	path('chat/', include('chat_app.urls')),
    path('notification/', notification, name='notification'),
    path('notification2/', notification2, name='notification2'),
	# path('accounts/', include('allauth.urls')),

]
if settings.DEBUG:
	urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
	urlpatterns = urlpatterns + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
