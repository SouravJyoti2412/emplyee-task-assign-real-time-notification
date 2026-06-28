from django.contrib import admin
from .models import CustomUser, Task , Message



from guardian.admin import GuardedModelAdmin

@admin.register(CustomUser)
class DocumentAdmin(GuardedModelAdmin):
    pass

@admin.register(Task)
class TaskAdmin(GuardedModelAdmin):
    pass

@admin.register(Message)
class MessegeAdmin(GuardedModelAdmin):
    pass