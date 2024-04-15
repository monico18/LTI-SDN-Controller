import requests
from requests.auth import HTTPBasicAuth

def get_dns(username, password, host):
    try:
        response = requests.get(f"https://{host}/rest/ip/dns", auth=HTTPBasicAuth(username, password), verify=False)
        dns = response.json()
        return dns
    except Exception as e:
        print("Failed to get DNS:", str(e))

def edit_dns(username, password, host, dns_config):
    try:
        response = requests.put(f"https://{host}/rest/ip/dns/set", auth=HTTPBasicAuth(username, password), data=dns_config, verify=False)
        return response.json()
    except Exception as e:
        print("Failed to edit DNS:", str(e))

def add_static_dns(username, password, host, name, address):
    try:
        response = requests.put(f"https://{host}/rest/ip/dns/static", auth=HTTPBasicAuth(username, password), data={'name': name, 'address': address}, verify=False)
        return response.json()
    except Exception as e:
        print("Failed to add static DNS:", str(e))

def remove_static_dns(username, password, host, dns_id):
    try:
        response = requests.delete(f"https://{host}/rest/ip/dns/static/{dns_id}", auth=HTTPBasicAuth(username, password), verify=False)
        return response.json()
    except Exception as e:
        print("Failed to remove static DNS:", str(e))

def edit_static_dns(username, password, host, dns_id):
    try:
        response = requests.patch(f"https://{host}/rest/ip/dns/static/{dns_id}", auth=HTTPBasicAuth(username, password), verify=False)
        return response.json()
    except Exception as e:
        print("Failed to remove static DNS:", str(e))


def get_static_dnses(username, password, host):
    try:
        response = requests.get(f"https://{host}/rest/ip/dns/static", auth=HTTPBasicAuth(username, password), verify=False)
        static_dns = response.json()
        return static_dns
    except Exception as e:
        print("Failed to get static DNS:", str(e) )

def get_static_dns(username, password, host, dns_id):
    try:
        response = requests.get(f"https://{host}/rest/ip/dns/static/{dns_id}", auth=HTTPBasicAuth(username, password), verify=False)
        static_dns = response.json()
        return static_dns
    except Exception as e:
        print("Failed to get static DNS:", str(e) )