import requests
from requests.auth import HTTPBasicAuth

def get_ip_address(username, password, host):
    try:
        response = requests.get(f"https://{host}/rest/ip/address", auth=HTTPBasicAuth(username, password), verify=False)
        ip_queries = response.json()
        return ip_queries

    except Exception as e:
        print("Failed to get ip queries:", str(e))

def add_ip_address(username, password, host, ip_query_config):
    try:
        response = requests.put(f"https://{host}/rest/ip/address", auth=HTTPBasicAuth(username, password), data=ip_query_config, verify=False)
        return response.json()

    except Exception as e:
        print("Failed to add ip query:", str(e))

def edit_ip_address(username, password, host, ip_query_id, ip_query_config):
    try:
        response = requests.patch(f"https://{host}/rest/ip/address/{ip_query_id}", auth=HTTPBasicAuth(username, password), data={'.id': ip_query_id, **ip_query_config}, verify=False)
        return response.json()

    except Exception as e:
        print("Failed to edit ip query:", str(e))

def delete_ip_address(username, password, host, ip_query_id):
    try:
        response = requests.delete(f"https://{host}/rest/ip/address/{ip_query_id}", auth=HTTPBasicAuth(username, password), verify=False)
        return response.json()

    except Exception as e:
        print("Failed to delete ip query:", str(e))


              