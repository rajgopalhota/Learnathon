import pandas as pd

# Read the Excel file
data = pd.read_excel('att2.xlsx')

# Pivot the data frame to create a new data frame with sessions as columns
data_pivot = data.pivot(index='student', columns='session', values='status')

# Rename the columns
data_pivot.columns = ['session_3', 'session_4', 'session_5']

# Reset the index
data_pivot = data_pivot.reset_index()

# Write the new data frame to an Excel file
data_pivot.to_excel('output_fileatt2.xlsx', index=False)
