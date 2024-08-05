from django.db import models
from django.conf import settings

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    info = models.CharField(max_length=255,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"({self.latitude}, {self.longitude})"
    
