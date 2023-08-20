from django.contrib import admin

from .models import DoctorExtended, DoctorProfile

from geo.models import Location


admin.site.register(DoctorProfile)


class DoctorModelAdmin(admin.ModelAdmin):
    # form = DoctorAdminForm

    def save_model(self, request, obj, form, change):
        # Hash the password before saving the object
        obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)



admin.site.register(DoctorExtended, DoctorModelAdmin)

