import os
import django
import json
from django.conf import settings



def load_bounds_from_json(filename):
    # Static dosya yolunu oluşturun
    file_path = "C:/Users/kur06/Documents/GitHub/gisenv/water_wells/static/json/"+ filename
    
    # Dosyayı açıp JSON verilerini okuyun
    with open(file_path, 'r') as file:
        bounds_data = json.load(file)
    return bounds_data  

def main():
    bounds_data = load_bounds_from_json('bounds.json')  # JSON dosyasının adı
    print(bounds_data)  # Yüklenen verileri yazdırma veya işleme

if __name__ == '__main__':
    main()
