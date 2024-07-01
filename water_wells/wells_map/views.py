from django.shortcuts import render, redirect
from django.core import serializers
from django.http import JsonResponse
from .models import Location
from .forms import LocationForm

def index(request):
    form = LocationForm()
    locations = Location.objects.all()
    locations_json = serializers.serialize('json', locations)
    print("*******" + locations_json)
    return render(request, 'maps/index.html', {'form': form, 'locations_json': locations_json})

def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        info = request.POST.get('info')
        print("lat: ")
        print(lat)
        if form.is_valid():
            print("form verisi geldi...")
            form.save()
            return JsonResponse({'status': 'success'})
        elif lat and lon:
            print("marker verisi geldi...")
            location=Location(latitude=lat,longitude=lon,info=info)
            location.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed', 'errors': form.errors})

def location_list(request):
    locations = Location.objects.all()
    return render(request, 'maps/location_list.html', {'locations': locations})


def georaster(request):
    form = LocationForm()
    locations = Location.objects.all()
    locations_json = serializers.serialize('json', locations)
    return render(request,'maps/georaster.html', {'form': form, 'locations_json': locations_json})

def serverraster(request):

    return render(request,'maps/serverraster.html')

def pngraster(request):

    return render(request,'maps/pngraster.html')