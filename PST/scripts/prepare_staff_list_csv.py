"""
Prepare staff list CSV for ODK form attachment
Extracts only the necessary columns from staff-list-with-gender.csv
"""
import pandas as pd

# Read the full staff list
staff_df = pd.read_csv('../csv/staff-list-with-gender.csv')

# Select only the columns needed for the form
columns_needed = ['tin', 'eeno', 'staff_name', 'gender', 'organisation', 'job']

# Create the lookup CSV with only needed columns
lookup_df = staff_df[columns_needed].copy()

# Remove any rows with missing TIN (can't lookup without TIN)
lookup_df = lookup_df.dropna(subset=['tin'])

# Remove duplicates based on TIN (keep first occurrence)
lookup_df = lookup_df.drop_duplicates(subset=['tin'], keep='first')

# Save as staff_list.csv (the name referenced in the form)
output_file = '../csv/staff_list.csv'
lookup_df.to_csv(output_file, index=False)

print(f"✓ Created {output_file}")
print(f"  Total records: {len(lookup_df)}")
print(f"\nColumns included:")
for col in columns_needed:
    print(f"  - {col}")
print(f"\nSample data:")
print(lookup_df.head())
print("\n✓ This file is ready to be uploaded as a media attachment to the ODK form")
