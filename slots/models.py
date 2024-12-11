from django.db import models
from bookednise_pro import settings

from shop.models import ShopStaff

User = settings.AUTH_USER_MODEL


SLOT_STATE_CHOICES = (
    ("Vacant", "Vacant"),
    ("Partial", "Partial"),
    ("Occupied", "Occupied")
)

class StaffSlot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="staff_slot")

    slot_date = models.DateField(null=True, blank=True)
    time_slot_count = models.IntegerField(default=0)
    state = models.CharField(default="Vacant", choices=SLOT_STATE_CHOICES, max_length=255)

    is_recurring = models.BooleanField(default=False)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class TimeSlot(models.Model):
    staff_slot = models.ForeignKey(StaffSlot, on_delete=models.CASCADE, related_name="slot_times")
    booking_id = models.IntegerField(null=True, blank=True)

    time = models.TimeField(null=True, blank=True)


    occupied = models.BooleanField(default=False)
    occupant = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name="booking_occupant")

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
