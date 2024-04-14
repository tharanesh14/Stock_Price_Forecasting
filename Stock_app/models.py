from django.db import models
from django.contrib.auth.models import User

class Hub(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_id')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_provider')
    
    def __str__(self):
        return self.name

class Machine(models.Model):
    hub = models.ForeignKey(Hub, related_name='machines', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    serial_code = models.CharField(max_length=100)
    purchase_date = models.DateField()
    last_service_date = models.DateField(null=True, blank=True)
    last_service_component = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name
