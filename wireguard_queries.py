import requests
from requests.auth import HTTPBasicAuth

def get_wireguard_profiles(username, password, host):
    try:
        response = requests.get(f"https://{host}/rest/interface/wireguard", auth=HTTPBasicAuth(username, password), verify=False)
        wireguard_profiles = response.json()
        return wireguard_profiles

    except Exception as e:
        print("Failed to get wireguard profiles:", str(e))

def add_wireguard_profile(username, password, host, wireguard_profile_config):
    try:
        response = requests.put(f"https://{host}/rest/interface/wireguard", auth=HTTPBasicAuth(username, password), data=wireguard_profile_config, verify=False)
        return response.json()

    except Exception as e:
        print("Failed to add wireguard profile:", str(e))

def edit_wireguard_profile(username, password, host, wireguard_profile_id, wireguard_profile_config):
    try:
        response = requests.patch(f"https://{host}/rest/interface/wireguard/{wireguard_profile_id}", auth=HTTPBasicAuth(username, password), data={'.id': wireguard_profile_id, **wireguard_profile_config}, verify=False)
        return response.json()

    except Exception as e:
        print("Failed to edit wireguard profile:", str(e))

def delete_wireguard_profile(username, password, host, wireguard_profile_id):
    try:
        response = requests.delete(f"https://{host}/rest/interface/wireguard/{wireguard_profile_id}", auth=HTTPBasicAuth(username, password), verify=False)
        return response.json()

    except Exception as e:
        print("Failed to delete wireguard profile:", str(e))

def get_wireguard_peers(username, password, host):
    try:
        response = requests.get(f"https://{host}/rest/interface/wireguard/peers", auth=HTTPBasicAuth(username, password), verify=False)
        wireguard_peers = response.json()
        return wireguard_peers

    except Exception as e:
        print("Failed to get wireguard peers:", str(e))

def add_wireguard_peer(username, password, host, wireguard_peer_config):
    try:
        response = requests.put(f"https://{host}/rest/interface/wireguard/peers", auth=HTTPBasicAuth(username, password), data=wireguard_peer_config, verify=False)
        return response.json()

    except Exception as e:
        print("Failed to add wireguard peer:", str(e))

def edit_wireguard_peer(username, password, host, wireguard_peer_id, wireguard_peer_config):
    try:
        response = requests.patch(f"https://{host}/rest/interface/wireguard/peers/{wireguard_peer_id}", auth=HTTPBasicAuth(username, password), data={'.id': wireguard_peer_id, **wireguard_peer_config}, verify=False)
        return response.json()

    except Exception as e:
        print("Failed to edit wireguard peer:", str(e))

def delete_wireguard_peer(username, password, host, wireguard_peer_id):
    try:
        response = requests.delete(f"https://{host}/rest/interface/wireguard/peers/{wireguard_peer_id}", auth=HTTPBasicAuth(username, password), verify=False)
        return response.json()

    except Exception as e:
        print("Failed to delete wireguard peer:", str(e))
