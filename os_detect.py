import subprocess
import re

def os_detect(host):
     # Option for the number of packets as a function of
    param = '-n'
    # Building the command. Ex: "ping -c 1 google.com"
    command = " ".join(['ping', param, '1', host]) 
    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
    match = re.search(r"TTL=(\d+)", output)
    if match:
        ttl = match.group(1)
    else:
        ttl = None
    if ttl:
        if int(ttl) >= 127:
            return ("The OS type is likely Windows")
        elif int(ttl) >= 63:
            return ("The OS type is likely Linux")
        else:
            return ("The OS type is likely Other")
    else:
        return ("Host is not accessible")
