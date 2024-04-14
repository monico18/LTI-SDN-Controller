import requests
from requests.auth import HTTPBasicAuth

def get_security_profiles(username, password, host):
    try:
        response = requests.get(f"https://{host}/rest/interface/wireless/security-profiles", auth=HTTPBasicAuth(username, password), verify=False)
        security_profiles = response.json()
        return security_profiles

    except Exception as e:
        print("Failed to get security profiles:", str(e))

def add_security_profile(username, password, host, security_profile_config):
    try:
        response = requests.put(f"https://{host}/rest/interface/wireless/security-profiles", auth=HTTPBasicAuth(username, password), data=security_profile_config, verify=False)
        return response.json()

    except Exception as e:
        print("Failed to add security profile:", str(e))

def edit_security_profile(username, password, host, security_profile_id, security_profile_config):
    try:
        response = requests.patch(f"https://{host}/rest/interface/wireless/security-profiles/{security_profile_id}", auth=HTTPBasicAuth(username, password), data={'.id': security_profile_id, **security_profile_config}, verify=False)
        return response.json()

    except Exception as e:
        print("Failed to edit security profile:", str(e))

def delete_security_profile(username, password, host, security_profile_id):
    try:
        response = requests.delete(f"https://{host}/rest/interface/wireless/security-profiles/{security_profile_id}", auth=HTTPBasicAuth(username, password), verify=False)
        return response.json()

    except Exception as e:
        print("Failed to delete security profile:", str(e))