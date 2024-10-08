import requests
import json
from requests.auth import HTTPBasicAuth

def get_bridges(username, password, host):
    try:
        response = requests.get(f"https://{host}/rest/interface/bridge", auth=HTTPBasicAuth(username, password), verify=False)
        bridges = response.json()
        return bridges

    except Exception as e:
        print("Failed to get bridges:", str(e))

def add_bridge(username, password, host, bridge_config):
    try:
        data = json.dumps(bridge_config)
        response = requests.put(f"https://{host}/rest/interface/bridge", auth=HTTPBasicAuth(username, password), data=data, verify=False)
        return response.json()

    except Exception as e:
        print("Failed to add bridge:", str(e))

def get_bridge_ports(username, password, host):
    try:
        response = requests.get(f"https://{host}/rest/interface/bridge/port", auth=HTTPBasicAuth(username, password), verify=False)
        bridge_ports = response.json()
        return bridge_ports

    except Exception as e:
        print("Failed to get bridge ports:", str(e))

def add_bridge_port(username, password, host, port_config):
    try:
        data = json.dumps(port_config)
        response = requests.put(f"https://{host}/rest/interface/bridge/port", auth=HTTPBasicAuth(username, password), data=data, verify=False)
        return response.json()

    except Exception as e:
        print("Failed to add bridge port:", str(e))

def delete_bridge_port(username, password, host, port_id):
    try:
        port_id_str = str(port_id)
        requests.delete(f"https://{host}/rest/interface/bridge/port/{port_id_str}", auth=HTTPBasicAuth(username, password),
                                    verify=False)
    except Exception as e:
        print("Failed to delete bridge port:", str(e))

def get_bridge(username, password, host, bridge_id):
    try:
        response = requests.get(f"https://{host}/rest/interface/bridge/{bridge_id}", auth=HTTPBasicAuth(username, password), verify=False)
        bridge = response.json()
        return bridge

    except Exception as e:
        print("Failed to get bridge:", str(e))

def edit_bridge(username, password, host, bridge_id, bridge_config):
    try:
        data = {
            '.id': bridge_id, **bridge_config
        }
        json_data = json.dumps(data)
        response = requests.patch(f"https://{host}/rest/interface/bridge/{bridge_id}", auth=HTTPBasicAuth(username, password), data=json_data,
                                  headers={'Content-Type': 'application/json'}, verify=False)
        return response.json()

    except Exception as e:
        print("Failed to edit bridge:", str(e))

def delete_bridge(username, password, host, bridge_id):
    try:
        requests.delete(f"https://{host}/rest/interface/bridge/{bridge_id}", auth=HTTPBasicAuth(username, password), verify=False)

    except Exception as e:
        print("Failed to delete bridge:", str(e))
