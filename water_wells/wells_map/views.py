from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from .models import Location
from .forms import LocationForm
import pyproj, json
import shapefile
from django.core.files.storage import FileSystemStorage
from geojson import Feature, FeatureCollection, Point
import os
import geojson
from pathlib import Path
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    form = LocationForm()
    locations = Location.objects.all()
    locations_json = serializers.serialize("json", locations)
    print("*******" + locations_json)
    return render(
        request,
        "maps/index.html",
        {"form": form, "locations_json": locations_json, "title": "Anasayfa"},
    )

@login_required
def add_location(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        lat = request.POST.get("lat")
        lon = request.POST.get("lon")
        info = request.POST.get("info")
        print("lat: ")
        print(lat)
        if form.is_valid():
            print("form verisi geldi...")
            form.save()
            return JsonResponse({"status": "success"})
        elif lat and lon:
            print("marker verisi geldi...")
            location = Location(latitude=lat, longitude=lon, info=info)
            location.save()
            return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed", "errors": form.errors})

@login_required
def location_list(request):
    locations = Location.objects.all()
    return render(request, "maps/location_list.html", {"locations": locations})

@login_required
def edit_location(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == "POST":
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect("location_list")
        
    else:
        form = LocationForm(instance=location)
    return render(request, "maps/edit_location.html", {"form": form})

@login_required
def delete_location(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == "POST":
        location.delete()
        return redirect("location_list")
    return render(request, "maps/delete_location.html", {"location": location})




def serverraster(request):

    return render(request, "maps/serverraster.html")


def pngraster(request):

    return render(request, "maps/pngraster.html")


def get_locations(request):
    locations = Location.objects.all()
    data = {
        "locations": [
            {"lat": loc.latitude, "lon": loc.longitude, "info": loc.info}
            for loc in locations
        ]
    }
    return JsonResponse(data)


def convert_wgs84_to_utm(lat, lon):
    wgs84 = pyproj.Proj(init="epsg:4326")
    utm33n = pyproj.Proj(proj="utm", zone=33, datum="WGS84")
    utm_x, utm_y = pyproj.transform(wgs84, utm33n, lon, lat)
    return utm_x, utm_y


def update_coordinates_to_utm(request):
    locations = Location.objects.all()
    for loc in locations:
        utm_x, utm_y = convert_wgs84_to_utm(loc.latitude, loc.longitude)
        loc.latitude = utm_y
        loc.longitude = utm_x
        loc.save()
    return JsonResponse({"status": "success"})


def map_view(request):

    return render(
        request,
        "maps/index.html",
        {
            "title": "Anasayfa",
        },
    )


# def custom_404(request, exception):
#     return render(request, 'errors/404.html', status=404)

# def custom_500(request):
#     return render(request, 'errors/500.html', status=500)