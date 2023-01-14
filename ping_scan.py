import os
import socket
import subprocess
import threading

def get_ip():
   return str(socket.gethostbyname(socket.gethostname()))

def check_connection():
    output = subprocess.check_output("ipconfig", shell=True).decode()
    section = ""
    flag_found = False
    skip_once = False
    for line in output.splitlines():
        if "Wireless LAN adapter Wi-Fi" in line:
            flag_found = True
        if flag_found:
            if ":" in line:
                section += line + "\n"
            if line.strip():
                if not skip_once:
                    skip_once = True
                    continue
                else:
                    break

    if "Media disconnected" not in section:
        return True
    else:
        return False

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if os.name == 'nt' else '-c'

    # Redirect output to /dev/null on Unix-like systems or to NUL on Windows
    if os.name == 'nt':
        redirect = '> NUL 2>&1'
    else:
        redirect = '> /dev/null 2>&1'

    # Building the command. Ex: "ping -c 1 google.com"
    command = " ".join(['ping', param, '1', host]) 

    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    
    if "unreachable" in output or "timed out" in output:
        return False
    else:
        return True

def host_dis(host_ip):
    octets = host_ip.split(".")
    base_ip = ".".join(octets[:3])
    host_range = []
    threads = []

    def check_host(hostname):
        if ping(hostname):
            host_range.append(hostname)
    try:
        for j in range(225):
            hostname = f"{base_ip}.{j}"
            t = threading.Thread(target=check_host, args=(hostname,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()
    except:
        pass

    return host_range

def ip_scan(host_ip):
    if ping(host_ip):
        return (True, f"{host_ip} is alive")
    else:
        return (False, f"{host_ip} is NOT alive")

