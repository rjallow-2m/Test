"""
Prepare staff list CSV for ODK form attachment
Extracts only the necessary columns from a source staff list CSV file.

Usage:
    python prepare_staff_list_csv.py <input_csv_file>
    
Example:
    python prepare_staff_list_csv.py ../csv/my_staff_data.csv
"""
import pandas as pd
import sys
import os

def prepare_staff_list(input_file, output_file='../csv/staff_list.csv'):
    """
    Prepare a staff list CSV for ODK form attachment.
    
    Args:
        input_file: Path to the source CSV file containing staff data
        output_file: Path for the output CSV file (default: ../csv/staff_list.csv)
    """
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file not found: {input_file}")
        print(f"   Please provide a valid CSV file with staff data.")
        sys.exit(1)
    
    # Read the full staff list
    staff_df = pd.read_csv(input_file)
    
    # Select only the columns needed for the form
    columns_needed = ['tin', 'eeno', 'staff_name', 'gender', 'organisation', 'job']
    
    # Check if all required columns exist
    missing_cols = [col for col in columns_needed if col not in staff_df.columns]
    if missing_cols:
        print(f"❌ Error: Missing required columns: {missing_cols}")
        print(f"   Available columns: {list(staff_df.columns)}")
        sys.exit(1)
    
    # Create the lookup CSV with only needed columns
    lookup_df = staff_df[columns_needed].copy()
    
    # Remove any rows with missing TIN (can't lookup without TIN)
    lookup_df = lookup_df.dropna(subset=['tin'])
    
    # Remove duplicates based on TIN (keep first occurrence)
    lookup_df = lookup_df.drop_duplicates(subset=['tin'], keep='first')
    
    # Save as staff_list.csv (the name referenced in the form)
    lookup_df.to_csv(output_file, index=False)
    
    print(f"✓ Created {output_file}")
    print(f"  Total records: {len(lookup_df)}")
    print(f"\nColumns included:")
    for col in columns_needed:
        print(f"  - {col}")
    print(f"\nSample data:")
    print(lookup_df.head())
    print("\n✓ This file is ready to be uploaded as a media attachment to the ODK form")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Error: No input file specified.")
        print(__doc__)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else '../csv/staff_list.csv'
    
    prepare_staff_list(input_file, output_file)
