from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.http import JsonResponse,HttpResponse
from .models import Location
from .forms import LocationForm
import pyproj,json
import shapefile
from django.core.files.storage import FileSystemStorage
from geojson import Feature, FeatureCollection, Point
import os
import geojson
from pathlib import Path

SHP_FOLDER = Path('D:/Projeler/125000haritalar/')
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

def edit_location(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect('location_list')
    else:
        form = LocationForm(instance=location)
    return render(request, 'maps/edit_location.html', {'form': form})

def delete_location(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        location.delete()
        return redirect('location_list')
    return render(request, 'maps/delete_location.html', {'location': location})

def georaster(request):
    form = LocationForm()
    locations = Location.objects.all()
    locations_json = serializers.serialize('json', locations)
    return render(request,'maps/georaster.html', {'form': form, 'locations_json': locations_json})

def serverraster(request):

    return render(request,'maps/serverraster.html')

def pngraster(request):

    return render(request,'maps/pngraster.html')

def get_locations(request):
    locations = Location.objects.all()
    data = {
        'locations': [
            {'lat': loc.latitude, 'lon': loc.longitude, 'info': loc.info}
            for loc in locations
        ]
    }
    return JsonResponse(data)


def convert_wgs84_to_utm(lat, lon):
    wgs84 = pyproj.Proj(init='epsg:4326')
    utm33n = pyproj.Proj(proj='utm', zone=33, datum='WGS84')
    utm_x, utm_y = pyproj.transform(wgs84, utm33n, lon, lat)
    return utm_x, utm_y

def update_coordinates_to_utm(request):
    locations = Location.objects.all()
    for loc in locations:
        utm_x, utm_y = convert_wgs84_to_utm(loc.latitude, loc.longitude)
        loc.latitude = utm_y
        loc.longitude = utm_x
        loc.save()
    return JsonResponse({'status': 'success'})


def shpView(request):

    return render(request,'maps/shp.html')

def upload_shapefile(request):
    if request.method == 'POST' and 'shapefile' in request.FILES and 'dbffile' in request.FILES:
        shp_file = request.FILES['shapefile']
        dbf_file = request.FILES['dbffile']
        fs = FileSystemStorage()
        shp_filename = fs.save(shp_file.name, shp_file)
        dbf_filename = fs.save(dbf_file.name, dbf_file)
        shp_file_path = fs.path(shp_filename)
        dbf_file_path = fs.path(dbf_filename)
        
        try:
            # Read shapefile
            with shapefile.Reader(shp=shp_file_path, dbf=dbf_file_path) as reader:
                fields = reader.fields[1:]
                field_names = [field[0] for field in fields]
                features = []
                for sr in reader.shapeRecords():
                    atr = dict(zip(field_names, sr.record))
                    geom = sr.shape.__geo_interface__
                    features.append(Feature(geometry=geom, properties=atr))
            
            # Convert to GeoJSON
            geojson = FeatureCollection(features)
            geojson_filename = shp_filename.replace('.shp', '.geojson')
            geojson_path = fs.path(geojson_filename)
            with open(geojson_path, 'w') as geojson_file:
                json.dump(geojson, geojson_file)

            # Clean up the uploaded files
            os.remove(shp_file_path)
            os.remove(dbf_file_path)

            # Return the GeoJSON file URL
            geojson_url = fs.url(geojson_filename)
            print(f'GeoJSON URL: {geojson_url}')  # Debugging line
            return JsonResponse({'geojson_url': geojson_url})
        
        except Exception as e:  
            os.remove(shp_file_path)
            os.remove(dbf_file_path)
            return HttpResponse(status=500, content=str(e))

    return render(request, 'maps/uploadshp.html')

def list_shp_files():
    shp_files = []
    for root, dirs, files in os.walk(SHP_FOLDER):
        for file in files:
            if file.endswith('.shp'):
                full_path = os.path.join(root, file)
                shp_files.append(full_path)
    return shp_files

def shp_to_geojson(shp_path):
    reader = shapefile.Reader(shp_path)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    features = []

    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        features.append(geojson.Feature(geometry=geom, properties=atr))

    return geojson.FeatureCollection(features)

def map_view(request):
   
   
    return render(request, 'maps/map.html')

def geojson_view(request):
    shp_path = 'D:/Projeler/125000haritalar/6_bolge/bolge_formasyon_sinir.shp'
    print("dosya : "+shp_path)
    geojson_data = shp_to_geojson(shp_path)
    return JsonResponse(geojson_data, safe=False)