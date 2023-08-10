from django.contrib import admin
from .models import PatientExtended, PatientProfile

# Register your models here.


admin.site.register(PatientProfile)


class PatientModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Hash the password before saving the object
        obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

admin.site.register(PatientExtended, PatientModelAdmin)