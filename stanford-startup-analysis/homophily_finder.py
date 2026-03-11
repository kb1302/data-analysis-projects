import pandas as pd
import openpyxl

# Step 1: Read the Excel file
data = pd.read_excel('university (4) (1).xlsx', sheet_name='Data')

# Step 2-8: Adjusted Code
def estimate_years(degree):
    estimation_years = {
        'Bachelors Degree': 4,
        'Masters Degree': 2,
        'Doctors Degree': 5,
        'Associates Degree': 2,
        'MBA': 2
    }
    return estimation_years.get(degree, 0)

def clean_year(year):
    if year in ['??', '?', '']:
        return None
    return int(year)

matches = []
grouped = data.groupby(['UniqueCompanyID', 'CleanUniversity'])

for (_, company_uni), group in grouped:
    match_found = False
    unique_persons = group['UniquePersonID'].unique()
    unique_person_pairs = [(p1, p2) for i, p1 in enumerate(unique_persons) for p2 in unique_persons[i + 1:]]
    
    for person1, person2 in unique_person_pairs:
        person1_data = group[group['UniquePersonID'] == person1].iloc[0]
        person2_data = group[group['UniquePersonID'] == person2].iloc[0]
        
        start1 = clean_year(person1_data['StartUniversity'])
        end1 = clean_year(person1_data['EndUniversity'])
        start2 = clean_year(person2_data['StartUniversity'])
        end2 = clean_year(person2_data['EndUniversity'])
        degree1 = person1_data['BroadDegree']
        degree2 = person2_data['BroadDegree']
        
        if start1 is None and end1 is not None:
            start1 = end1 - estimate_years(degree1)
        elif end1 is None and start1 is not None:
            end1 = start1 + estimate_years(degree1)
        
        if start2 is None and end2 is not None:
            start2 = end2 - estimate_years(degree2)
        elif end2 is None and start2 is not None:
            end2 = start2 + estimate_years(degree2)
        
        if (start1 is not None and end2 is not None and 
            (start1 <= end2 and start2 <= end1)) or (start2 is not None and end1 is not None and 
            (start2 <= end1 and start1 <= end2)):
            clean_university = person1_data['CleanUniversity']
            matches.append((person1_data['UniqueCompanyID'], clean_university))
            matches.append((person2_data['UniqueCompanyID'], clean_university))
            match_found = True
    
    if not match_found:
        matches.append((group.iloc[0]['UniqueCompanyID'], ''))

# Create a DataFrame with the matches
matches_df = pd.DataFrame(matches, columns=['UniqueCompanyID', 'CleanUniversityMatch'])

# Drop duplicate rows
matches_df.drop_duplicates(inplace=True)

# Add 'HomophilyUniDummy' column to data DataFrame
data['HomophilyUniDummy'] = 0

# Combine multiple matches for the same company into one row
combined_matches = matches_df.groupby('UniqueCompanyID')['CleanUniversityMatch'].apply(', '.join).reset_index()

# Merge with the original data to get HomophilyUniDummy
final_df = combined_matches.merge(data[['UniqueCompanyID', 'HomophilyUniDummy']], on='UniqueCompanyID', how='left')

# Adjust HomophilyUniDummy based on CleanUniversityMatch
final_df['HomophilyUniDummy'] = final_df['CleanUniversityMatch'].apply(lambda x: 1 if x else 0)

# Create a new DataFrame to hold unique companies and their matches
unique_companies = final_df.drop_duplicates(subset='UniqueCompanyID', keep='first')

# Further processing to create CleanUniversity column
clean_university_col = []
for _, row in unique_companies.iterrows():
    if row['HomophilyUniDummy'] == 1:
        clean_university_col.append(row['CleanUniversityMatch'])
    else:
        clean_university_col.append('')
unique_companies['CleanUniversity'] = clean_university_col

# Drop unnecessary columns
unique_companies.drop(['CleanUniversityMatch', 'HomophilyUniDummy'], axis=1, inplace=True)

# Get UDummy and RSDummy columns from the original data
udummy_col = []
rsdummy_col = []
for _, row in unique_companies.iterrows():
    company_id = row['UniqueCompanyID']
    first_entry = data[data['UniqueCompanyID'] == company_id].iloc[0]
    udummy_col.append(first_entry['UDummy'])
    rsdummy_col.append(first_entry['RSDummy'])

unique_companies['UDummy'] = udummy_col
unique_companies['RSDummy'] = rsdummy_col

# Save the results to a new Excel file
unique_companies.to_excel('homophily_uni_final.xlsx', index=False)