from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.http import JsonResponse,HttpResponse
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


# Create your views here.

SHP_FOLDER = Path('D:/Projeler/125000haritalar/')

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode()
        if isinstance(obj, fiona.collection.Properties):
            return dict(obj)
        return JSONEncoder.default(self, obj)
    
class ConvertShpToGeoJSON(View):
    def get(self, request, shp_file):
        shp_file_path = os.path.join(SHP_FOLDER, shp_file)

        if not os.path.exists(shp_file_path):
            return JsonResponse({'error': 'Shapefile not found'}, status=404)

        try:
            with fiona.open(shp_file_path) as src:
                transformer = Transformer.from_crs(src.crs, "EPSG:4326", always_xy=True)
                features = []

                for feature in src:
                    geom = shape(feature['geometry'])

                    # Transforming the coordinates
                    if geom.geom_type == 'Polygon':
                        transformed_coords = [
                            [transformer.transform(x, y) for x, y in ring]
                            for ring in geom.exterior.coords
                        ]
                        geom = shape({'type': 'Polygon', 'coordinates': [transformed_coords]})
                    elif geom.geom_type == 'MultiPolygon':
                        transformed_coords = [
                            [[transformer.transform(x, y) for x, y in ring] for ring in polygon.exterior.coords]
                            for polygon in geom.geoms
                        ]
                        geom = shape({'type': 'MultiPolygon', 'coordinates': transformed_coords})

                    features.append({
                        'type': 'Feature',
                        'geometry': mapping(geom),
                        'properties': feature['properties']
                    })

                geojson = {
                    'type': 'FeatureCollection',
                    'features': features
                }

                return JsonResponse(geojson)
        except Exception as e:
            return JsonResponse({'error': f'Error processing SHP file {shp_file_path}: {str(e)}'}, status=500)
    
def shp_to_geojson(shp_path):
    try:
        reader = shapefile.Reader(shp_path)
        fields = reader.fields[1:]
        field_names = [field[0] for field in fields]
        features = []

        for sr in reader.shapeRecords():
            atr = dict(zip(field_names, sr.record))
            geom = sr.shape.__geo_interface__
            features.append(geojson.Feature(geometry=geom, properties=atr))

        return geojson.FeatureCollection(features)
    except Exception as e:
        print(f"Error converting SHP to GeoJSON: {e}")
        raise
    
def shp_to_geojson_with_fiona(shp_path):
    try:
        features = []
        with fiona.open(shp_path, 'r',encoding='latin1') as source:
            for feature in source:
                # Özellikleri JSON formatına uygun hale getir
                geom = feature['geometry']
                props = {k: str(v) for k, v in feature['properties'].items()}
                features.append(geojson.Feature(geometry=geom, properties=props))
        return geojson.FeatureCollection(features)
    except Exception as e:
        print(f"Error converting SHP to GeoJSON with Fiona: {e}")
        raise

def geojson_view(request, shp_filename):
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

def list_shp_files():
    shp_files = []
    for root, dirs, files in os.walk(SHP_FOLDER):
        for file in files:
            if file.endswith('.shp'):
                full_path = os.path.join(root, file)
                shp_files.append(full_path)
    return shp_files


def shpView(request):
    shp_files = list_shp_files()
    encoded_shp_files = [urllib.parse.quote(f) for f in shp_files]
    return render(request, 'maps/shpmap.html', {'shp_files': zip(shp_files, encoded_shp_files)})

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



