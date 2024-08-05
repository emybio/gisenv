from django.db import models
from firma.models import Firma
from users.models import CustomUser

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
    firma=models.ForeignKey(Firma, null=True,blank=True,on_delete=models.SET_NULL)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True,)

    def __str__(self): 
        return self.isim
