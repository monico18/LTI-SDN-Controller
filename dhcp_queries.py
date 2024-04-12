def add_dhcp_server(api, dhcp_server_config):
    try:
        return api('/ip/dhcp-server/add', **dhcp_server_config)

    except Exception as e:
        print("Failed to add DHCP server:", str(e))

def delete_dhcp_server(api, dhcp_server_id):
    try:
        return api('/ip/dhcp-server/remove', {'.id': dhcp_server_id})
    except Exception as e:
        print("Failed to delete DHCP server:", str(e))

def edit_dhcp_server(api, dhcp_server_id, dhcp_server_config):
    try:
        return api('/ip/dhcp-server/set', {'.id': dhcp_server_id, **dhcp_server_config})
    except Exception as e:
        print("Failed to edit DHCP server:", str(e))
    else:
        print("Failed to edit DHCP server.")

def get_available_dhcp_servers(api):
    try:
        response = api('/ip/dhcp-server/print')
        dhcp_servers = response.get('data', [])
        return dhcp_servers
    except Exception as e:
        print("Failed to get available DHCP servers:", str(e))