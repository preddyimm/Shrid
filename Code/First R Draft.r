library(dplyr)
library(sf)
library(ggplot2)
library(readr)

# Read the data
shrid_with_parks <- read_csv('C:\\Users\\rajes\\OneDrive\\Documents\\Code\\files\\shrid_with_parks_first_park_year_and_id.csv')
shrid_centroids <- read_csv('C:\\Users\\rajes\\OneDrive\\Documents\\Code\\files\\shrid_centroids.csv')
shrug_shrid_poly <- st_read('C:\\Users\\rajes\\OneDrive\\Documents\\Code\\files\\shrug-shrid-poly-shp.zip')

treated_shrids <- shrid_with_parks$shrid2
total_number_of_shrids <- nrow(shrug_shrid_poly)

# Number of shrids per slice
slice <- 5000

# Function to classify shrids based on distance
classify_shrids <- function(row_data_single_with_distance_parameter, distance) {
  nearest_distance <- row_data_single_with_distance_parameter$nearest_distance
  if(row_data_single_with_distance_parameter$shrid2 %in% treated_shrids) {
    return('treated')
  } else if(nearest_distance <= distance) {
    return('contaminator')
  } else {
    return('control')
  }
}

# Print the head of shrug_shrid_poly
print(head(shrug_shrid_poly))

# Treated shrids from the polygon data
treated_shrids_gdf <- shrug_shrid_poly[shrug_shrid_poly$shrid2 %in% treated_shrids, ]

print(head(treated_shrids_gdf))

final_df <- shrid_centroids %>% select(shrid2) %>% mutate(
  park_status10 = 'place_holder_1',
  park_status20 = 'place_holder_2',
  park_status30 = 'place_holder_3'
)

print(head(final_df))

# Deciding CRS for converting latitude and longitude to metric system
crs3 <- 3857

# Convert into metric system using crs3
shrug_shrid_poly <- st_transform(shrug_shrid_poly, crs3)

count <- 0

for (i in seq(1, total_number_of_shrids, by = slice)) {
  count <- count + 1
  print(count)
  
  # Creating samples of size 'slice'
  shrug_shrid_poly_sample <- shrug_shrid_poly[i:min(i + slice - 1, nrow(shrug_shrid_poly)), ]
  
  # Calculating distance
  sample_shrids_with_nearest_distances <- shrug_shrid_poly_sample
  sample_shrids_with_nearest_distances$nearest_distance <- st_distance(sample_shrids_with_nearest_distances$geometry, st_union(shrug_shrid_poly_sample$geometry), by_element = TRUE)
  
  # Applying the classify function and adding it to final_df
  final_df[i:min(i + slice - 1, nrow(final_df)), 'park_status10'] <- apply(sample_shrids_with_nearest_distances, 1, classify_shrids, distance = 10000)
  final_df[i:min(i + slice - 1, nrow(final_df)), 'park_status20'] <- apply(sample_shrids_with_nearest_distances, 1, classify_shrids, distance = 20000)
  final_df[i:min(i + slice - 1, nrow(final_df)), 'park_status30'] <- apply(sample_shrids_with_nearest_distances, 1, classify_shrids, distance = 30000)
  
  print(final_df[i:min(i + slice - 1, nrow(final_df)), ])
}

# Save the final dataframe to CSV
write_csv(final_df, 'C:/Users/rajes/OneDrive/Documents/Code/Output/Last_5K_slice_from_R_df.csv')

# Uncomment below lines for plotting using ggplot2
# final_gdf <- st_transform(shrug_shrid_poly[shrug_shrid_poly$shrid2 %in% final_df$shrid2, ], original_crs)
# ggplot(final_gdf) + geom_sf()
