import socket
import threading
from version_scan import *
from threading import Thread
from queue import Queue

def get_open_port(host):
    start_port = 1
    end_port = 9999
    open_ports = []

    def scan_port(port, open_ports):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        try:
            sock.connect((host, port))
            service = socket.getservbyport(port)
            open_ports.append((port, service))
        except socket.error:
            pass
        finally:
            sock.close()

    threads = []
    for port in range(start_port, end_port+1):
        t = threading.Thread(target=scan_port, args=(port, open_ports))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    return open_ports

def port_scan(host):
    str_open_ports = ""
    open_ports = get_open_port(host)
    # Print the open ports
    str_open_ports += "Open ports:\n"
    str_open_ports += "-" * 25 + "\n"
    if not len(open_ports):
        str_open_ports += "No open ports detected"
    for port, service in open_ports:
        str_open_ports += f"Port {port}: {service}\n"
    return str_open_ports

def port_scan_with_version(host):
    result_queue = Queue()
    open_ports = get_open_port(host)
    result_queue.put("Open ports:\n" + "-" * 25 + "\n")

    if not len(open_ports):
        result_queue.put("No open ports detected")
    else:
        threads = []

        def port_version_scan(host, port, service, result_queue):
            result_queue.put(f"Port       :  {port}\nService:  {service}\nVersion:  {version_scan(host, port)}\n\n")

        for port, service in open_ports:
            t = threading.Thread(target=port_version_scan, args=(host, port, service, result_queue))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    str_open_ports_with_version = ""
    while not result_queue.empty():
        str_open_ports_with_version += result_queue.get()
    return str_open_ports_with_version
