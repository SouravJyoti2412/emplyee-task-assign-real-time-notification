from django.shortcuts import render

def notification(request):
    return render(request, 'notification.html')


def notification2(request):
    return render(request, 'notification2.html')