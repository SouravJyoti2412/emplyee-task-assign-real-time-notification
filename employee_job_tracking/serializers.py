from rest_framework import serializers
from .models import Task , CustomUser, Message

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password']  # 👈 This excludes the password field


class MessegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'