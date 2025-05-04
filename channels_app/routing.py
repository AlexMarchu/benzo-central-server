from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'api/ws/station/(?P<station_id>\w+)$', consumers.ServerConsumer.as_asgi()),
]