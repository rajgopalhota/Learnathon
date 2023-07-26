import pandas as pd

# Read the first Excel file
data1 = pd.read_excel('output_fileatt1.xlsx')

# Read the second Excel file
data2 = pd.read_excel('output_fileatt2.xlsx')

# Merge the two data frames on the 'student' column
data_merged = pd.merge(data1, data2, on='student', how='outer')

# Fill missing values with 0
data_merged = data_merged.fillna(0)

# Select the columns to keep
columns_to_keep = ['student', 'session_1','session_2', 'session_3', 'session_4', 'session_5']
data_merged = data_merged[columns_to_keep]

# Write the new data frame to an Excel file
data_merged.to_excel('finalatt.xlsx', index=False)
