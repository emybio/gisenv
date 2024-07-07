from django import forms
from .models import Firma

class FirmaForm(forms.ModelForm):
    class Meta:
        model = Firma
        fields = [
            'isim', 'meslek', 'diploma_oda_sicil_no', 'adres', 
        ]
