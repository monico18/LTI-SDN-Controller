import requests
import json
from requests.auth import HTTPBasicAuth

def get_wireless_profiles(username, password, host):
    try:
        response = requests.get(f"https://{host}/rest/interface/wireless", auth=HTTPBasicAuth(username, password), verify=False)
        wireless_profiles = response.json()
        return wireless_profiles

    except Exception as e:
        print("Failed to get wireless profiles:", str(e))

def get_wireless_profile(username, password, host, wireless_profile_id):
    try:
        response = requests.get(f"https://{host}/rest/interface/wireless/{wireless_profile_id}", auth=HTTPBasicAuth(username, password), verify=False)
        wireless_profile = response.json()
        return wireless_profile

    except Exception as e:
        print("Failed to get wireless profile:", str(e))

def edit_wireless_profile(username, password, host, wireless_profile_id, wireless_profile_config):
    try:
        data = {
            '.id': wireless_profile_id, **wireless_profile_config
        }
        json_data = json.dumps(data)
        response = requests.patch(f"https://{host}/rest/interface/wireless/{wireless_profile_id}", auth=HTTPBasicAuth(username, password), 
                                  data=json_data, headers={'Content-Type': 'application/json'}, verify=False)
        return response.json()

    except Exception as e:
        print("Failed to edit wireless profile:", str(e))
