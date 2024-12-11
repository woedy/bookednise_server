from django.contrib import admin

from bookings.models import Booking, BookingPayment, BookingRating, GiftBooking, WalkInBooking

# Register your models here.

admin.site.register(Booking)
admin.site.register(GiftBooking)
admin.site.register(BookingPayment)
admin.site.register(BookingRating)
admin.site.register(WalkInBooking)
