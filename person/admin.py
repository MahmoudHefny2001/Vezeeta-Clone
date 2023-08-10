from django.contrib import admin

# Register your models here.


from .models import Person
  
 admin.site.register(Person)
  
 class PersonModelAdmin(admin.ModelAdmin): 
     def save_model(self, request, obj, form, change): 
         # Hash the password before saving the object 
         obj.set_password(form.cleaned_data['password']) 
         super().save_model(request, obj, form, change)
