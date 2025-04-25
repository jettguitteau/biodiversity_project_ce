import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import seaborn as sns

observations = pd.read_csv('observations.csv')
species_info = pd.read_csv('species_info.csv')

# View the first few columns of each DataFrame.
print(observations.head())
print(species_info.head())

# View some basic information about each DataFrame. 
print(observations.describe())
print(species_info.describe())

# Count species per category and visualize with bar graph.
print(species_info.category.value_counts())
category_counts = species_info['category'].value_counts()
category_counts.to_excel('category_counts.xlsx', index=True)

plt.figure(figsize=(8, 5))
plt.bar(category_counts.index, category_counts.values, color='teal', edgecolor='black')
plt.title('Number of Species per Category')
plt.xlabel('Category of Species')
plt.ylabel('Number of Different Species')
plt.xticks(rotation=45)
plt.tight_layout()

# Visualizing which categories have the most species with some type of conservation concern. 
species_info['conservation_status'] = species_info['conservation_status'].fillna('No Intervention')

at_risk = species_info[
    (species_info['conservation_status'] != 'In Recovery') & 
    (species_info['conservation_status'] != 'No Intervention')
    ]
at_risk_counts = at_risk['category'].value_counts()
at_risk_counts.to_excel('at_risk_counts.xlsx', index=True)

plt.figure(figsize=(8, 5))
plt.bar(at_risk_counts.index, at_risk_counts.values, color='red', edgecolor='black')
plt.title('Number of At-Risk Species per Category')
plt.xlabel('Category of Species')
plt.ylabel('Number of Different At-Risk Species')
plt.xticks(rotation=30)
plt.tight_layout()

# Create a scatterplot of the total species counts against the at-risk counts. 
total_vs_atrisk_data = pd.DataFrame({
    'total_species': category_counts,
    'at_risk_species': at_risk_counts
}).dropna()
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=total_vs_atrisk_data,
    x='total_species',
    y='at_risk_species',
    hue='category',
    palette='Set2',
    s=100,  
    edgecolor='black'
)
plt.title('Species vs. At-Risk Species per Category')
plt.xlabel('Total Species per Category')
plt.ylabel('At-Risk Species per Category')
plt.legend(title='Category')
plt.tight_layout()
plt.show()

# Determine what percentage of each category of species is at-risk. 
total_species_per_category = species_info['category'].value_counts()
at_risk_species_per_category = at_risk['category'].value_counts()

risk_percentage = (at_risk_species_per_category / total_species_per_category) * 100
sorted_risk_percentage = risk_percentage.sort_values(ascending=False)
sorted_risk_percentage.to_excel('sorted_risk_percentage.xlsx', index=True)

plt.figure(figsize=(8, 5))
plt.bar(sorted_risk_percentage.index, sorted_risk_percentage.values, color='blue', edgecolor='black')
plt.title('Percentage of Each Category of Species At-Risk')
plt.xlabel('Category of Species')
plt.ylabel('Percentage of Category At Some Type of Risk')
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# Statistical Anaylsis 

# Create a contingency table (categories as rows, at-risk and not at-risk as columns)
categories = species_info['category'].unique()
total_species = species_info['category'].value_counts()
at_risk_species = at_risk['category'].value_counts()
non_at_risk_species = total_species - at_risk_species
contingency_table = np.array([at_risk_species, non_at_risk_species])

chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)

print(f"Chi2 Stat: {chi2_stat}")
print(f"P-Value: {p_value:.10f}")
print(f"Degrees of Freedom: {dof}")
print(f"Expected frequencies: \n{expected}")