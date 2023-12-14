# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 12:30:27 2023

@author: rajes
"""

import pandas as pd

# Paths to the CSV files
csv_file1 = 'C:/Users/rajes/OneDrive/Documents/Code/Output/Last_20K_slice_df.csv'
csv_file2 = 'C:/Users/rajes/OneDrive/Documents/Code/Output/Last_15K_slice_df.csv'
csv_file3 = 'C:/Users/rajes/OneDrive/Documents/Code/Output/Last_10K_slice_df.csv'
csv_file4 = 'C:/Users/rajes/OneDrive/Documents/Code/Output/Last_5K_slice_df.csv'

# Read the CSV files into DataFrames
df1 = pd.read_csv(csv_file1)
df2 = pd.read_csv(csv_file3)
#df3 = pd.read_csv(csv_file3)

# Ensure the DataFrames have the same structure
# This step may vary depending on your data and what you consider as 'difference'
df2 = df2[df1.columns]

# Find the differences
# This will show rows that are different. The approach may vary based on your specific needs.
differences = df1[(df1 != df2)]

# Drop rows that are completely null (no differences)
differences.dropna(how='all', inplace=True)

# Print or output the differences
print(differences)
