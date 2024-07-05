from django.db import models
from sahis.models import Sahis  # Sahis modelini import edin

class Firma(models.Model):
    isim = models.CharField(max_length=100)
    meslek = models.CharField(max_length=100)
    diploma_oda_sicil_no = models.CharField(max_length=50)
    adres = models.CharField(max_length=255)
    sahislar = models.ManyToManyField(Sahis, related_name='firmalar')

    def __str__(self):
        return self.isim
