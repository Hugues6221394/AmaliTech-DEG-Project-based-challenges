from django.db import models
# Create your models here.

class Monitor(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    timeout = models.IntegerField()
    alert_email = models.EmailField()
    STATUS_CHOICES = [
        ('up', 'Up'),
        ('down', 'Down')
    ]

    status = models.CharField(max_length=10, choices= STATUS_CHOICES, default='up')

    last_heartbeat = models.DateTimeField(null=True, blank= True)
    is_paused = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
