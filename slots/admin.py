from django.contrib import admin

from slots.models import StaffSlot, TimeSlot

# Register your models here.
admin.site.register(StaffSlot)
admin.site.register(TimeSlot)
