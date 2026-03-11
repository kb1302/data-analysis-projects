import pandas as pd

# Step 1: Read university (1).xlsx
df = pd.read_excel('university (1).xlsx', sheet_name='Main Data')

# Step 2: Filter column 'BroadDegree' by 'Bachelors Degree'
filtered_df = df[df['BroadDegree'] == 'Bachelors Degree']

# Step 3: Find multiples of UniqueCompanyID
duplicate_ids = filtered_df[filtered_df.duplicated(['UniqueCompanyID'], keep=False)]

# Step 4: Check CleanUniversity for duplicate UniqueCompanyIDs
duplicate_universities = duplicate_ids[duplicate_ids.duplicated(['UniqueCompanyID', 'CleanUniversity'], keep='first')]

# Step 5: Delete all duplicate entries with the same CleanUniversity and UniqueCompanyID
filtered_df.drop_duplicates(subset=['UniqueCompanyID', 'CleanUniversity'], keep='first', inplace=True)

# Step 6: Count the total number of entries for each CleanUniversity
grouped_df = filtered_df.groupby('CleanUniversity').agg({'UniqueCompanyID': 'count', 'UFounderDummy': 'sum', 'RSFounderDummy': 'sum'})

# Step 7: Separate the count based on UFounderDummy and RSFounderDummy
grouped_df['Unicorns'] = grouped_df['UFounderDummy']
grouped_df['RS'] = grouped_df['RSFounderDummy']

# Step 8: Save the results to a new excel file
results_df = grouped_df[['Unicorns', 'RS']].reset_index()
results_df.columns = ['CleanUniversity', 'Unicorns', 'RS']
results_df.to_excel('results.xlsx', index=False)
