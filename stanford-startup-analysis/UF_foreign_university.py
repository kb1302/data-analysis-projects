import pandas as pd

# Read the excel file
df = pd.read_excel('university (1).xlsx', sheet_name='Main Data')

# Filter out individuals with '0' in UFounderDummy column
filtered_df = df[df['UFounderDummy'] != 0]

# Filter out 'United States' and '??' from CleanUniversityCountry column for Country Founders table
filtered_countries = filtered_df[filtered_df['CleanUniversityCountry'].isin(['United States', '??']) == False]

# Calculate the number of founders for each country
country_counts = filtered_countries['CleanUniversityCountry'].value_counts().reset_index()
country_counts.columns = ['Country', 'Number of Founders']

# Filter out individuals with '0' in UFounderDummy column and '??' or 'United States' from CleanUniversityCountry column for University Occurrences table
filtered_universities = filtered_df[(filtered_df['CleanUniversityCountry'].isin(['United States', '??']) == False) & (filtered_df['CleanUniversity'] != '??')]

# Calculate the number of occurrences for each university
university_counts = filtered_universities['CleanUniversity'].value_counts().reset_index()
university_counts.columns = ['University', 'Number of Occurrences']

# Create a new Excel file and write the tables to separate sheets
with pd.ExcelWriter('results.xlsx') as writer:
    country_counts.to_excel(writer, sheet_name='Country Founders', index=False)
    university_counts.to_excel(writer, sheet_name='University Occurrences', index=False)
