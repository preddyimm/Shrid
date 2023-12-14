import geopandas as gpd
import pandas as pd

# Load the CSV files
shrid_centroids = pd.read_csv('C:/Users/rajes/OneDrive/Documents/Code/files/shrid_centroids.csv')
shrid_with_parks = pd.read_csv('C:/Users/rajes/OneDrive/Documents/Code/files/shrid_with_parks_first_park_year_and_id.csv')

# Load the shapefile using geopandas
shrid_shapefile = gpd.read_file('C:/Users/rajes/OneDrive/Documents/Code/shrug-shrid-poly-shp/shrid2_open.shp')

# Print the first 5 rows of each
print(shrid_centroids.head(), shrid_with_parks.head(), shrid_shapefile.head())
