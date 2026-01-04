# ODK-test.py - Employee Details Questionnaire

def employee_questionnaire():
    print("=" * 50)
    print("EMPLOYEE DETAILS QUESTIONNAIRE")
    print("=" * 50)
    print()
    
    employee_data = {}
    
    # Personal Information
    print("PERSONAL INFORMATION")
    employee_data['full_name'] = input("1. Full Name: ")
    employee_data['date_of_birth'] = input("2. Date of Birth (DD/MM/YYYY): ")
    employee_data['gender'] = input("3. Gender: ")
    employee_data['nationality'] = input("4. Nationality: ")
    employee_data['marital_status'] = input("5. Marital Status: ")
    
    # Contact Information
    print("\nCONTACT INFORMATION")
    employee_data['phone_number'] = input("6. Phone Number: ")
    employee_data['email'] = input("7. Email Address: ")
    employee_data['residential_address'] = input("8. Residential Address: ")
    employee_data['city'] = input("9. City: ")
    employee_data['postal_code'] = input("10. Postal Code: ")
    
    # Emergency Contact
    print("\nEMERGENCY CONTACT")
    employee_data['emergency_contact_name'] = input("11. Emergency Contact Name: ")
    employee_data['emergency_contact_relationship'] = input("12. Relationship: ")
    employee_data['emergency_contact_phone'] = input("13. Emergency Contact Phone: ")
    
    # Employment Information
    print("\nEMPLOYMENT INFORMATION")
    employee_data['employee_id'] = input("14. Employee ID: ")
    employee_data['department'] = input("15. Department: ")
    employee_data['position'] = input("16. Job Position/Title: ")
    employee_data['employment_type'] = input("17. Employment Type (Full-time/Part-time/Contract): ")
    employee_data['start_date'] = input("18. Start Date (DD/MM/YYYY): ")
    employee_data['supervisor_name'] = input("19. Supervisor Name: ")
    
    # Education & Skills
    print("\nEDUCATION & SKILLS")
    employee_data['highest_education'] = input("20. Highest Level of Education: ")
    employee_data['field_of_study'] = input("21. Field of Study: ")
    employee_data['certifications'] = input("22. Professional Certifications (if any): ")
    employee_data['key_skills'] = input("23. Key Skills: ")
    
    # Additional Information
    print("\nADDITIONAL INFORMATION")
    employee_data['previous_employer'] = input("24. Previous Employer (if any): ")
    employee_data['years_of_experience'] = input("25. Total Years of Work Experience: ")
    
    # Display Summary
    print("\n" + "=" * 50)
    print("QUESTIONNAIRE COMPLETED")
    print("=" * 50)
    print("\nEmployee Data Summary:")
    for key, value in employee_data.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    return employee_data

def main():
    employee_data = employee_questionnaire()
    
    # Optionally save to file
    save_option = input("\nWould you like to save this data to a file? (yes/no): ")
    if save_option.lower() == 'yes':
        filename = f"employee_{employee_data.get('employee_id', 'unknown')}.txt"
        with open(filename, 'w') as f:
            for key, value in employee_data.items():
                f.write(f"{key.replace('_', ' ').title()}: {value}\n")
        print(f"\nData saved to {filename}")

if __name__ == "__main__":
    main()
