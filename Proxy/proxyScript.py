import socket
import ssl
import time

host = "0.0.0.0" # allows proxy to listen to all incoming connections
port = 50007 # ephemeral port
destPort = 8080 # for an HTTP connection

# two lines needed for TLS encryption from client->proxy
contextServer = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER) # context stores all default settings of a server needing to make TLS connection (server beacuse of attribute PROTOCOL_TLS_SERVER)
                                                        # constructing a SSLContext object which is a class provided by SSL
contextServer.load_cert_chain(certfile="MyCert.crt", keyfile="MyKey.key") # loads the public certificate and private key into the TLS context object
                                                                          # certificates are usually signed by a trusted authority but can make a self
                                                                          # signed one for testing purposes, need a certificate for TLS server so client can trust

# context for TLS from proxy->website
contextClient = ssl.create_default_context() # creates TLS context with default settings
contextClient.check_hostname = False # disables chacking domain names on the certificate it is accepting
contextClient.verify_mode = ssl.CERT_NONE # allows the client to accept any certificate

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientConnIn: # create a new socket object as the clients connection in
    clientConnIn.bind((host, port)) # bind the socket to the host and port variables
    clientConnIn.listen(1) # sets port to listen for incoming connections, allowing max one connection in the queue
    while True:
        serverTLSConn, addr = clientConnIn.accept() # when this line is run, as soon it it gets to accept() is waits until a connection comes in,
                                                    # then it stores the incoming clients IP address in addr and creates a new socket object to store the incoming connection 
                                                    # (kind of like in multithreading passing off the connection), in serverTLSConn
        with contextServer.wrap_socket(serverTLSConn, server_side=True) as serverTLSConn: # takes the serverTLSConn object, wraps it in the defined context, then restores it in the same variable
            print('Connected by', addr)
            data1 = serverTLSConn.recv(4096) # defines data 1 as the incoming data from the TLS connection, can recieve up to 1024 bytes, can recieve any amount of bytes though
            time_recieved_proxy = time.time() # proxy recieves the data right after recv so we add this here

            # now here we are acting as a client and trying to connect out to the website and forwarding the data we recieved
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientConnOut: # this is creating a socket for the conneciton out to the website
                
                # this block of code was added to allow the proxy to hit whatever endpoint is passed into it by the client
                website_string = data1.decode() # store the decoded version of the http request so that it can be parsed easier
                index_website_start = website_string.find("Website: ")
                index_website_start += 9 # adding nine so that we can start this variable at the start of the IP address
                index_website_end = website_string.find("\r\n\r\n")
                destHost = website_string[index_website_start:index_website_end].strip() # strip included to remove any extra newlines

                clientConnOut.connect((destHost, destPort)) # this connects the socket to the website, need a connection to website before you can wrap in TLS
                with contextClient.wrap_socket(clientConnOut, server_hostname=destHost) as clientTLSConnOut: # wrapping connection out in TLS
                    proxy_header = b"\r\nProxy-Received-At: " + str(time_recieved_proxy).encode()
                    index_header_end = data1.find(b"\r\n\r\n") # returns the index found where that string starts
                    data1 = data1[:index_header_end] + proxy_header + data1[index_header_end:] # reformat the packet by adding in first the original headers up to but not including \r\n\r\n
                                                                                            # then add in the new header,                                                                  
                                                                                            # then add in the last \r\n\r\n
                    clientTLSConnOut.sendall(data1)  # send modified packet
                    data2 = clientTLSConnOut.recv(4096) # data2 is the response from the website
                    serverTLSConn.sendall(data2) # sends the response from the website back to the client