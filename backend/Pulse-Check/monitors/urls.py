from django.urls import path
from .views import MonitorCreateView, HeartbeatView, MonitorStatusCheckView, PauseMonitorView

urlpatterns = [
    path('monitors/', MonitorCreateView.as_view(), name='create-monitor'),
    path('monitors/<str:device_id>/heartbeat/', HeartbeatView.as_view(), name='heartbeat'),
    path('monitors/check-status/', MonitorStatusCheckView.as_view(), name='check-status'),
    path('monitors/<str:device_id>/pause/', PauseMonitorView.as_view(), name='pause-monitor'),
]