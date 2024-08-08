from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os

@login_required
def get_kml_files(request):
    kml_folder_path = settings.BASE_DIR / 'static' / 'kml'
    kml_files = [f for f in os.listdir(kml_folder_path) if f.endswith('.kml')]
    return JsonResponse({'kml_files': kml_files})

@login_required
def get_kml_data(request):
    kml_filename = request.GET.get('filename', None)
    if not kml_filename:
        return JsonResponse({'error': 'Filename not provided'}, status=400)

    kml_file_path = settings.BASE_DIR / 'static' / 'kml' / kml_filename
    if not kml_file_path.exists():
        return JsonResponse({'error': 'KML file not found'}, status=404)
    
    with open(kml_file_path, 'r', encoding='utf-8') as file:
        kml_content = file.read()
    
    return JsonResponse({'kml_data': kml_content})

def kmz_home(request):
    
    return render(request,'kmz/index.html')

@login_required 
def kml_display(request):
    
    return render(request,'kmz/kml_map.html')