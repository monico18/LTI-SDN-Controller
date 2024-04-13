import requests
from requests.auth import HTTPBasicAuth

def get_pools(username, password, host):
    try:
        response = requests.get(f"https://{host}/rest/ip/pool", auth=HTTPBasicAuth(username, password), verify=False)
        pools = response.json()
        return pools

    except Exception as e:
        print("Failed to get pools:", str(e))

def add_pool(username, password, host, pool_config):
    try:
        response = requests.post(f"https://{host}/rest/ip/pool", auth=HTTPBasicAuth(username, password), data=pool_config, verify=False)
        return response.json()

    except Exception as e:
        print("Failed to add pool:", str(e))
def delete_pool(username, password, host, pool_id):
    try:
        response = requests.delete(f"https://{host}/rest/ip/pool/{pool_id}", auth=HTTPBasicAuth(username, password), verify=False)
        return response.json()

    except Exception as e:
        print("Failed to delete pool:", str(e))

def edit_pool(username, password, host, pool_id, pool_config):
    try:
        response = requests.patch(f"https://{host}/rest/ip/pool/{pool_id}", auth=HTTPBasicAuth(username, password), data={'.id': pool_id, **pool_config}, verify=False)
        return response.json()

    except Exception as e:
        print("Failed to edit pool:", str(e))