# add_gender_to_staff.py
# Script to add gender column to staff-list.csv based on names

import csv
import re
from collections import Counter

# Gambian/West African name patterns for gender prediction
MALE_NAMES = {
    'alhagie', 'alagie', 'lamin', 'momodou', 'ousman', 'ebrima', 'bakary', 'muhammed',
    'omar', 'sainey', 'famara', 'baba', 'kawsu', 'demba', 'yankuba', 'saikou', 'seedy',
    'abdourahman', 'sunkary', 'alkali', 'amadou', 'essa', 'samba', 'paul', 'george',
    'tijan', 'ahmed', 'muhammed', 'mohammed', 'batholeman', 'choi', 'ganyie', 'juwara',
    'suwareh', 'thomas', 'jaw', 'jeng', 'sarr', 'mendy', 'jallow'
}

FEMALE_NAMES = {
    'nenneh', 'neneh', 'binta', 'safiatou', 'fatou', 'awa', 'isatou', 'rabiatou',
    'mama', 'bintou', 'jalika', 'fanta', 'mariama', 'aminata', 'kumba', 'aja',
    'kaddy', 'adama', 'asanna', 'fatoumata', 'hawa', 'sanyang', 'ceesay'
}

def predict_gender(full_name):
    """
    Predict gender based on Gambian/West African name patterns
    Returns: 'Male', 'Female', or 'Unknown'
    """
    if not full_name or full_name.strip() == '':
        return 'Unknown'
    
    # Convert to lowercase and split
    name_parts = full_name.lower().split()
    
    # Check each part of the name
    for part in name_parts:
        # Remove common suffixes/titles
        clean_part = re.sub(r'[^a-z]', '', part)
        
        if clean_part in MALE_NAMES:
            return 'Male'
        if clean_part in FEMALE_NAMES:
            return 'Female'
    
    # Check for common patterns
    name_lower = full_name.lower()
    
    # Check for female indicators
    if any(indicator in name_lower for indicator in ['binta', 'fatou', 'awa', 'isatou', 'neneh']):
        return 'Female'
    
    # Check for male indicators
    if any(indicator in name_lower for indicator in ['lamin', 'ousman', 'momodou', 'ebrima']):
        return 'Male'
    
    return 'Unknown'

def main():
    print("=" * 60)
    print("Adding Gender Column to Staff List")
    print("=" * 60)
    print()
    
    input_file = 'staff-list.csv'
    output_file = 'staff-list-with-gender.csv'
    
    # Read the CSV file
    print(f"Reading {input_file}...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            
            # Check if staff_name column exists
            if 'staff_name' not in fieldnames:
                print("✗ Error: 'staff_name' column not found in the file")
                return
            
            # Add gender to fieldnames if not already there
            if 'gender' not in fieldnames:
                fieldnames = list(fieldnames) + ['gender']
            
            rows = list(reader)
            total_records = len(rows)
            print(f"✓ Loaded {total_records:,} records")
            
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        return
    
    # Add gender column
    print("\nPredicting gender based on names...")
    gender_counts = Counter()
    
    for i, row in enumerate(rows, 1):
        if i % 5000 == 0:
            print(f"  Processed {i:,} / {total_records:,} records...")
        
        staff_name = row.get('staff_name', '')
        gender = predict_gender(staff_name)
        row['gender'] = gender
        gender_counts[gender] += 1
    
    print(f"✓ Processed all {total_records:,} records")
    
    # Show statistics
    print("\nGender Distribution:")
    for gender, count in gender_counts.most_common():
        percentage = (count / total_records) * 100
        print(f"  {gender}: {count:,} ({percentage:.1f}%)")
    
    # Save the updated file
    print(f"\nSaving to {output_file}...")
    try:
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"✓ Successfully saved {total_records:,} records with gender column")
    except Exception as e:
        print(f"✗ Error saving file: {e}")
        return
    
    # Show sample
    print("\nSample records with gender:")
    print(f"{'Staff Name':<30} {'Gender':<10}")
    print("-" * 40)
    for row in rows[:20]:
        print(f"{row.get('staff_name', ''):<30} {row.get('gender', ''):<10}")
    
    # Optionally update original file
    print("\n" + "=" * 60)
    update = input("Do you want to update the original staff-list.csv? (yes/no): ")
    if update.lower() == 'yes':
        with open(input_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print("✓ Original file updated")
    else:
        print(f"Original file unchanged. Updated data saved in {output_file}")

if __name__ == "__main__":
    main()
