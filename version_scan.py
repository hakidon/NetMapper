import socket

def version_scan(ip, port):
    server_version = ""
    try:
        # Create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.settimeout(3)

        # Connect to the server
        s.connect((ip, port))

        # Send a request to the remote host
        request = b"GET / HTTP/1.1\r\nUser-Agent: Python\r\nAccept: */*\r\n\r\n"
        s.send(request)

        # Receive a response from the remote host
        response = s.recv(4096)

        # Close the socket
        s.close()

        # Extract the server version from the headers
        header_str = response.decode()
        headers = header_str.split('\r\n')
        for header in headers:
            if 'Server' in header:
                server_version = header.split(':')[1].strip()
                break
    except:
        server_version = ('(Not accessible)')
        
    return (server_version)
