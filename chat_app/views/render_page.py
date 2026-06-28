from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from employee_job_tracking.models import CustomUser

def index(request):
    return render(request,'index.html')


def login(request):
    return render(request,'login.html')



def register(request):
    return render(request,'register.html')

def chat(request, receiver_id):
    user = 24
    print(user)
    receiver = get_object_or_404(CustomUser, id=receiver_id)
    print(receiver)

    # Private room name generation
    def get_room_name(user1_id, user2_id):
        return f"private_{min(user1_id, user2_id)}_{max(user1_id, user2_id)}"

    room_name = get_room_name(user, receiver.id)

    return render(request, 'chatting.html', {
        'room_name': room_name,
        'receiver': receiver,
    })
