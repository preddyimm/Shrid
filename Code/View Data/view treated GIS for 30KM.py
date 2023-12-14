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

shrug_shrid_poly = shrug_shrid_poly.to_crs(epsg=crs3)

# To check the headings of the data
print('printing shrug_shrid_poly')
print(shrug_shrid_poly.head())

#treated shrids from the polygon data
gdf = shrug_shrid_poly[shrug_shrid_poly['shrid2'].isin(treated_shrids)].copy()
# Assuming your GeoDataFrame is named 'gdf' and is already loaded

# Ensure the GeoDataFrame is in a CRS that uses meters (like UTM)
# Replace 'EPSG:XXXX' with the appropriate UTM zone for your area

# Buffer the polygons by 30,000 meters (which is 30 km)
gdf['buffered'] = gdf.geometry.buffer(10000)

# Plotting
fig, ax = plt.subplots(figsize=(10, 10))

# Plot original polygons
gdf.plot(ax=ax, color='blue', edgecolor='k', alpha=0.5)

# Plot buffered areas
gdf['buffered'].plot(ax=ax, color='green', alpha=0.3)

# You might want to adjust the limits and labels of the plot
ax.set_title("Treated Areas and 30 km Buffer Zones")
plt.show()

