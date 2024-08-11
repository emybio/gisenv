from django.shortcuts import render
from django.http import JsonResponse
from .models import Il,Ilce,Semt,Mahalle
import requests
from bs4 import BeautifulSoup

# Create your views here.

def get_ilceler(request):
    il_id= request.GET.get('il_id')
    ilceler= Ilce.objects.filter(il_id=il_id).values('id','ad')
    return JsonResponse(list(ilceler),safe=False)

def get_semtler(request):
    ilce_id=request.GET.get('ilce_id')
    semtler=Semt.objects.filter(ilce_id=ilce_id).values('id','ad')
    return JsonResponse(list(semtler),safe=False)
    
def get_mahalleler(request):
    semt_id= request.GET.get('semt_id')
    mahalleler = Mahalle.objects.filter(semt_id=semt_id).values('id','ad')
    return JsonResponse(list(mahalleler),safe= False)

def get_yerler(request):
    iller = Il.objects.all()
    return render(request,"turkiye/yerler.html",{'iller':iller})

def scrape_parcel_data(request):
    url = 'https://parselsorgu.tkgm.gov.tr/'  # İlgili URL'yi buraya yazın
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Web sayfasından gerekli verileri çekin
    # Örneğin, tüm parsel verilerini toplama işlemi
    data = []
    for item in soup.find_all('canvas'):  # İlgili HTML elementini seçin
        data.append({
            'key': item.find('key-selector').text,  # Veriyi çekme işlemi
            'value': item.find('value-selector').text,
        })
    
    return JsonResponse(data, safe=False)