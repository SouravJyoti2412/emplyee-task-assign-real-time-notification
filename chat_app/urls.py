from django.contrib import admin
from django.urls import path , include

from chat_app.views.render_page import index , login , register,chat
from chat_app.views.google_login import  google_login, google_login_new
urlpatterns = [
    path('index/',index ),
    path('login/',login ),
    path('login-google/',google_login),
    path('login-by-google/', google_login_new),
    path('register/', register),
    path('chat/<int:receiver_id>/', chat, name='chat')


]