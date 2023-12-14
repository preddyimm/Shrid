# from numpy import number
import pandas as pd
import geopandas as gpd
# from shapely.geometry import Point
# from geopandas.tools import sjoin
# from shapely.ops import nearest_points
import matplotlib.pyplot as plt

# import the data
shrid_with_parks = pd.read_csv('C:/Users/rajes/OneDrive/Documents/Code/files/shrid_with_parks_first_park_year_and_id.csv')
shrid_centroids = pd.read_csv('C:/Users/rajes/OneDrive/Documents/Code/files/shrid_centroids.csv')
shrug_shrid_poly = gpd.read_file('C:/Users/rajes/OneDrive/Documents/Code/files/shrug-shrid-poly-shp.zip')

treated_shrids = shrid_with_parks['shrid2']
total_number_of_shrids = len(shrug_shrid_poly)

# Number of shrids per slice
slice = 20000

#Creating a function to classify shrids based on distance
def classify_shrids(row_data_single_with_distance_parameter, distance):
    nearest_distance = row_data_single_with_distance_parameter['nearest distance']
    if row_data_single_with_distance_parameter['shrid2'] in list(treated_shrids):
        return 'treated'
    elif nearest_distance <= distance:
        return 'contaminator'
    else:
        return 'control'

# To check the headings of the data
print('printing shrug_shrid_poly')
print(shrug_shrid_poly.head())

#treated shrids from the polygon data
treated_shrids_gdf = shrug_shrid_poly[shrug_shrid_poly['shrid2'].isin(treated_shrids)]

print("printing treated shrids")
print(treated_shrids_gdf.head())

final_df = shrid_centroids[['shrid2']].copy()

#creating a column for park status by distance
final_df['park_status10'] = 'place_holder_1'
final_df['park_status20'] = 'place_holder_2'
final_df['park_status30'] = 'place_holder_3'

print("printing final_df")
print(final_df)

#Deciding crs for converting latitude and longitude to metric system.
original_crs = shrug_shrid_poly.crs
crs1 = 32644
crs2 = 7755
crs3 = 3857
crs4 = 4326

# To convert into metric system and choosing crs3
shrug_shrid_poly = shrug_shrid_poly.to_crs(epsg=crs3)

# creating polygon gdf for treated shrids from shrug_shrid_poly
treated_shrids_gdf = shrug_shrid_poly[shrug_shrid_poly['shrid2'].isin(treated_shrids)].copy()
count = 0

for i in range(0, total_number_of_shrids, slice):
    count = count + 1 
    print(count)
    #creating samples of size 'slice'
    shrug_shrid_poly_sample = shrug_shrid_poly[i:i+slice].copy()
    treated_shrids_sample_gdf = shrug_shrid_poly_sample[shrug_shrid_poly_sample['shrid2'].isin(treated_shrids)].copy()
    
    #calculating distance from each shrid to the combined structure of treated shrids using unary_union
    sample_shrids_with_nearest_distances = shrug_shrid_poly[i:i + slice].copy()
    sample_shrids_with_nearest_distances["nearest distance"] = sample_shrids_with_nearest_distances['geometry'].apply(lambda x: x.distance(treated_shrids_sample_gdf.unary_union))
    
    #Applying the classify function and adding it to the final_df
    final_df.loc[i:i + slice, 'park_status10'] = sample_shrids_with_nearest_distances.apply(classify_shrids, axis=1, args=(10000,))
    final_df.loc[i:i + slice, 'park_status20'] = sample_shrids_with_nearest_distances.apply(classify_shrids, axis=1, args=(20000,))
    final_df.loc[i:i + slice, 'park_status30'] = sample_shrids_with_nearest_distances.apply(classify_shrids, axis=1, args=(30000,))
    
    print("printing " + str(i) + " : " + str(i + slice))
    print(final_df[i:i + slice])
    
    #convering the added data to a gdf so as to plot
    x = shrug_shrid_poly[shrug_shrid_poly['shrid2'].isin(final_df[i:i + slice]['shrid2'])].to_crs(original_crs)
    x.plot()
    plt.show()


print(final_df)

#Creating a csv final for for the classified shrids
final_df.to_csv('C:/Users/rajes/OneDrive/Documents/Code/Output/Last_20K_slice_df.csv', index=False)

#final_gdf = shrug_shrid_poly[shrug_shrid_poly['shrid2'].isin(final_df['shrid2'])].to_crs(original_crs)

#final_gdf.plot()

#plt.show()

