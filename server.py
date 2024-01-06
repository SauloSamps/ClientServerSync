import socket
import os

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 4444  # Choose a port number

    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    return server_socket
    
def send_connect_message(proxy_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = proxy_address  # Replace with the actual server IP address
    server_port = 5555  # Use the same port number as in the server

    client_socket.connect((server_host, server_port))

    # Send the connect message
    message = "CONNECT"
    client_socket.send(message.encode('utf-8'))

    client_socket.close()


def send_broadcast_message():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    print("Socket created") # FOR DEBUGGING
    server_port = 6666  # Use the same port number as in the server

    # Send the connect message to the broadcast address
    broadcast_address = '192.168.1.255'  # Replace with the broadcast address of your subnet
    message = "FIND"

    client_socket.sendto(message.encode('utf-8'), (broadcast_address, server_port))
    print("FIND message sent") # FOR DEBUGGING

    # Receive the response (assuming the server responds with its address)
    response, server_address = client_socket.recvfrom(1024)
    print("FIND response received") # FOR DEBUGGING
    print(f"Received response from {server_address}: {response.decode('utf-8')}")

    client_socket.close()
    print("Socket closed") # FOR DEBUGGING
    return server_address


def receive_file(client_socket, filename):
    
    with open(filename, 'wb') as file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)
            
def send_file(filename, destination_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = destination_address  # Replace with the actual server IP address
    server_port = 5555  # Use the same port number as in the server

    client_socket.connect((server_host, server_port))

    with open(filename, 'rb') as file:
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)

    client_socket.close()

def handle_connection(client_socket, destination_address):
    # Receive the message containing the operation and filename
    message = client_socket.recv(1024).decode('utf-8')
    #print(message)
    
    if message.startswith("RECOVER:"):
        print("RECOVER message received") # FOR DEBUGGING
        filename = message.split(":")[1]
        filename = filename.split(".")[0]
        
        send_file(filename+"-proxy-server.txt", destination_address)
        print(f"Recovering file: {filename}")
        print("\nRelaying file to proxy...")

    elif message.startswith("MODIFY:"):
        filename = message.split(":")[1]
        if os.path.exists(filename):
            # Delete the file
            os.remove(filename)
            print(f"The file '{filename}' has been deleted.")
        else:
            print(f"The file '{filename}' does not exist on this server.")
        
    else:
        filename = message.split(".")[0]
            
        client_socket, client_address = server_socket.accept()
        receive_file(client_socket, filename+"-server.txt")
        print(f"Received file: {filename}")

if __name__ == "__main__":
    server_socket = start_server()
    print("Sending FIND message") # FOR DEBUGGING
    proxy_address = send_broadcast_message()
    print("FIND message sent. Now connecting...") # FOR DEBUGGING
    send_connect_message(proxy_address[0])
    print("CONNECT message sent") # FOR DEBUGGING
    while True:
        print("waiting message")
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        handle_connection(client_socket, proxy_address[0])

