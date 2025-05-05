from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import CustomUser, Task
from .serializers import CustomUserSerializer, TaskSerializer


@receiver(post_save, sender=CustomUser)
def track_employee_job(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    data = CustomUserSerializer(instance).data
    print("signal data for CustomUser:", data)

    async_to_sync(channel_layer.group_send)(
        "admin_customer",
        {
            "type": "user.create" if created else "user.update",
            "data": data,
        }
    )


@receiver(post_save, sender=Task)
def send_task_update(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    data = TaskSerializer(instance).data
    print("signal data for Task:", data)

    async_to_sync(channel_layer.group_send)(
        "admin_jobs",
        {
            "type": "job.update",
            "data": data,
        }
    )
