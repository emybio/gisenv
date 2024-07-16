from django.shortcuts import render
from wells_map.forms import *
from  django.core import serializers

# Create your views here.


def index(request):
    return render(request, "georaster/georaster.html", {})


def georaster(request):
    form = LocationForm()
    locations = Location.objects.all()
    locations_json = serializers.serialize("json", locations)
    return render(
        request, "georaster/georaster.html", {"form": form, "locations_json": locations_json, "title": "Georaster Harita"}
    )
