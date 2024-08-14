from django.db import models

# Create your models here.


class Il(models.Model):
    ad = models.CharField(max_length=100)

    def __str__(self):
        return self.ad


class Ilce(models.Model):
    
    il = models.ForeignKey(Il,  on_delete=models.CASCADE,null=True)
    ad = models.CharField(max_length=100)

    def __str__(self):
        return self.ad


class Semt(models.Model):
   
    il = models.ForeignKey(Il, related_name="semt_il", on_delete=models.CASCADE,null=True)
    ilce = models.ForeignKey(Ilce, related_name="semt_ilce", on_delete=models.CASCADE,null=True)
    ad = models.CharField(max_length=100)

    def __str__(self):
        return self.ad


class Mahalle(models.Model):
    il = models.ForeignKey(Il, related_name="mahalle_il", on_delete=models.CASCADE,null=True)
    ilce = models.ForeignKey(Ilce, related_name="mahalle_ilce", on_delete=models.CASCADE,null=True)
    
    semt = models.ForeignKey(
        Semt, related_name="mahalle_semt", on_delete=models.CASCADE, null=True
    )
    ad = models.CharField(max_length=100)
    posta_kodu=models.IntegerField(default=0)

    def __str__(self):
        return self.ad   
