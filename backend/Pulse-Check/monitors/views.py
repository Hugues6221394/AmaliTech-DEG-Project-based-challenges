from django.db.models.expressions import result
from django.utils import timezone

from django.core.serializers import serialize
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Monitor
from .serializers import MonitorSerializer

class MonitorCreateView(APIView):
    def get(self, request):
        monitors = Monitor.objects.all()

        serializer = MonitorSerializer(monitors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = MonitorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# to handle heartbeat requests
class HeartbeatView(APIView):
    def post(self, request, device_id):
        try:
            monitor = Monitor.objects.get(device_id=device_id)
        except Monitor.DoesNotExist:
            return Response(
                {"error": "Monitor not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        monitor.last_heartbeat = timezone.now()
        monitor.status='up'

        if monitor.is_paused:
            monitor.is_paused = False
        monitor.save()

        return Response(
            {"message": "Heartbeat received"},
            status=status.HTTP_200_OK
        )

#checking system state
class MonitorStatusCheckView(APIView):
    def get(self, request):
        monitors = Monitor.objects.all()
        results = []
        for monitor in monitors:
            if monitor.is_paused: #Paused devices should NOT trigger alerts.
                continue
            if monitor.last_heartbeat is None:
                continue

            time_difference = (timezone.now() - monitor.last_heartbeat).total_seconds()

            if time_difference > monitor.timeout:
                monitor.status = 'down'
                monitor.save()

                #Trigger alert
                print(
                    {"ALERT": f"Device {monitor.device_id} is down!",
                     "time": str(timezone.now())
                     }
                )

                #Store result
                results.append({
                    "device_id": monitor.device_id,
                    "status": "down"
                })

            else:
                results.append({
                    "device_id": monitor.device_id,
                    "status": "up"
                })

        return Response(results, status=status.HTTP_200_OK)


class PauseMonitorView(APIView):
    def post(self, request, device_id):
        try:
            monitor = Monitor.objects.get(device_id=device_id)
        except Monitor.DoesNotExist:
            return Response(
                {"error": "Monitor not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        monitor.is_paused= True
        monitor.save()

        return Response(
            {"message": f"Monitor {device_id} paused"},
            status=status.HTTP_200_OK
        )
