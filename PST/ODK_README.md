# ODK Employee Details Questionnaire

## Files Created

This package contains an ODK (Open Data Kit) form for collecting employee details with 25 questions.

### Files:
1. **employee_odk_form.csv** - Survey questions (main form structure)
2. **employee_odk_choices.csv** - Answer choices for multiple choice questions
3. **employee_odk_settings.csv** - Form metadata and settings
4. **create_odk_xlsform.py** - Python script to convert CSVs to Excel XLSForm

## Form Structure

### Personal Information (5 questions)
- Full Name
- Date of Birth
- Gender (multiple choice)
- Nationality
- Marital Status (multiple choice)

### Contact Information (5 questions)
- Phone Number (validated)
- Email Address (validated)
- Residential Address
- City
- Postal Code

### Emergency Contact (3 questions)
- Emergency Contact Name
- Relationship
- Emergency Contact Phone

### Employment Information (6 questions)
- Employee ID
- Department
- Job Position/Title
- Employment Type (multiple choice: Full-time/Part-time/Contract/Intern)
- Start Date
- Supervisor Name

### Education & Skills (4 questions)
- Highest Level of Education (multiple choice)
- Field of Study
- Professional Certifications (optional)
- Key Skills

### Additional Information (2 questions)
- Previous Employer (optional)
- Total Years of Work Experience

## How to Use

### Option 1: Generate Excel XLSForm (Recommended)
```bash
# Install required packages
pip install pandas openpyxl

# Run the converter
python create_odk_xlsform.py
```
This creates **Employee_Details_ODK_Form.xlsx** ready for ODK.

### Option 2: Use Online Tools
1. Go to [ODK Build](https://build.getodk.org)
2. Import the CSV files manually
3. Download as XForm

### Option 3: Use Command Line Tool
```bash
# Install pyxform
pip install pyxform

# Convert to XForm
xls2xform Employee_Details_ODK_Form.xlsx employee_form.xml
```

## Deploy to ODK

1. **ODK Central**: Upload the .xlsx file directly
2. **ODK Aggregate**: Convert to .xml first, then upload
3. **ODK Collect**: Download form from server on mobile device

## Features

- ✓ Input validation (email, phone numbers)
- ✓ Required/optional field controls
- ✓ Organized into logical sections
- ✓ Multiple choice questions with predefined options
- ✓ Date pickers for date fields
- ✓ Works offline on mobile devices
- ✓ Data exports to CSV/Excel

## Requirements

- **For form creation**: pandas, openpyxl (Python packages)
- **For deployment**: ODK Central or ODK Aggregate server
- **For data collection**: ODK Collect mobile app (Android)
