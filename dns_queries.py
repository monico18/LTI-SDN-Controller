import requests
from requests.auth import HTTPBasicAuth
import json

def get_dns(username, password, host):
    try:
        response = requests.get(f"https://{host}/rest/ip/dns", auth=HTTPBasicAuth(username, password), verify=False)
        dns = response.json()
        return dns
    except Exception as e:
        print("Failed to get DNS:", str(e))

def update_dns(username, password, host, dns_config):
    try:
        json_data = json.dumps(dns_config)
        response = requests.post(f"https://{host}/rest/ip/dns/set", auth=HTTPBasicAuth(username, password), data=json_data,
                                 headers={'Content-Type': 'application/json'}, verify=False)
        return response.json()
    except Exception as e:
        print("Failed to edit DNS:", str(e))

def add_static_dns(username, password, host, dns_config):
    try:
        data = json.dumps(dns_config)
        response = requests.put(f"https://{host}/rest/ip/dns/static", auth=HTTPBasicAuth(username, password), data=data, verify=False)
        return response
    except Exception as e:
        print("Failed to add static DNS:", str(e))

def delete_static_dns(username, password, host, dns_id):
    try:
        requests.delete(f"https://{host}/rest/ip/dns/static/{dns_id}", auth=HTTPBasicAuth(username, password), verify=False)
    except Exception as e:
        print("Failed to remove static DNS:", str(e))

def update_static_dns(username, password, host, dns_id,dns_config):
    try:
        data = {
            '.id': dns_id, **dns_config
        }
        json_data = json.dumps(data)
        response = requests.patch(f"https://{host}/rest/ip/dns/static/{dns_id}", auth=HTTPBasicAuth(username, password), 
                                  data=json_data, headers={'Content-Type': 'application/json'}, verify=False)
        return response
    except Exception as e:
        print("Failed to update static DNS:", str(e))


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