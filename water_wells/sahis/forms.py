from django import forms
from .models import Sahis

class SahisForm(forms.ModelForm):
    class Meta:
        model = Sahis
        fields = [
            'tc_kimlik_no', 'adres', 'isim', 'telefon', 'il', 'ilce', 'koy', 
            'ada', 'parsel', 'koordinat1', 'koordinat2'
        ]
