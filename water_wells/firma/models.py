from django.db import models
from django.conf import settings
#from sahis.models import Sahis  # Sahis modelini import edin

class Firma(models.Model):
    isim = models.CharField(max_length=100)
    meslek = models.CharField(max_length=100)
    diploma_oda_sicil_no = models.CharField(max_length=50)
    adres = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    #sahislar = models.ManyToManyField(Sahis, related_name='firmalar',null=True)

    def __str__(self):
        return self.isim
