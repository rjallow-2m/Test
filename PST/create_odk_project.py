# create_odk_project.py
# Script to create a new project on ODK Central

import requests
from upload_config import ODK_CONFIG

def create_project(project_name):
    """Create a new project on ODK Central"""
    
    print("=" * 60)
    print("ODK Central - Create New Project")
    print("=" * 60)
    print()
    
    server_url = ODK_CONFIG['server_url'].rstrip('/')
    email = ODK_CONFIG['email']
    password = ODK_CONFIG['password']
    
    print(f"Server: {server_url}")
    print(f"Project Name: {project_name}")
    print()
    
    try:
        # Step 1: Authenticate
        print("[1/2] Authenticating...")
        auth_url = f"{server_url}/v1/sessions"
        auth_data = {
            "email": email,
            "password": password
        }
        
        auth_response = requests.post(auth_url, json=auth_data, timeout=10)
        
        if auth_response.status_code != 200:
            print(f"✗ Authentication failed: {auth_response.status_code}")
            print(f"Response: {auth_response.text}")
            return False
        
        token = auth_response.json()['token']
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        print("✓ Authentication successful")
        
        # Step 2: Create project
        print(f"\n[2/2] Creating project '{project_name}'...")
        project_url = f"{server_url}/v1/projects"
        project_data = {
            "name": project_name
        }
        
        project_response = requests.post(project_url, json=project_data, headers=headers, timeout=10)
        
        if project_response.status_code not in [200, 201]:
            print(f"✗ Failed to create project: {project_response.status_code}")
            print(f"Response: {project_response.text}")
            return False
        
        project_info = project_response.json()
        project_id = project_info.get('id')
        
        print("✓ Project created successfully")
        print("\n" + "=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print(f"\nProject Name: {project_name}")
        print(f"Project ID: {project_id}")
        print(f"Access at: {server_url}/#/projects/{project_id}")
        
        return project_id
        
    except requests.exceptions.Timeout:
        print(f"\n✗ Error: Request timed out")
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
    project_name = "Test"
    create_project(project_name)
