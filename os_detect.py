import subprocess
import re

def os_detect(host):
    result = subprocess.run(['ping', host,'-n','1'],stdout=subprocess.PIPE)
    output = result.stdout.decode()
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

