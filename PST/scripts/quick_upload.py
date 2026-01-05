# quick_upload.py
# Quick upload to ODK Central using saved config

import requests
import os
from upload_config import ODK_CONFIG

def quick_upload():
    """Upload XLSForm to ODK Central using saved configuration"""
    
    print("=" * 60)
    print("ODK Central Form Upload")
    print("=" * 60)
    print()
    
    # Get config
    server_url = ODK_CONFIG['server_url'].rstrip('/')
    email = ODK_CONFIG['email']
    password = ODK_CONFIG['password']
    project_id = ODK_CONFIG['project_id']
    xlsform_file = ODK_CONFIG['xlsform_file']
    
    print(f"Server: {server_url}")
    print(f"Email: {email}")
    print(f"Project ID: {project_id}")
    print(f"Form file: {xlsform_file}")
    print()
    
    if not os.path.exists(xlsform_file):
        print(f"✗ Error: {xlsform_file} not found!")
        return False
    
    try:
        # Step 1: Authenticate
        print("[1/4] Authenticating...")
        auth_url = f"{server_url}/v1/sessions"
        print(f"Auth URL: {auth_url}")
        auth_data = {
            "email": email,
            "password": password
        }
        
        print("Sending authentication request...")
        try:
            auth_response = requests.post(auth_url, json=auth_data, timeout=10, verify=True)
            print(f"Auth response status: {auth_response.status_code}")
        except requests.exceptions.Timeout:
            print("✗ Request timed out - server may be slow or unresponsive")
            return False
        except requests.exceptions.SSLError as e:
            print(f"✗ SSL Error: {e}")
            print("You may need to update certificates or use verify=False (not recommended)")
            return False
        
        if auth_response.status_code != 200:
            print(f"✗ Authentication failed: {auth_response.status_code}")
            print(f"Response: {auth_response.text}")
            return False
        
        token = auth_response.json()['token']
        headers = {
            'Authorization': f'Bearer {token}'
        }
        print("✓ Authentication successful")
        
        # Step 2: Check if form exists
        print("\n[2/4] Checking existing forms...")
        form_id = 'employee_details_v1'
        
        check_url = f"{server_url}/v1/projects/{project_id}/forms/{form_id}"
        check_response = requests.get(check_url, headers=headers)
        
        form_exists = check_response.status_code == 200
        
        if form_exists:
            print(f"⚠ Form '{form_id}' already exists - will create new version")
        else:
            print(f"Creating new form '{form_id}'")
        
        # Step 3: Upload the XLSForm
        print(f"\n[3/4] Uploading form...")
        
        with open(xlsform_file, 'rb') as f:
            files = {
                'xlsx': (xlsform_file, f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            }
            
            headers_upload = headers.copy()
            headers_upload['X-XlsForm-FormId-Fallback'] = form_id
            
            if form_exists:
                # Create draft for existing form
                upload_url = f"{server_url}/v1/projects/{project_id}/forms/{form_id}/draft"
                upload_response = requests.post(upload_url, headers=headers_upload, files=files)
            else:
                # Create new form
                upload_url = f"{server_url}/v1/projects/{project_id}/forms"
                upload_response = requests.post(upload_url, headers=headers_upload, files=files)
        
        if upload_response.status_code not in [200, 201]:
            print(f"✗ Upload failed: {upload_response.status_code}")
            print(f"Response: {upload_response.text}")
            return False
        
        print("✓ Form uploaded successfully")
        
        # Step 4: Publish draft if needed
        if form_exists:
            print("\n[4/4] Publishing draft...")
            publish_url = f"{server_url}/v1/projects/{project_id}/forms/{form_id}/draft/publish"
            publish_response = requests.post(publish_url, headers=headers)
            
            if publish_response.status_code != 200:
                print(f"⚠ Warning: Failed to publish draft: {publish_response.status_code}")
                print(f"Response: {publish_response.text}")
                print("You may need to publish manually from ODK Central web interface.")
            else:
                print("✓ Form published successfully")
        else:
            print("\n[4/4] Form created")
        
        print("\n" + "=" * 60)
        print("✓ SUCCESS: Form uploaded to ODK Central!")
        print("=" * 60)
        print(f"\nForm ID: {form_id}")
        print(f"View at: {server_url}/#/projects/{project_id}")
        print("\nNext steps:")
        print("1. Review form in ODK Central web interface")
        print("2. Configure app users if needed")
        print("3. Download form to ODK Collect mobile app")
        
        return True
        
    except requests.exceptions.Timeout:
        print(f"\n✗ Error: Request timed out after 30 seconds")
        print("The server may be slow or unreachable")
        return False
    except requests.exceptions.ConnectionError:
        print(f"\n✗ Error: Cannot connect to {server_url}")
        print("Please check your internet connection and server URL")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    quick_upload()
