from typing import final
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopandas.tools import sjoin
from shapely.ops import nearest_points
import matplotlib.pyplot as plt

# Load the data
shrid_with_parks = pd.read_csv('C:/Users/rajes/OneDrive/Documents/Code/files/shrid_with_parks_first_park_year_and_id.csv')
shrid_centroids = pd.read_csv('C:/Users/rajes/OneDrive/Documents/Code/files/shrid_centroids.csv')[:70001]
shrug_shrid_poly = gpd.read_file('C:/Users/rajes/OneDrive/Documents/Code/files/shrug-shrid-poly-shp.zip')[:70001]


treated_shrids = shrid_with_parks['shrid2']

original_crs = shrug_shrid_poly.crs
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

print("printing treated shrids")
print(treated_shrids_gdf.head())

#creating the final dataframe with all the shrid ids
final_df = shrid_centroids[['shrid2']].copy()

#creating a column for park status by distance
final_df['park_status10'] = 'place_holder_1'
final_df['park_status20'] = 'place_holder_2'
final_df['park_status30'] = 'place_holder_3'

print("printing final_df")
print(final_df)

#creating a new gdf and including distances to its nearest treated park
all_shrids_with_nearest_distances = shrug_shrid_poly.copy()
all_shrids_with_nearest_distances["nearest distance"] = 'place_holder_4'
all_shrids_with_nearest_distances["nearest treated shrid"] = 'place_holder_5'

print("printing all_shrids_with_nearest_distances")
print(all_shrids_with_nearest_distances)

# creating a new gdf of treated data with distance parameter for the purpose of calculations
treated_shrids_with_distance = treated_shrids_gdf.copy()
treated_shrids_with_distance['distance'] = 'place_holder_6'

print("printing treated_shrids_with_distance")
print(treated_shrids_with_distance)

#Creating a function to calculate distance from nearest treated shrids for all shrids
def nearest_treated_distance(row_data_single_with_distance_parameter, treated_data_total_with_distance_parameter):
    treated_data_total_with_distance_parameter['distance'] = treated_data_total_with_distance_parameter['geometry'].apply(lambda x: x.distance(row_data_single_with_distance_parameter.geometry))
    
    nearest_treated_row = treated_data_total_with_distance_parameter.loc[treated_data_total_with_distance_parameter['distance'].idxmin()]
    nearest_shrid = nearest_treated_row['shrid2']
    nearest_distance = nearest_treated_row['distance']
    row_data_single_with_distance_parameter['nearest distance'] = nearest_distance
    row_data_single_with_distance_parameter['nearest treated shrid'] = nearest_shrid
    return row_data_single_with_distance_parameter

#Adding distance to all shrids
all_shrids_with_nearest_distances = all_shrids_with_nearest_distances.apply(nearest_treated_distance, axis=1, args=(treated_shrids_with_distance, ))

print("printing all_shrids_with_nearest_distances")
print(all_shrids_with_nearest_distances)

#Creating a function to classify shrids based on distance
def classify_shrids(row_data_single_with_distance_parameter, distance):
    nearest_distance = row_data_single_with_distance_parameter['nearest distance']
    if row_data_single_with_distance_parameter['shrid2'] == row_data_single_with_distance_parameter['nearest treated shrid']:
        return 'treated'
    elif nearest_distance <= distance:
        return 'contaminator'
    else:
        return 'control'
    
# using the distance to classify the shrids
final_df['park_status10'] = all_shrids_with_nearest_distances.apply(classify_shrids, axis=1, args=(10000,))
final_df['park_status20'] = all_shrids_with_nearest_distances.apply(classify_shrids, axis=1, args=(20000,))
final_df['park_status30'] = all_shrids_with_nearest_distances.apply(classify_shrids, axis=1, args=(30000,))
    
print(final_df)

final_df.to_csv('C:/Users/rajes/OneDrive/Documents/Code/Output/final_df_70000_sample.csv', index=False)

final_gdf = shrug_shrid_poly[shrug_shrid_poly['shrid2'].isin(final_df['shrid2'])].to_crs(original_crs)

final_gdf.plot()
plt.show()
