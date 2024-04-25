import requests
from requests.auth import HTTPBasicAuth
import json

def get_ip_addresses(username, password, host):
    try:
        response = requests.get(f"https://{host}/rest/ip/address", auth=HTTPBasicAuth(username, password), verify=False)
        ip_queries = response.json()
        return ip_queries

    except Exception as e:
        print("Failed to get ip queries:", str(e))

def get_ip_address(username, password, host, ip_id):
    try:
        response = requests.get(f"https://{host}/rest/ip/address/{ip_id}", auth=HTTPBasicAuth(username, password), verify=False)
        ip_queries = response.json()
        return ip_queries

    except Exception as e:
        print("Failed to get ip queries:", str(e))

def add_ip_address(username, password, host, ip_config):
    try:
        data = json.dumps(ip_config)
        response = requests.put(f"https://{host}/rest/ip/address", auth=HTTPBasicAuth(username, password), data=data, verify=False)
        return response

    except Exception as e:
        print("Failed to add ip query:", str(e))

def edit_ip_address(username, password, host, ip_id, ip_query_config):
    try:
        data = {
            '.id': ip_id, **ip_query_config
        }
        json_data = json.dumps(data)
        response = requests.patch(f"https://{host}/rest/ip/address/{ip_id}", auth=HTTPBasicAuth(username, password), data=json_data, verify=False)
        return response

    except Exception as e:
        print("Failed to edit ip query:", str(e))

def delete_ip_address(username, password, host, ip_id):
    try:
        requests.delete(f"https://{host}/rest/ip/address/{ip_id}", auth=HTTPBasicAuth(username, password), verify=False)
    except Exception as e:
        print("Failed to delete ip query:", str(e))


              