from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from employee_job_tracking.models import Task , CustomUser
from employee_job_tracking.serializers import MessegeSerializer , CustomUserSerializer
from celery import shared_task
from employee_job_tracking.models import Message
from django.db.models import Q
from app.helper import user_validation

from rest_framework.permissions import AllowAny


class ChatView(APIView):
    authentication_classes = []      # <‑‑ skip auth checks
    permission_classes     = [AllowAny]
    def post(self, request , *args, **kwargs):
        # sender = request.data.get("sender_id")
        token = request.headers.get('Authorization')
        token = token.split()[1]
        user_json = user_validation(token)
        if user_json["message"] == "User present":   
            user = user_json["user_obj"]
        sender = user.id
        reciver = request.data.get("reciver_id")
        all_masseges_obj = Message.objects.filter( Q(sender=sender, receiver=reciver) |Q(sender=reciver, receiver=sender)).order_by('-timestamp')[:50]
        all_masseges_json =  MessegeSerializer(all_masseges_obj, many=True)     
        return Response({"message": "User all massege.", "massege" :all_masseges_json.data, "sender":sender } , status=status.HTTP_200_OK)
    

def get_chat_partners(current_user):
    # Get users where current_user is sender or receiver
    sent_to = Message.objects.filter(sender=current_user).exclude(receiver=None).values_list('receiver', flat=True)
    received_from = Message.objects.filter(receiver=current_user).values_list('sender', flat=True)
    # Union and remove duplicates
    user_ids = set(list(sent_to) + list(received_from))

    # Return the user queryset
    return CustomUser.objects.filter(id__in=user_ids)

class ChatList(APIView):
    authentication_classes = []      # <‑‑ skip auth checks
    permission_classes     = [AllowAny]
    def post(self, request , *args, **kwargs):
        token = request.headers.get('Authorization')
        token = token.split()[1]
        user_json = user_validation(token)
        if user_json["message"] == "User present":   
            user = user_json["user_obj"]
            result = get_chat_partners(user.id)
            all_masseges_json = CustomUserSerializer(result ,  many=True)
        return Response({"message": "User all massege.", 
                             "massege" :all_masseges_json.data 
                             }, status=status.HTTP_200_OK)
    

class SearchUserList(APIView):
    authentication_classes = []      # <‑‑ skip auth checks
    permission_classes     = [AllowAny]
    def post(self , request,*args, **kwargs ):
        token = request.headers.get('Authorization')
        token = token.split()[1]
        user_json = user_validation(token)
        if user_json["message"] == "User present":   
            user = user_json["user_obj"]
        user = CustomUser.objects.all().exclude(user.id)
        userList_json = CustomUserSerializer(user ,many=True )
        return Response({"message": "User all massege.", "result" :userList_json.data}, status=status.HTTP_200_OK)