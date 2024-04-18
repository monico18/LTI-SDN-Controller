import requests
from requests.auth import HTTPBasicAuth
import json

def get_static_routes(username, password, host):
    try:
        response = requests.get(f"https://{host}/rest/ip/route", auth=HTTPBasicAuth(username, password), verify=False)
        static_routes = response.json()
        return static_routes

    except Exception as e:
        print("Failed to get static routes:", str(e))

def add_static_route(username, password, host, static_route_config):
    try:
        data = json.dumps(static_route_config)
        response = requests.put(f"https://{host}/rest/ip/route", auth=HTTPBasicAuth(username, password), data=data, verify=False)
        print(response.json())
        return response.json()

    except Exception as e:
        print("Failed to add static route:", str(e))

def edit_static_route(username, password, host, static_route_id, static_route_config):
    try:
        data = {
            '.id': static_route_id, **static_route_config
        }
        json_data = json.dumps(data)
        response = requests.patch(f"https://{host}/rest/ip/route/{static_route_id}", auth=HTTPBasicAuth(username, password), data=json_data, verify=False)
        return response.json()

    except Exception as e:
        print("Failed to edit static route:", str(e))

def delete_static_route(username, password, host, static_route_id):
    try:
        requests.delete(f"https://{host}/rest/ip/route/{static_route_id}", auth=HTTPBasicAuth(username, password), verify=False)
    except Exception as e:
        print("Failed to delete static route:", str(e))

def get_static_route(username, password, host, static_route_id):
    try:
        response = requests.get(f"https://{host}/rest/ip/route/{static_route_id}", auth=HTTPBasicAuth(username, password), verify=False)
        static_route = response.json()
        return static_route

    except Exception as e:
        print("Failed to get static route:", str(e))