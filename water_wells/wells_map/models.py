from django.db import models
from users.models import CustomUser

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    info = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True,)

    def __str__(self):
        return f"({self.latitude}, {self.longitude})"
    
