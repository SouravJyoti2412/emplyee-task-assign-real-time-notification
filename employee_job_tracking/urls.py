from django.contrib import admin
from django.urls import path , include
from employee_job_tracking.views.user_signup_login import UserSignupLoginAPIView
from employee_job_tracking.views.task_views import TaskAPIView

urlpatterns = [
    path('task/',TaskAPIView.as_view()),
    path('user/', UserSignupLoginAPIView.as_view()),
]
