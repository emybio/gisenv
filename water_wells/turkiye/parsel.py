import requests
import random,django,time
import json
from django.conf import settings
import os

# JSON dosyasını yükleme
def load_bounds_from_json(filename):
    file_path="C:/Users/kur06/Documents/GitHub/gisenv/water_wells/static/json/"+ filename
    with open(file_path, 'r') as file:
        bounds_data = json.load(file)
    return bounds_data

    
def is_point_in_polygon(point, polygon):
    x, y = point
    inside = False
    n = len(polygon)
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def fetch_parcel_info(lat, lon, retries=3):
    url = f'https://cbsapi.tkgm.gov.tr/megsiswebapi.v3.1/api/parsel/{lat}/{lon}/'
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)  # 10 saniyelik zaman aşımı
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            time.sleep(2 ** attempt)  # Backoff stratejisi
    return None

def get_random_point_within_polygon(polygon):
    min_lat = min([point[1] for point in polygon])
    max_lat = max([point[1] for point in polygon])
    min_lon = min([point[0] for point in polygon])
    max_lon = max([point[0] for point in polygon])

    while True:
        random_point = (random.uniform(min_lon, max_lon), random.uniform(min_lat, max_lat))
        if is_point_in_polygon(random_point, polygon):
            return random_point

def format_parcel_info(parcel_info):
    # Geri dönen parsel bilgilerini belirli formatta yeniden düzenleyin
    return {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                parcel_info.get('geometry', {}).get('coordinates', [[]])
            ]
        },
        "properties": {
            "ilceAd": parcel_info.get('properties', {}).get('ilceAd', ''),
            "mevkii": parcel_info.get('properties', {}).get('mevkii', ''),
            "ilId": parcel_info.get('properties', {}).get('ilId', ''),
            "durum": parcel_info.get('properties', {}).get('durum', ''),
            "ilceId": parcel_info.get('properties', {}).get('ilceId', ''),
            "zeminKmdurum": parcel_info.get('properties', {}).get('zeminKmdurum', ''),
            "parselNo": parcel_info.get('properties', {}).get('parselNo', ''),
            "mahalleAd": parcel_info.get('properties', {}).get('mahalleAd', ''),
            "ozet": parcel_info.get('properties', {}).get('ozet', ''),
            "gittigiParselListe": parcel_info.get('properties', {}).get('gittigiParselListe', ''),
            "gittigiParselSebep": parcel_info.get('properties', {}).get('gittigiParselSebep', ''),
            "alan": parcel_info.get('properties', {}).get('alan', ''),
            "adaNo": parcel_info.get('properties', {}).get('adaNo', ''),
            "nitelik": parcel_info.get('properties', {}).get('nitelik', ''),
            "ilAd": parcel_info.get('properties', {}).get('ilAd', ''),
            "mahalleId": parcel_info.get('properties', {}).get('mahalleId', ''),
            "pafta": parcel_info.get('properties', {}).get('pafta', '')
        }
    }

def main():
    bounds_data = load_bounds_from_json('bounds.json')
    all_data = []
    
    max_requests = 1000  # Maksimum istek sayısı
    request_count = 0

    for region, data in bounds_data.items():
        coordinates = data.get('geometry', {}).get('coordinates', [])
        for coord_list in coordinates:
            for _ in range(100):  # Her çokgende 100 rastgele nokta test et
                if request_count >= max_requests:
                    print("Maximum request limit reached.")
                    return
                
                point = get_random_point_within_polygon(coord_list)
                lat, lon = point
                parcel_info = fetch_parcel_info(lat, lon)
                if parcel_info:
                    formatted_info = format_parcel_info(parcel_info)
                    all_data.append({
                        'region': region,
                        'latitude': lat,
                        'longitude': lon,
                        'data': formatted_info
                    })
                
                request_count += 1
                time.sleep(0.1)  # Her isteğin arasında 0.1 saniye bekle

    with open('parsel_data.json', 'w') as file:
        json.dump(all_data, file, indent=4)

if __name__ == '__main__':
    main()