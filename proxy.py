import socket
import random
import threading
import os

'''
GLOBAL VARIABLES
    In this section you can add your global variables:
'''

saved_files = {} #stores filename and a list of IPs associated with it.

'''
SERVER STARTER
    Functions associated with starting the server:
'''

def start_server():
    '''
    This function starts the proxy server. it listens on all interfaces on port 5555.
    This is in order to receive files from both client during upload and server during
    file retrieval.
    '''
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 5555  # Choose a port number

    server_socket.bind((host, port))
    server_socket.listen(5) #receives as parameter the number of possible queued connections

    print(f"Server listening on {host}:{port}")

    return server_socket

def handle_udp_client(server_socket_udp):
    while True:
        # Handle the UDP client's requests here
        data, client_address = server_socket_udp.recvfrom(1024)
        message = data.decode('utf-8')
        print(f"Received UDP data from client {client_address}: {message}")

        if (message == "FIND"):
            response = "PROXY-CONFIRM"
            server_socket_udp.sendto(response.encode('utf-8'), client_address)
        else:
            response = "PROXY-CONFIRM"
            global client_ip 
            client_ip = client_address[0]
            print(f"Updated client address as {client_ip}")
            server_socket_udp.sendto(response.encode('utf-8'), client_address)

        

def start_udp_server():
    # UDP socket
    server_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = '0.0.0.0'
    port_udp = 6666
    server_socket_udp.bind((host, port_udp))

    print(f"UDP Server listening on {host}:{port_udp}")

    # Start a thread to handle UDP clients
    threading.Thread(target=handle_udp_client, args=(server_socket_udp,)).start()
    #handle_udp_client(server_socket_udp)

'''
FILE HANDLING FUNCTIONS
    Functions to handle the files. Include a function to receive a file and a function
    to send files.
'''

def receive_file(client_socket, filename): #receives socket. filename is so it can save a copy.
    with open(filename, 'wb') as file:
        while True:
            data = client_socket.recv(1024) #reads the data in the file.
            if not data:
                break
            file.write(data)

def send_file(filename, destination_address, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = destination_address  # Replace with the actual server IP address
    server_port = port  # Use the same port number as in the server

    client_socket.connect((server_host, server_port))

    with open(filename, 'rb') as file:
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)

    client_socket.close()


'''
FILE LIST FUNCTIONS
    Functions to handle appending and finding files on the
    saved_files dictionary declared above
'''
            
def append_file_server(filename, ip):
     # Check if the filename is already in the dictionary
    if filename in saved_files:
        # If yes, append the IP to the existing list
        saved_files[filename].append(ip)
    else:
        # If no, create a new entry with the filename and a list containing the IP
        saved_files[filename] = [ip]

def get_ips_for_file(filename):
    # Check if the filename is in the dictionary
    if filename in saved_files:
        # Return the list of IPs for the given filename
        return saved_files[filename]
    else:
        # If the filename is not found, return an empty list
        return []

'''
MESSAGES FUNCTIONS
    Crucial to control the flow of the application. There are 3 types
    of messages:

    1) FILE:{filename} - signals the recipient it's about to receive a
    file from upload.
    2) CONNECT - signals the recipient the source is trying to connect
    to integrate the network of storage servers.
    3) RECOVER:{filename} - signals the recipient it wants filename back
    from a storage server
'''

            
def send_upload_message(filename, source_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = source_address  # Replace with the actual server IP address
    server_port = 4444  # Use the same port number as in the server

    client_socket.connect((server_host, server_port))

    # Send the connect message
    message = filename
    client_socket.send(message.encode('utf-8'))

    client_socket.close()
    
def send_recover_message(filename, source_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = source_address  # Replace with the actual server IP address
    server_port = 4444  # Use the same port number as in the server

    client_socket.connect((server_host, server_port))

    # Send the connect message
    message = "RECOVER:"+filename
    client_socket.send(message.encode('utf-8'))

    client_socket.close()

def send_modify_message(filename, destination_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = destination_address  # Replace with the actual server IP address
    server_port = 4444  # Use the same port number as in the server

    client_socket.connect((server_host, server_port))

    # Send the connect message
    message = "MODIFY:"+filename
    client_socket.send(message.encode('utf-8'))

    client_socket.close()


'''
FLOW CONTROL
    Functions to handle control of the application based on messages
    received.
'''
    

def handle_connection(client_socket, source_addresses):
    # Receive the message containing the operation and filename
    message = client_socket.recv(1024).decode('utf-8')

    
    if message.startswith("CONNECT"):
        # Handles server trying to connect.
        # Adds IP of connected server to the list of possible recipients
        # List name is source_addresses

        print("CONNECT message received") # FOR DEBUGGING
        source_address = client_socket.getpeername()[0]
        source_addresses.append(source_address)
        print(f"Connected servers: {source_addresses}")
        client_socket.close()
        print("Connect socket closed") # FOR DEBUGGING
        

    elif message.startswith("FILE:"):
        # Handles client sending files
        # redirects the file to a random connected server
        # appends the IP of the server to the dictionary saved_files

        print("FILE message received") # FOR DEBUGGING
        filename = message.split(":")[1]
        filename = filename.split(".")[0]
        copies = int(message.split(":")[2])
        
        print("FILE Wait Accept") # FOR DEBUGGING
        client_socket, client_address = server_socket.accept()
        print("FILE Wait Accept passed") # FOR DEBUGGING
        receive_file(client_socket, filename+"-proxy.txt")
        print("File receive passed") # FOR DEBUGGING
        print(f"Received file: {filename}")
        print("\nRelaying file...")
        
        destination_list = random.sample(source_addresses, copies)
        print("Destination list passed") # FOR DEBUGGING
        
        for element in destination_list:
            send_upload_message(filename+"-proxy.txt", element)
            send_file(filename+"-proxy.txt", element, 4444)
            print("File relayed to "+element+"\n")
            append_file_server(filename+".txt", element)
            print(saved_files)
            print("File sent passed") # FOR DEBUGGING

        client_socket.close()
        print("File socket closed") # FOR DEBUGGING
        os.remove(filename+"-proxy.txt")
        
    elif message.startswith("RECOVER:"):
        # Handles the client requesting a file recovery

        print("RECOVER message received") # FOR DEBUGGING
        filename = message.split(":")[1]
        
        destination_list = get_ips_for_file(filename)
        
        for element in destination_list:
            try:
                send_recover_message(filename, element)
                print("RECOVER Wait Accept") # FOR DEBUGGING
                client_socket, client_address = server_socket.accept()
                print("RECOVER Wait Accept passed") # FOR DEBUGGING
                receive_file(client_socket, filename)
                print("File received") # FOR DEBUGGING
                print(f"Received file: {filename}")
                print("\nRelaying file...")
                print("Sending file...") # FOR DEBUGGING
                send_file(filename, client_ip, 3333)
                print("File sent") # FOR DEBUGGING
                print("File relayed to client\n")
                break
            
            except:
                print("Something went wrong. Trying again...")

        client_socket.close()
        print("File socket closed") # FOR DEBUGGING
        os.remove(filename)

    elif message.startswith("FIND"):
        print("FIND message received") # FOR DEBUGGING
        source_address = client_socket.getpeername()[0]
        print("Replying FIND message from server") # FOR DEBUGGING
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((source_address, 4444))
        print("Connection successful") # FOR DEBUGGING
        message = "PROXY-CONFIRM"
        client_socket.send(message.encode('utf-8'))
        print("Message sent") # FOR DEBUGGING
        client_socket.close()
        print("Socket closed") # FOR DEBUGGING
    
    elif message.startswith("SERVER-STATUS"):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((client_ip, 3333))
        message = "Connected with " + str(len(source_addresses)) + " machines with these addresses " + str(source_addresses)
        client_socket.send(message.encode('utf-8'))
        client_socket.close()

    elif message.startswith("MODIFY:"):
        print("MODIFY message received") # FOR DEBUGGING
        filename = message.split(":")[1]
        copies = int(message.split(":")[2])
        print(filename) # FOR DEBUGGING
        
        if (len(get_ips_for_file(filename)) > copies):
            print("MODIFY entered loop") # FOR DEBUGGING
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("MODIFY socket opened") # FOR DEBUGGING
            client_socket.connect((client_ip, 3333))
            print("MODIFY socket connected") # FOR DEBUGGING
            message = "DELETION"
            client_socket.send(message.encode('utf-8'))
            print("DELETION MESSAGE SENT socket connected") # FOR DEBUGGING
            client_socket.close()
            print("DELETION socket closed") # FOR DEBUGGING

            destination_list = random.sample(source_addresses, len(get_ips_for_file(filename))-copies)
            print(destination_list) # FOR DEBUGGING
            print("Destination list passed") # FOR DEBUGGING
            for element in destination_list:
                print("destination about to go") # FOR DEBUGGING
                send_modify_message(filename.split(".")[0] + "-proxy-server.txt", element)
                print(f"sent MODIFY to {destination_list}") # FOR DEBUGGING
            client_socket.close()
            print("MODIFY socket closed") # FOR DEBUGGING
        elif (len(get_ips_for_file(filename)) < copies):
            new_copies = copies - len(get_ips_for_file(filename))
            filename = filename.split(".")[0]

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((client_ip, 3333))
            message = "RESEND:"+str(new_copies)
            client_socket.send(message.encode('utf-8'))
            print("RESEND MESSAGE")
            client_socket.close()
            
            print("FILE Wait Accept") # FOR DEBUGGING
            client_socket, client_address = server_socket.accept()
            print("FILE Wait Accept passed") # FOR DEBUGGING
            receive_file(client_socket, filename+"-proxy.txt")
            print("File receive passed") # FOR DEBUGGING
            print(f"Received file: {filename}")
            print("\nRelaying file...")
            
            destination_list = random.sample(source_addresses, new_copies)
            print("Destination list passed") # FOR DEBUGGING
            
            for element in destination_list:
                send_upload_message(filename+"-proxy.txt", element)
                send_file(filename+"-proxy.txt", element, 4444)
                print("File relayed to "+element+"\n")
                append_file_server(filename+".txt", element)
                print(saved_files)
                print("File sent passed") # FOR DEBUGGING

            client_socket.close()
            print("File socket closed") # FOR DEBUGGING
            os.remove(filename+"-proxy.txt")


if __name__ == "__main__":
    server_socket = start_server()
    start_udp_server()
    print("Sever started") # FOR DEBUGGING
    source_addresses = []
    print("File catalog created") # FOR DEBUGGING

    while True:
        print("LOOP Wait Accept") # FOR DEBUGGING
        client_socket, client_address = server_socket.accept()
        print("LOOP Wait Accept passed") # FOR DEBUGGING
        print(f"Connection from {client_address}")
        print("Handle Connection started...") # FOR DEBUGGING
        handle_connection(client_socket, source_addresses)


