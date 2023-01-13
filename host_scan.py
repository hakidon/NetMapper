import os
import re
import socket

def get_hostname(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        hostname = None
    return hostname

def get_mac_address(ip):
    # Use the ARP command to get the MAC address
    result = os.popen("arp -a "+ip).read()
    match = re.search(r"(([a-f\d]{1,2}\-){5}[a-f\d]{1,2})", result)
    if match:
        mac_address = match.group(0)
    else:
        mac_address = 'Not accessible'
    return mac_address

def host_scan(ip):
    host_info = ''
    hostname = get_hostname(ip)
    mac_address = get_mac_address(ip)
    if hostname:
        host_info += f"Host name: {hostname}" + '\n'
    else:
        host_info += "Host name: (Not accessible)" + '\n'

    if mac_address:
        host_info += f"Mac address: {mac_address}"
    else:
        host_info += "Mac address: (Not accessible)"
    
    return host_info
