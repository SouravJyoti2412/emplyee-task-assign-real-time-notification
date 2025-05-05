from django.db import models
import uuid

class CustomUser(models.Model):
    choices=[("admin", "Admin"), ("employee", "Employee")]
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Hashed manually or with bcrypt
    role = models.CharField(choices, max_length=50)
    token = models.JSONField(null=True, blank=True , default=None)  # For storing JWT or other tokens
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

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