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
                skip_once = True
            if line.strip() == "" and not skip_once:
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
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Returning current state.")

    return host_range

def ip_scan(host_ip):
    if ping(host_ip):
        return (True, f"{host_ip} is alive")
    else:
        return (False, f"{host_ip} is NOT alive")

# def main(host):
#     # ip_scan(host)
#     print(f"Reachable hosts: {host_dis(host)}")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("host", help="The host to scan")
#     args = parser.parse_args()

# host = "10.213.6.224"
# print(host_dis(host))
# # ip_scan ("10.213.6.224")
