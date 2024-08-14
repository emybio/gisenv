from django import forms
from .models import Sahis

class SahisForm(forms.ModelForm):
    
    class Meta:
        model = Sahis
        fields = ['id',
            'tc_kimlik_no', 'adres', 'isim', 'telefon', 'mahalle',
            'ada', 'parsel', 'koordinat1', 'koordinat2', 'firma'
        ]
        widgets = {
            'firma': forms.Select(attrs={'class': 'form-control'}),
            'mahalle':forms.Select(attrs={'class':'form-control'}),
        }
        
def __init__(self, *args, **kwargs):
    super(SahisForm, self).__init__(*args, **kwargs)
    self.fields['firma'].required = False  