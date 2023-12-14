import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import matplotlib.pyplot as plt

# Specify the path to your GIS file
file_path = "C:\\Users\\rajes\\OneDrive\\Documents\\Code\\files\\shrug-shrid-poly-shp.zip"
shrid_centroids = pd.read_csv('C:/Users/rajes/OneDrive/Documents/Code/sample/sliced_shrid_centroids.csv')
shrug_shrid_poly = gpd.read_file('C:/Users/rajes/OneDrive/Documents/Code/files/shrug-shrid-poly-shp.zip')
shrid_with_parks = pd.read_csv('C:/Users/rajes/OneDrive/Documents/Code/files/shrid_with_parks_first_park_year_and_id.csv')

treated_shrids = shrid_with_parks['shrid2']

crs1 = 32644
crs2 = 7755
crs3 = 3857

# To convert into metric system
shrug_shrid_poly = shrug_shrid_poly.to_crs(epsg=crs3)

# To check the headings of the data
print('printing shrug_shrid_poly')
print(shrug_shrid_poly.head())

#treated shrids from the polygon data
treated_shrids_gdf = shrug_shrid_poly[shrug_shrid_poly['shrid2'].isin(treated_shrids)]


# Plot the GIS data
treated_shrids_gdf.plot()


# Show the plot
plt.show()
