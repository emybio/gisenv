from flask import Flask, jsonify, send_from_directory
from django.http import JsonResponse
from django.conf import settings
import os

app = Flask(__name__)

# TIFF dosyalarının bulunduğu dizin
TIFF_DIR = 'D:/Projeler/125000haritalar/harita/x'

def list_layers(request):
    tiff_dir = os.path.join(settings.BASE_DIR, TIFF_DIR)
    layers = []
    for root, dirs, files in os.walk(tiff_dir):
        for file in files:
            if file.endswith('.tif'):
                layers.append({'name': file, 'url': f'/static/{file}'})
    return JsonResponse(layers, safe=False)

@app.route('/api/layers', methods=['GET'])
def get_layers():
    # TIFF dosyalarını listele
    files = [f for f in os.listdir(TIFF_DIR) if f.endswith('.tif')]
    layers = [{'name': f, 'url': f'/static/{f}'} for f in files]
    return jsonify(layers)

@app.route('/static/<path:filename>')
def serve_file(filename):
    return send_from_directory(TIFF_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)