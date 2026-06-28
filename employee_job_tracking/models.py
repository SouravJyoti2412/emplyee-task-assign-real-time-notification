from django.db import models
import uuid

# class CustomUser(models.Model):
#     choices=[("admin", "Admin"), ("employee", "Employee")]
#     uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     full_name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)  # Hashed manually or with bcrypt
#     role = models.CharField(choices, max_length=50)
#     token = models.JSONField(null=True, blank=True , default=None)  # For storing JWT or other tokens
#     is_verified = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

class CustomUser(models.Model):
    ROLE_CHOICES = [("admin", "Admin"), ("employee", "Employee")]
    AUTH_PROVIDER_CHOICES = [
        ('email', 'Email'),
        ('google', 'Google'),
        ('facebook', 'Facebook'),
        ('github', 'GitHub'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, blank=True)  # blank allowed for social users
    role = models.CharField(choices=ROLE_CHOICES, max_length=50)
    token = models.JSONField(null=True, blank=True, default=None)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # New fields
    auth_provider = models.CharField(
        max_length=20, choices=AUTH_PROVIDER_CHOICES, default='email'
    )
    profile_picture = models.URLField(null=True, blank=True)  # optional but common

    def __str__(self):
        return self.email

class Task(models.Model):
    choices=[("Pending", "Pending"), ("In_Progress", "In_Progress"), ("Completed", "Completed")]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(choices, default="Pending")
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'task_db'
        managed = True
        verbose_name = 'Task'
        verbose_name_plural = 'All task'




class Message(models.Model):
    MESSAGE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('voice', 'Voice'),
        ('file', 'File'),
    ]

    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE, null=True, blank=True)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, default='text')
    content = models.TextField(blank=True, null=True)  # Text content
    media_file = models.FileField(upload_to='chat_media/', blank=True, null=True)  # Image, Video, Voice
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.full_name} to {self.receiver.full_name if self.receiver else 'Room'}: {self.message_type}"
