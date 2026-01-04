# create_odk_xlsform.py
# Script to convert CSV files to Excel XLSForm for ODK

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
import os

def create_xlsform():
    """Create an Excel XLSForm from CSV files for ODK"""
    
    try:
        # Read CSV files
        survey_df = pd.read_csv('employee_odk_form.csv')
        choices_df = pd.read_csv('employee_odk_choices.csv')
        settings_df = pd.read_csv('employee_odk_settings.csv')
        
        # Create Excel writer
        output_file = 'Employee_Details_ODK_Form.xlsx'
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Write each sheet
            survey_df.to_excel(writer, sheet_name='survey', index=False)
            choices_df.to_excel(writer, sheet_name='choices', index=False)
            settings_df.to_excel(writer, sheet_name='settings', index=False)
            
            # Format the workbook
            workbook = writer.book
            
            # Format each sheet
            for sheet_name in ['survey', 'choices', 'settings']:
                sheet = workbook[sheet_name]
                
                # Style header row
                header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
                header_font = Font(bold=True, color='FFFFFF')
                
                for cell in sheet[1]:
                    cell.fill = header_fill
                    cell.font = header_font
                
                # Auto-adjust column widths
                for column in sheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    sheet.column_dimensions[column_letter].width = adjusted_width
        
        print(f"✓ Successfully created {output_file}")
        print(f"\nNext steps:")
        print("1. Open the Excel file to review the form")
        print("2. Upload to ODK Central or convert to XForm using:")
        print("   - ODK Build (https://build.getodk.org)")
        print("   - pyxform: 'xls2xform Employee_Details_ODK_Form.xlsx form.xml'")
        print("3. Deploy to ODK Collect mobile app")
        
        return output_file
        
    except ImportError as e:
        print("Error: Required packages not installed.")
        print("\nPlease install required packages:")
        print("  pip install pandas openpyxl")
        return None
    except Exception as e:
        print(f"Error creating XLSForm: {e}")
        return None

def main():
    print("=" * 60)
    print("ODK XLSForm Generator - Employee Details Questionnaire")
    print("=" * 60)
    print()
    
    # Check if CSV files exist
    required_files = [
        'employee_odk_form.csv',
        'employee_odk_choices.csv', 
        'employee_odk_settings.csv'
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print("Error: Missing required CSV files:")
        for f in missing_files:
            print(f"  - {f}")
        return
    
    # Create the XLSForm
    create_xlsform()

if __name__ == "__main__":
    main()
