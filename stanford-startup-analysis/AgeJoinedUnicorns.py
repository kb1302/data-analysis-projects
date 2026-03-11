import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the Excel file
df = pd.read_excel('founder.xlsx', sheet_name='Data')

# Extract the age column
age_column = 'AgeJoinedUNI'
ages = df[age_column]

# Remove rows with empty or invalid values
ages = ages.dropna()  # Remove empty cells
ages = ages[~ages.astype(str).str.contains('[?]+')]  # Remove rows with question marks

# Create a histogram
plt.hist(ages, bins='auto', edgecolor='black')

# Calculate mean age
mean_age = ages.mean()

# Add mean line
plt.axvline(x=mean_age, color='r', linestyle='--', label='Mean Age')

# Add frequency labels to the bars
hist, bin_edges = np.histogram(ages, bins='auto')
for i in range(len(hist)):
    if hist[i] > 0:
        plt.text(bin_edges[i], hist[i], str(hist[i]), ha='center', va='bottom')

# Set labels and title
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.title('Age Distribution of Founders when their Companies became Unicorns')

# Add legend
plt.legend()

# Display the histogram
plt.show()
