import requests
from requests.auth import HTTPBasicAuth

def add_dhcp_server(username, password, host, dhcp_server_config):
    try:
        url = f"https://{host}/rest/ip/dhcp-server"
        response = requests.put(url, auth=HTTPBasicAuth(username, password), data=dhcp_server_config, verify=False)
        return response.json()

    except Exception as e:
        print("Failed to add DHCP server:", str(e))

def delete_dhcp_server(username, password, host, dhcp_server_id):
    try:
        url = f"http://{host}/rest/ip/dhcp-server/{dhcp_server_id}"
        response = requests.delete(url, auth=HTTPBasicAuth(username, password), data={'.id': dhcp_server_id}, verify=False)
        return response.json()

    except Exception as e:
        print("Failed to delete DHCP server:", str(e))

def edit_dhcp_server(username, password, host, dhcp_server_id, dhcp_server_config):
    try:
        url = f"https://{host}/rest/ip/dhcp-server/{dhcp_server_id}"
        response = requests.patch(url, auth=HTTPBasicAuth(username, password), data={'.id': dhcp_server_id, **dhcp_server_config}, verify=False)
        return response.json()

    except Exception as e:
        print("Failed to edit DHCP server:", str(e))

def get_available_dhcp_servers(username, password, host):
        response = requests.get(f"https://{host}/rest/ip/dhcp-server", auth=HTTPBasicAuth(username, password), verify=False)
        dhcp_servers = response.json()
        return dhcp_servers