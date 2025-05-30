from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/report/status/(?P<task_id>\w+)/$', consumers.ReportStatusConsumer.as_asgi()),
]