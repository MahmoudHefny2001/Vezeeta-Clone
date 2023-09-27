from django.contrib import admin

from .models import TimeSlot, DateSlot

admin.site.register(TimeSlot)
admin.site.register(DateSlot)
