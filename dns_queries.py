def create_dns(api, address):
    api(cmd='/ip/dns/set', servers=address, allow_remote_requests=True)

def add_static_dns(api, name, address):
    api(cmd='/ip/dns/static/add', name=name, address=address)

def remove_static_dns(api, record_id):
    api(cmd='/ip/dns/static/remove', numbers=record_id)

def enable_static_dns(api, record_id):
    api(cmd='/ip/dns/static/enable', numbers=record_id)

def disable_static_dns(api, record_id):
    api(cmd='/ip/dns/static/disable', numbers=record_id)