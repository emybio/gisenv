import os


#kmz_folder = os.path.join(BASE_DIR, 'static/kmz')
print("Available KMZ files:")
for f in os.listdir("D:/Projeler/gisenv/water_wells/static/kmz"):
        print(f)
        
# kmz_folder = os.path.join(settings.BASE_DIR, 'static/kmz')
# kmz_files = [f for f in os.listdir(kmz_folder) if f.endswith('.kmz')]
# kml_data_list = []

# for kmz_file in kmz_files:
#         kmz_path = os.path.join(kmz_folder, kmz_file)
#         try:
#             with zipfile.ZipFile(kmz_path, 'r') as kmz:
#                 kml_filename = [name for name in kmz.namelist() if name.endswith('.kml')]
#                 print(f"Found KML files in {kmz_file}: {kml_filename}")
#         except zipfile.BadZipFile:
#             print(f"Error: {kmz_file} is not a valid KMZ file.")
