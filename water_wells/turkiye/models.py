from django.db import models

# Create your models here.


class Il(models.Model):
    ad = models.CharField(max_length=100)

    def __str__(self):
        return self.ad


class Ilce(models.Model):
    ad = models.CharField(max_length=100)
    il = models.ForeignKey(Il, related_name="ilceler", on_delete=models.CASCADE)

    def __str__(self):
        return self.ad


class Semt(models.Model):
   
    il = models.ForeignKey(Il, related_name="semt_il", on_delete=models.CASCADE,null=True)
    ilce = models.ForeignKey(Ilce, related_name="semtler", on_delete=models.CASCADE)
    ad = models.CharField(max_length=100)

    def __str__(self):
        return self.ad


class Mahalle(models.Model):
    il = models.ForeignKey(Il, related_name="mahalle_il", on_delete=models.CASCADE,null=True)
    ilce = models.ForeignKey(Ilce, related_name="mahallle_ilce", on_delete=models.CASCADE,null=True)
    
    semt = models.ForeignKey(
        Semt, related_name="mahalle_semt", on_delete=models.CASCADE, null=True
    )
    ad = models.CharField(max_length=100)
    posta_kodu=models.IntegerField(default=0)

    def __str__(self):
        return self.ad   
