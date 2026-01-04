# upload_to_odk_central.py
# Script to upload XLSForm to ODK Central

import requests
import json
from getpass import getpass
import os

def upload_to_odk_central():
    """Upload XLSForm to ODK Central"""
    
    print("=" * 60)
    print("ODK Central Form Upload")
    print("=" * 60)
    print()
    
    # Get ODK Central credentials
    print("Enter your ODK Central details:")
    server_url = input("Server URL (e.g., https://your-server.getodk.cloud): ").strip()
    if not server_url.startswith('http'):
        server_url = 'https://' + server_url
    
    # Remove trailing slash if present
    server_url = server_url.rstrip('/')
    
    email = input("Email: ").strip()
    password = getpass("Password: ")
    project_id = input("Project ID (numeric): ").strip()
    
    # XLSForm file
    xlsform_file = 'Employee_Details_ODK_Form.xlsx'
    
    if not os.path.exists(xlsform_file):
        print(f"\n✗ Error: {xlsform_file} not found!")
        print("Please run 'python create_odk_xlsform.py' first.")
        return False
    
    try:
        # Step 1: Authenticate and get session token
        print("\n[1/4] Authenticating...")
        auth_url = f"{server_url}/v1/sessions"
        auth_data = {
            "email": email,
            "password": password
        }
        
        auth_response = requests.post(auth_url, json=auth_data)
        
        if auth_response.status_code != 200:
            print(f"✗ Authentication failed: {auth_response.status_code}")
            print(f"Response: {auth_response.text}")
            return False
        
        token = auth_response.json()['token']
        headers = {
            'Authorization': f'Bearer {token}'
        }
        print("✓ Authentication successful")
        
        # Step 2: Check if form already exists
        print("\n[2/4] Checking existing forms...")
        form_id = 'employee_details_v1'
        
        check_url = f"{server_url}/v1/projects/{project_id}/forms/{form_id}"
        check_response = requests.get(check_url, headers=headers)
        
        form_exists = check_response.status_code == 200
        
        if form_exists:
            print(f"⚠ Form '{form_id}' already exists")
            update = input("Do you want to create a new version? (yes/no): ").lower()
            if update != 'yes':
                print("Upload cancelled.")
                return False
        
        # Step 3: Upload the XLSForm
        print(f"\n[3/4] Uploading form...")
        
        if form_exists:
            # Create new draft for existing form
            draft_url = f"{server_url}/v1/projects/{project_id}/forms/{form_id}/draft"
            upload_url = f"{draft_url}"
            method = 'post'
        else:
            # Create new form
            upload_url = f"{server_url}/v1/projects/{project_id}/forms"
            method = 'post'
        
        # Upload file
        with open(xlsform_file, 'rb') as f:
            files = {
                'xlsx': (xlsform_file, f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            }
            
            headers_upload = headers.copy()
            headers_upload['X-XlsForm-FormId-Fallback'] = form_id
            
            if method == 'post':
                upload_response = requests.post(upload_url, headers=headers_upload, files=files)
            else:
                upload_response = requests.put(upload_url, headers=headers_upload, files=files)
        
        if upload_response.status_code not in [200, 201]:
            print(f"✗ Upload failed: {upload_response.status_code}")
            print(f"Response: {upload_response.text}")
            return False
        
        print("✓ Form uploaded successfully")
        
        # Step 4: Publish the draft (if it's an update)
        if form_exists:
            print("\n[4/4] Publishing draft...")
            publish_url = f"{server_url}/v1/projects/{project_id}/forms/{form_id}/draft/publish"
            publish_response = requests.post(publish_url, headers=headers)
            
            if publish_response.status_code != 200:
                print(f"⚠ Warning: Failed to publish draft: {publish_response.status_code}")
                print(f"Response: {publish_response.text}")
                print("You may need to publish it manually from ODK Central web interface.")
            else:
                print("✓ Form published successfully")
        else:
            print("\n[4/4] Form created (no publishing needed)")
        
        print("\n" + "=" * 60)
        print("✓ SUCCESS: Form uploaded to ODK Central!")
        print("=" * 60)
        print(f"\nForm ID: {form_id}")
        print(f"Access at: {server_url}/v1/projects/{project_id}")
        print("\nNext steps:")
        print("1. Configure form settings in ODK Central web interface")
        print("2. Set up app users if needed")
        print("3. Download form to ODK Collect mobile app")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print(f"\n✗ Error: Cannot connect to {server_url}")
        print("Please check:")
        print("  - Server URL is correct")
        print("  - You have internet connection")
        print("  - Server is online")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False

def main():
    try:
        upload_to_odk_central()
    except KeyboardInterrupt:
        print("\n\nUpload cancelled by user.")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")

if __name__ == "__main__":
    main()
