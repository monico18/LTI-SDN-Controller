import requests

def add_dhcp_server(username, password, host, dhcp_server_config):
    try:
        url = f"https://{host}/rest/ip/dhcp-server/add"
        response = requests.post(url, auth=(username, password), data=dhcp_server_config)
        return response.json()

    except Exception as e:
        print("Failed to add DHCP server:", str(e))

def delete_dhcp_server(username, password, host, dhcp_server_id):
    try:
        url = f"http://{host}/rest/ip/dhcp-server/{dhcp_server_id}"
        response = requests.delete(url, auth=(username, password), data={'.id': dhcp_server_id})
        return response.json()

    except Exception as e:
        print("Failed to delete DHCP server:", str(e))

def edit_dhcp_server(username, password, host, dhcp_server_id, dhcp_server_config):
    try:
        url = f"https://{host}/rest/ip/dhcp-server/{dhcp_server_id}"
        response = requests.patch(url, auth=(username, password), data={'.id': dhcp_server_id, **dhcp_server_config})
        return response.json()

    except Exception as e:
        print("Failed to edit DHCP server:", str(e))

def get_available_dhcp_servers(username, password, host):
    try:
        url = f"https://{host}/rest/ip/dhcp-server"
        response = requests.get(url, auth=(username, password))
        dhcp_servers = response.json().get('data', [])
        return dhcp_servers

    except Exception as e:
        print("Failed to get available DHCP servers:", str(e))