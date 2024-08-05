from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.http import JsonResponse,HttpResponse
from water_wells.shape.views import CustomJSONEncoder, shp_to_geojson_with_fiona
from wells_map.models import Location
import urllib.parse
import pyproj,json
import shapefile
from django.core.files.storage import FileSystemStorage
from geojson import Feature, FeatureCollection, Point
import os
import geojson
from pathlib import Path
import fiona
from shapely.geometry import shape, mapping
from pyproj import Transformer
from json import JSONEncoder
from django.contrib.auth.decorators import login_required

SHP_FOLDER = Path('D:/Projeler/125000haritalar/harita/x')

@login_required
def tif_view(request, shp_filename):
    shp_filename = urllib.parse.unquote(shp_filename)
    shp_path = os.path.join(SHP_FOLDER, shp_filename)
    try:
        geojson_data = shp_to_geojson_with_fiona(shp_path)
        # Log the GeoJSON data for debugging purposes
        #print(geojson_data)
        return JsonResponse(geojson_data, encoder=CustomJSONEncoder, safe=False)
    except Exception as e:
         print(f"Error processing SHP file {shp_filename}: {e}") 
         raise