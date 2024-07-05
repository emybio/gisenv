from django.db import models

class Sahis(models.Model):
    tc_kimlik_no = models.CharField(max_length=11, unique=True)
    adres = models.CharField(max_length=255)
    isim = models.CharField(max_length=100)
    telefon = models.CharField(max_length=15)
    il = models.CharField(max_length=50)
    ilce = models.CharField(max_length=50)
    koy = models.CharField(max_length=50)
    ada = models.CharField(max_length=50)
    parsel = models.CharField(max_length=50)
    koordinat1 = models.CharField(max_length=50)
    koordinat2 = models.CharField(max_length=50)

    def __str__(self):
        return self.isim
