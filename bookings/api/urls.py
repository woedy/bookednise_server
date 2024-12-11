from django.urls import path

from bookings.api.views import change_booking_status, shop_bookings_view, shop_booking_detail_view, book_appointment_view, \
    client_bookings_view, reschedule_appointment_view, cancel_appointment_view, make_payment_view, booking_ratings, \
    add_split_view, walkin_booking_view, complete_appointment_view, send_booking_chat_message, \
    get_booking_chat_messages, client_bookings_chat, shop_bookings_chat
from chats.api.views import send_chat_message

app_name = 'bookings'

urlpatterns = [
    path('shop-bookings/', shop_bookings_view, name="shop_bookings_view"),
    path('shop-booking-detail/', shop_booking_detail_view, name="shop_booking_detail_view"),

    path('book-appointment/', book_appointment_view, name="book_appointment_view"),
    path('walkin-booking/', walkin_booking_view, name="walkin_booking_view"),
    path('add-split/', add_split_view, name="add_split_view"),
    path('client-bookings/', client_bookings_view, name="client_bookings_view"),
    path('reschedule-appointment/', reschedule_appointment_view, name="reschedule_appointment_view"),
    path('change-booking-status/', change_booking_status, name="change_booking_status"),
    path('cancel-appointment/', cancel_appointment_view, name="cancel_appointment_view"),
    path('complete-appointment/', complete_appointment_view, name="complete_appointment_view"),
    path('make-payment/', make_payment_view, name="make_payment_view"),
    path('rate-booking/', booking_ratings, name="booking_ratings"),

    #path('booking-chats/', send_chat_message, name="send_chat_message"),
    path('send-booking-chat/', send_booking_chat_message, name="send_booking_chat_message"),
    path('get-booking-chats/', get_booking_chat_messages, name="get_booking_chat_messages"),
    path('get-client-bookings-chats/', client_bookings_chat, name="client_bookings_chat"),
    path('get-shop-bookings-chats/', shop_bookings_chat, name="shop_bookings_chat"),


]
