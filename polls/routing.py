from django.urls import path
from .consumers import PollConsumer


websocket_urlpatterns = [
    path('ws/poll/', PollConsumer.as_asgi()),
]
