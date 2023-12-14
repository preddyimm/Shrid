import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopandas.tools import sjoin
from shapely.ops import nearest_points

# Load the data
shrid_with_parks = pd.read_csv('C:/Users/rajes/OneDrive/Documents/Code/files/shrid_with_parks_first_park_year_and_id.csv')
shrid_centroids = pd.read_csv('C:/Users/rajes/OneDrive/Documents/Code/files/shrid_centroids.csv')
shrug_shrid_poly = gpd.read_file('C:/Users/rajes/OneDrive/Documents/Code/files/shrug-shrid-poly-shp.zip')

print(shrid_centroids)
print(shrid_with_parks)
print(shrug_shrid_poly)

# Slice the dataframe, so that the code runs faster, for 50 treated shrids and 12000 control shrids
sliced_shrid_centroids = shrid_centroids.iloc[0:12001]
sliced_shrd_with_parks = shrid_with_parks.iloc[0:51]
sliced_shrug_shrid_poly = shrug_shrid_poly.iloc[0:12001]

# Save the sliced dataframe to a new CSV file
sliced_shrid_centroids.to_csv('C:/Users/rajes/OneDrive/Documents/Code/sample/sliced_shrid_centroids.csv')
sliced_shrd_with_parks.to_csv('C:/Users/rajes/OneDrive/Documents/Code/sample/sliced_shrd_with_parks.csv')
sliced_shrug_shrid_poly.to_csv('C:/Users/rajes/OneDrive/Documents/Code/sample/sliced_shrug_shrid_poly.csv')