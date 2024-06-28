import rasterio as r
import georasters as gr
import geopandas as gpd


destinationCRS = "EPSG:4326"
sourceCRS = r.open(tif_file).crs.to_epsg()

geoFrame = gr.to_geopandas(gr.from_file(tif_file))

if sourceCRS != destinationCRS:
    geoFrame = geoFrame.to_crs(destinationCRS) 

return geoFrame