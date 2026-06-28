from django.contrib import admin
from django.urls import path , include
from employee_job_tracking.views.user_signup_login import UserSignupAPIView , UserLoginAPIView , LoginRedirectionApi
from employee_job_tracking.views.task_views import TaskAPIView
from employee_job_tracking.views.chat_view import ChatView ,ChatList  , SearchUserList
urlpatterns = [ 
    path('task/',TaskAPIView.as_view()),
    path('user/', UserSignupAPIView.as_view()),
    path('user-login/', UserLoginAPIView.as_view()),
    path('login-redirection/',LoginRedirectionApi.as_view() ),
    path('user-messege/', ChatView.as_view()),
    path('chat-list/', ChatList.as_view()),
    path('search-user-list/', SearchUserList.as_view())
]
