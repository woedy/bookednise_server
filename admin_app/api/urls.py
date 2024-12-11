from django.urls import path

from admin_app.api.views import overview_view, list_all_shops_admin_view, admin_shop_details_view, remove_vendor_view, \
    list_all_users_admin_view, admin_user_details_view, remove_user_view, list_all_bookings_admin_view, \
    remove_booking_view, list_all_bookings_review_view
from bookings.api.views import shop_bookings_view, shop_booking_detail_view

app_name = 'admin_app'

urlpatterns = [
    path('overview/', overview_view, name="overview_view"),
    path('list-vendors-admin/', list_all_shops_admin_view, name="list_all_shops_admin_view"),
    path('vendor-details/', admin_shop_details_view, name="admin_shop_details_view"),
    path('delete-vendor/', remove_vendor_view, name="remove_vendor_view"),

    path('list-all-users-admin/', list_all_users_admin_view, name="list_all_users_admin_view"),
    path('user-detail-admin/', admin_user_details_view, name="admin_user_details_view"),
    path('delete-user-admin/', remove_user_view, name="remove_user_view"),

    path('list-bookings-admin/', list_all_bookings_admin_view, name="list_all_bookings_admin_view"),
    path('delete-booking-admin/', remove_booking_view, name="remove_booking_view"),

    path('list-bookings-review/', list_all_bookings_review_view, name="list_all_bookings_review_view"),


]
