from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/events/<int:pk>/', consumers.EventConsumer.as_asgi()),
]
