import os
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from wells_map.forms import *
from  django.core import serializers 
from django.contrib.auth.decorators import login_required

# Create your views here.

# TIFF dosyalarının bulunduğu dizin
TIFF_DIR = 'D:/Projeler/gisenv/water_wells/wells_map/static/tiff'
@login_required
def list_layers(request):
    print("list_layer girdi")
    tiff_dir = os.path.join(settings.BASE_DIR, TIFF_DIR)
    layers = []
    for root, dirs, files in os.walk(tiff_dir):
        for file in files:
            if file.endswith('.tif'):
                layers.append({'name': file, 'url': f'/static/tiff/{file}'})
    return JsonResponse(layers, safe=False)
@login_required
def index(request):
    return render(request, "georaster/georaster.html", {})

@login_required
def georaster(request):
    form = LocationForm()
    locations = Location.objects.all()
    locations_json = serializers.serialize("json", locations)
    tiff_json= list_layers
    return render(
        request, "georaster/georaster.html", {"form": form, "locations_json": locations_json, "title": "Georaster Harita"}
    )
