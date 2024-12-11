from django.db import models
from bookednise_pro import settings
from django.db.models.signals import pre_save

from bookednise_pro.utils import unique_booking_id_generator
from chats.models import PrivateChatRoom
from shop.models import ShopService, Shop, ShopStaff, ShopPackage
from slots.models import StaffSlot

User = settings.AUTH_USER_MODEL


STATUS_CHOICE = (

    ('Created', 'Created'),
    ('Pending', 'Pending'),
    ('Confirmed', 'Confirmed'),
    ('Rescheduled', 'Rescheduled'),
    ('Approved', 'Approved'),
    ('Declined', 'Declined'),
    ('Started', 'Started'),
    ('Ongoing', 'Ongoing'),
    ('Review', 'Review'),
    ('Completed', 'Completed'),
    ('Canceled', 'Canceled'),
)


class Booking(models.Model):
    booking_id = models.CharField(max_length=200, null=True, blank=True)
    room = models.ForeignKey(PrivateChatRoom, on_delete=models.SET_NULL, null=True, related_name='booking_chat_rooms')
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True, related_name='shop_bookings')
    service = models.ForeignKey(ShopService, on_delete=models.SET_NULL, null=True, related_name='shop_service_bookings')
    booked_staff = models.ForeignKey(ShopStaff, on_delete=models.SET_NULL, null=True,related_name='booking_staffs')
    package = models.ForeignKey(ShopPackage, on_delete=models.SET_NULL, null=True,related_name='booking_package')
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='shop_service_bookings')
    service_type = models.CharField(max_length=200,  null=True, blank=True)
    home_service = models.BooleanField(default=False, blank=True, null=True)
    slot = models.ForeignKey(StaffSlot, on_delete=models.SET_NULL, null=True, blank=True, related_name="staff_slot")

    booking_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    booking_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    re_scheduled = models.BooleanField(default=False)
    booking_rescheduled_at = models.DateTimeField(null=True, blank=True)

    split = models.BooleanField(default=False, blank=True, null=True)
    booking_split_from = models.TimeField(null=True, blank=True)
    booking_split_to = models.TimeField(null=True, blank=True)

    amount_to_pay = models.CharField(null=True, blank=True, max_length=100)
    actual_price = models.CharField(null=True, blank=True, max_length=100)
    paid = models.BooleanField(default=False)

    confirm_payment = models.BooleanField(default=False)
    is_gift = models.BooleanField(default=False)

    actual_duration = models.CharField(null=True, blank=True, max_length=100)

    notes = models.TextField(null=True, blank=True)

    review = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, default="Pending", null=True, blank=True, choices=STATUS_CHOICE)

    booking_start = models.DateTimeField(null=True, blank=True)
    booking_end = models.DateTimeField(null=True, blank=True)

    booking_approved_at = models.DateTimeField(null=True, blank=True)
    booking_declined_at = models.DateTimeField(null=True, blank=True)
    booking_cancelled_at = models.DateTimeField(null=True, blank=True)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.booking_id












def pre_save_booking_id_generator(sender, instance, *args, **kwargs):
    if not instance.booking_id:

        instance.booking_id = unique_booking_id_generator(instance)

pre_save.connect(pre_save_booking_id_generator, sender=Booking)



class GiftBooking(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='gift_bookings')
    customer_name = models.CharField(max_length=200,  null=True, blank=True)
    customer_phone = models.CharField(max_length=200,  null=True, blank=True)
    customer_email = models.CharField(max_length=200,  null=True, blank=True)


    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BookingPayment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booking_payments')
    payment_method = models.CharField(max_length=200,  null=True, blank=True)
    amount = models.CharField(max_length=200,  null=True, blank=True)


    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BookingRating(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booking_ratings')
    rating = models.IntegerField(default=0)
    report = models.TextField(null=True, blank=True)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class WalkInBooking(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='walk_in_bookings')
    customer_name = models.CharField(max_length=200,  null=True, blank=True)
    contact = models.CharField(max_length=200,  null=True, blank=True)
    email = models.CharField(max_length=200,  null=True, blank=True)


    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


