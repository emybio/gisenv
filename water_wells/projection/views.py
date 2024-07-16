from django.shortcuts import render
from wells_map.models import Location
from django.core import serializers

# Create your views here.


def proj(request):
    print("map")
    return render(request, "projections/map.html", {})


def proj2(request):
    print("map2")
    locations = Location.objects.all()
    locations_json = serializers.serialize("json", locations)
    title = "Projection 2"
    return render(
        request,
        "projections/map2.html",
        {"locations_json": locations_json, "title": title},
    )
