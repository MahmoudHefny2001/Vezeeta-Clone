from django.contrib import admin

from .models import DoctorExtended, DoctorProfile

admin.site.register(DoctorExtended)
admin.site.register(DoctorProfile)


class DoctorModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Hash the password before saving the object
        obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)