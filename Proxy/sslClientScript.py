import socket
import ssl
import time

host = "128.110.217.80" # IP address of proxy server (node 0)
website_ip = "128.110.217.91" # node 1
port = 50007 # ephemeral port

# three lines below needed to add TLS encryption
context = ssl.create_default_context() # creates TLS context with default settings
context.check_hostname = False # disables chacking domain names on the certificate
context.verify_mode = ssl.CERT_NONE # allows the client to accept any certificate

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    with context.wrap_socket(s, server_hostname=host) as s: # also needed to wrap normal socket in TLS socket
        s.sendall(b"GET /probe HTTP/1.1\r\nHost: " + host.encode() + b"\r\nClient-Sent-At: " + str(time.time()).encode() + b"\r\nWebsite: " + website_ip.encode() + b"\r\n\r\n") # keeps sending packets until the whole byte string is sent (can take multiple packets)
                                                                            # this is sending a HTTP GET request
        data = s.recv(4096) # reads up to 4096 bytes recieved back from the server, waits for response
        print(data)