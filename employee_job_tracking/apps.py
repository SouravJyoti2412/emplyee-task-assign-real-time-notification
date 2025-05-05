
from django.apps import AppConfig

class EmployeeJobTrackingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employee_job_tracking'
    def ready(self):
        import employee_job_tracking.signals
        return employee_job_tracking.signals
