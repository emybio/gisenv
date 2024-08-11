import json
import requests
import time

# Belirtilen bounds bilgileri
ADANA_BOUNDS = {'lat_min': 34.045, 'lat_max': 37.385, 'lon_min': 36.317, 'lon_max': 38.684}
MERSIN_BOUNDS = {'lat_min': 32.152, 'lat_max': 35.522, 'lon_min': 35.497, 'lon_max': 37.882}
HATAY_BOUNDS = {'lat_min': 35.098, 'lat_max': 37.268, 'lon_min': 35.667, 'lon_max': 37.205}
OSMANIYE_BOUNDS = {'lat_min': 35.644, 'lat_max': 37.04, 'lon_min': 36.808, 'lon_max': 37.797}

BOUNDS_LIST = [ADANA_BOUNDS]

def fetch_parcel_info(lat, lon, retries=3):
    url = f'https://cbsapi.tkgm.gov.tr/megsiswebapi.v3.1/api/parsel/{lat}/{lon}/'
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)  # 10 saniyelik zaman aşımı
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}, retrying in {2 ** attempt} seconds...")
            time.sleep(2 ** attempt)  # Backoff stratejisi
    return None

def generate_grid(lat_min, lat_max, lon_min, lon_max, step=0.001):
    lat_range = list(range(int(lat_min * 1000), int(lat_max * 1000), int(step * 1000)))
    lon_range = list(range(int(lon_min * 1000), int(lon_max * 1000), int(step * 1000)))
    
    grid_points = [(lon / 1000.0, lat / 1000.0) for lat in lat_range for lon in lon_range]
    
    return grid_points

def main():
    all_data = []
    step_size = 0.001  # 100 metrelik adımlar

    for bounds in BOUNDS_LIST:
        grid_points = generate_grid(bounds['lat_min'], bounds['lat_max'], bounds['lon_min'], bounds['lon_max'], step=step_size)
        for point in grid_points:
            lat, lon = point
            parcel_info = fetch_parcel_info(lat, lon)
            if parcel_info:
                feature = {
                    "type": "Feature",
                    "geometry": parcel_info["geometry"],
                    "properties": parcel_info["properties"]
                }
                all_data.append(feature)

            # API sınırlamalarına dikkat ederek her 50 istekte bir bekleme süresi ekleyelim
            if len(all_data) % 50 == 0:
                print("Sleeping for 10 seconds to avoid API rate limits...")
                time.sleep(10)

    # Sonuçları kaydetme
    feature_collection = {
        "type": "FeatureCollection",
        "features": all_data
    }

    output_file_path = 'staticfiles/json/complete_parsel_data_bounds.json'
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(feature_collection, output_file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
