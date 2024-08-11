from django import forms
from .models import Il,Ilce,Semt, Mahalle


class IlceForm(forms.Form):
    il = forms.ModelChoiceField(queryset=Il.objects.all(),required=True)
   
class SemtForm(forms.Form):
    ilce=forms.ModelChoiceField(queryset=Ilce.objects.all(),required=True)
    
class MahalleForm(forms.Form):
    semt=forms.ModelChoiceField(queryset=Semt.objects.all(),required=True)     