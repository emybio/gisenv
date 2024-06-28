# GeoTIFF to Leaflet Map Project

This project demonstrates how to convert GeoTIFF files to PNG tiles and display them on a Leaflet map. The project utilizes GDAL for converting GeoTIFF files and Leaflet for displaying the map.

## Prerequisites

1. **GDAL**: Install GDAL for your operating system.
   - **Windows**: Use OSGeo4W installer.
   - **macOS**: Use Homebrew.
   - **Linux**: Use the package manager for your distribution (e.g., apt for Ubuntu).

2. **Python**: Ensure Python is installed on your system.

## Installation

### Windows

1. **Install GDAL**:
   - Download and install OSGeo4W from [OSGeo4W](https://trac.osgeo.org/osgeo4w/).
   - During the installation, select GDAL and other necessary packages.

2. **Add GDAL to PATH**:
   - Open the System Properties dialog (Win + Pause).
   - Go to Advanced system settings > Environment Variables.
   - Find the `Path` variable in the System variables section and click Edit.
   - Add the path to the GDAL `bin` directory (e.g., `C:\OSGeo4W64\bin`).

### macOS

1. **Install GDAL**:
   ```sh
   brew install gdal

## Add GDAL to PATH:
Add the following line to your ~/.bash_profile or ~/.zshrc file:
    export PATH="/usr/local/opt/gdal/bin:$PATH"

#### **Linux**
#### Install GDAL:
    sudo apt-get update
    sudo apt-get install gdal-bin

## Usage
1. Step: Convert GeoTIFF to VRT
Convert a paletted GeoTIFF file to an RGBA VRT file using gdal_translate:

**gdal_translate -of vrt -expand rgba path_to_your_geotiff_file.tif temp.vrt**

2. Step: Generate Tiles from VRT
Generate tiles from the VRT file using gdal2tiles.py:

**gdal2tiles.py -z 0-5 -w none temp.vrt output_directory**

3. Step: Display Tiles on Leaflet Map
Create an HTML file with the following content to display the tiles on a Leaflet map:

        <!DOCTYPE html>
        <html>
        <head>
            <title>Leaflet with PNG Tile Layer</title>
            <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
            <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
            <style>
                #map {
                    height: 600px;
                }
            </style>
        </head>
        <body>
            <div id="map"></div>
            <script>
                var map = L.map('map').setView([0, 0], 2);
        
                // OpenStreetMap tile layer
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 19,
                    attribution: '&copy; OpenStreetMap contributors'
                }).addTo(map);
        
                // Custom PNG tile layer
                L.tileLayer('http://yourserver.com/tiles/{z}/{x}/{y}.png', {
                    maxZoom: 19,
                    attribution: '© Your Attribution'
                }).addTo(map);
        
                map.setView([latitude, longitude], zoomLevel);  // Adjust center and zoom level
            </script>
        </body>
        </html>
Replace http://yourserver.com/tiles/{z}/{x}/{y}.png with the actual URL where your tiles are hosted. Also, adjust latitude, longitude, and zoomLevel according to your requirements.

## Troubleshooting
If you encounter any issues, ensure the following:

GDAL is correctly installed and added to the PATH.
The GeoTIFF file is correctly converted to VRT format.
The tiles are generated and accessible via the specified URL.
## Contributing
If you have any suggestions or improvements, feel free to submit a pull request or open an issue.

## License
This project is licensed under the MIT License.
