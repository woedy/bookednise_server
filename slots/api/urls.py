from django.urls import path

from slots.api.views import set_staff_slot, list_staff_availability, set_availability_interval, set_staff_slot_shop_default, update_staff_slot, \
    remove_staff_slot

app_name = 'slots'

urlpatterns = [
    path('set-shop-default-availability/', set_staff_slot_shop_default, name="set_staff_slot_shop_default"),
    path('set-availability/', set_staff_slot, name="set_staff_slot"),
    path('update-availability/', update_staff_slot, name="update_staff_slot"),
    path('remove-availability/', remove_staff_slot, name="remove_staff_slot"),
    path('list-staff-availability/', list_staff_availability, name="list_staff_availability"),
#
    path('set-availability-interval/', set_availability_interval, name="set_availability_interval")

]
