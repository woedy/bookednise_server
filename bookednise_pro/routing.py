from django.urls import path, re_path

from chats.api.consumers import BookingChatConsumers
from chats.consumers import ChatConsumer

websocket_urlpatterns = [

    path('ws/communications/chats', BookingChatConsumers.as_asgi()),
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),

]