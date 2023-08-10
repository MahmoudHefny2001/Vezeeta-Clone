from django.contrib import admin

# Register your models here.


from .models import Person
  
  
class PersonModelAdmin(admin.ModelAdmin): 
    pass
    # def save_model(self, request, obj, form, change): 
        # Hash the password before saving the object 
        # obj.set_password(form.cleaned_data['password']) 
        # super().save_model(request, obj, form, change)

admin.site.register(Person, PersonModelAdmin)