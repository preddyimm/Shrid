import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopandas.tools import sjoin
from shapely.ops import nearest_points

# Load the data
shrid_with_parks = pd.read_csv('C:/Users/rajes/OneDrive/Documents/Code/sample/sliced_shrd_with_parks.csv')
shrid_centroids = pd.read_csv('C:/Users/rajes/OneDrive/Documents/Code/sample/sliced_shrid_centroids.csv')
shrug_shrid_poly = gpd.read_file('C:/Users/rajes/OneDrive/Documents/Code/files/shrug-shrid-poly-shp.zip').iloc[0:12001]


treated_shrids = shrid_with_parks['shrid2']

# To convert into metric system
shrug_shrid_poly = shrug_shrid_poly.to_crs(epsg=7755)

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

print("printing all_shrids_with_nearest_distances")
print(all_shrids_with_nearest_distances)

# creating a new gdf of treated data with distance parameter for the purpose of calculations
treated_shrids_with_distance = treated_shrids_gdf.copy()
treated_shrids_with_distance['distance'] = 'place_holder_5'

print("printing treated_shrids_with_distance")
print(treated_shrids_with_distance)

#Creating a function to calculate distance from nearest treated shrids for all shrids
def classify_shrids(row_data_single_with_distance_parameter, treated_data_total_with_distance_parameter, distance):
    treated_data_total_with_distance_parameter['distance'] = treated_data_total_with_distance_parameter['geometry'].apply(lambda x: x.distance(row_data_single_with_distance_parameter.geometry))
    
    nearest_treated_row = treated_data_total_with_distance_parameter.loc[treated_data_total_with_distance_parameter['distance'].idxmin()]
    nearest_shrid = nearest_treated_row['shrid2']
    nearest_distance = nearest_treated_row['distance']
    row_data_single_with_distance_parameter['nearest distance'] = nearest_distance
    
    if row_data_single_with_distance_parameter['shrid2'] == nearest_shrid:
        return 'treated'
    else:
        if nearest_distance <= distance:
            return 'contaminator'
        else:
            return 'control'
        
# using the distance to classify the shrids at 10000 meters
final_df['park_status10'] = all_shrids_with_nearest_distances.apply(classify_shrids, axis=1, args=(treated_shrids_with_distance, 10000))
print(final_df[0:10])

# using the distance to classify the shrids at 20000 meters
final_df['park_status20'] = all_shrids_with_nearest_distances.apply(classify_shrids, axis=1, args=(treated_shrids_with_distance, 20000))
print(final_df[0:10])

# using the distance to classify the shrids at 30000 meters
final_df['park_status30'] = all_shrids_with_nearest_distances.apply(classify_shrids, axis=1, args=(treated_shrids_with_distance, 30000))
print(final_df[0:10])