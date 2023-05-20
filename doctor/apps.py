from django.apps import AppConfig


class DoctorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'doctor'
    verbose_name = 'Doctor'


    def ready(self):
        import doctor.signals
        

