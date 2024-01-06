import socket
import shutil

def start_server():
    '''
    This function starts the client server. it listens on all interfaces on port 3333.
    This is in order to receive files from both client during upload and server during
    file retrieval.
    '''
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 3333  # Choose a port number

    server_socket.bind((host, port))
    server_socket.listen(5) #receives as parameter the number of possible queued connections

    print(f"Client awaiting file on {host}:{port}")

    return server_socket

def timeout_handler(signum, frame):
    # This function will be called when the timeout occurs
    raise TimeoutError("Timeout occurred")

def send_broadcast_message():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    #print("Socket created") # FOR DEBUGGING
    server_port = 6666  # Use the same port number as in the server

    # Send the connect message to the broadcast address
    broadcast_address = '192.168.1.255'  # Replace with the broadcast address of your subnet
    message = "CLIENT-FIND"

    client_socket.sendto(message.encode('utf-8'), (broadcast_address, server_port))
    #print("FIND message sent") # FOR DEBUGGING

    # Receive the response (assuming the server responds with its address)
    response, server_address = client_socket.recvfrom(1024)
    #print("FIND response received") # FOR DEBUGGING
    print(f"Received response from {server_address}: {response.decode('utf-8')}")

    client_socket.close()
    #print("Socket closed") # FOR DEBUGGING
    return server_address[0]

def send_status_message(destination_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = destination_address  # Replace with the actual server IP address
    server_port = 5555  # Use the same port number as in the server

    client_socket.connect((server_host, server_port))

    # Send the connect message
    message = "SERVER-STATUS"
    client_socket.send(message.encode('utf-8'))

    client_socket, client_address = server_socket.accept()
    response = client_socket.recv(1024).decode('utf-8')
    
    client_socket.close()

    return response

def send_upload_message(filename, destination_address, copies):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = destination_address  # Replace with the actual server IP address
    server_port = 5555  # Use the same port number as in the server

    client_socket.connect((server_host, server_port))

    # Send the connect message
    message = "FILE:"+filename+":"+copies
    client_socket.send(message.encode('utf-8'))

    client_socket.close()



def send_recover_message(filename,destination_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = destination_address  # Replace with the actual server IP address
    server_port = 5555  # Use the same port number as in the server

    client_socket.connect((server_host, server_port))

    # Send the connect message
    message = "RECOVER:"+filename
    client_socket.send(message.encode('utf-8'))

    client_socket.close()

def send_modify_message(filename, destination_address, copies):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = destination_address  # Replace with the actual server IP address
    server_port = 5555  # Use the same port number as in the server

    client_socket.connect((server_host, server_port))

    # Send the connect message
    message = "MODIFY:"+filename+":"+copies
    client_socket.send(message.encode('utf-8'))

    client_socket.close()

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

def recover_file(filename): #receives socket. filename is so it can save a copy.
    client_socket, client_address = server_socket.accept()
    with open(filename, 'wb') as file:
        while True:
            data = client_socket.recv(1024) #reads the data in the file.
            if not data:
                break
            file.write(data)

def print_centered(text):
    terminal_width, _ = shutil.get_terminal_size()
    centered_text = text.center(terminal_width)
    print(centered_text)

if __name__ == "__main__":
    server_socket = start_server()
    proxy_address = send_broadcast_message()
    print("Successfully connected to proxy\n\n")
    
    
    # Choose one of the following options based on your needs:

    # Option 1: Connect to the server

    # Option 2: Send a file
    '''
    send_upload_message("teste.txt", proxy_address)
    print("Upload message sent") # FOR DEBUGGING

    send_file("teste.txt", proxy_address)
    print("File Sent") # FOR DEBUGGING

    send_recover_message("teste.txt", proxy_address)
    print("Recovery message sent") # FOR DEBUGGING

    recover_file("teste-recovered.txt")
    print("File recovered") # FOR DEBUGGING
    '''
    print_centered(" *** Welcome to FileSync *** ")
    print_centered(" *** warning: this application is a prototype *** ")
    print("You can type commands on this application. If you're not sure what to do, type help.")
    while(True):
        user_input = input("FileSync>> ")

        if(user_input.startswith("help")):
            print("List of commands(use parameters without brackets):\n")
            print("upload [filename with extension] [number of copies] --- uploads n copies of filename to random connected servers")
            print("recover [filename with extension] --- recovers a copy of filename stored in a random connected server")
            print("connected-servers --- displays the number and list of connected servers.")
            print("modify [filename with extension] [number of copies] --- changes the number of copies in servers to given number")
            print("quit --- closes the application")
        elif(user_input.startswith("upload")):
            filename = user_input.split()[1]
            copies = user_input.split()[2]
            max_copies = int(send_status_message(proxy_address).split()[2])

            if (int(copies) <= max_copies):
                send_upload_message(filename, proxy_address, copies)
                send_file(filename, proxy_address)
            else:
                print("Number of copies requested exceeds the number of servers.")
                print("You can check the number of connected servers by the 'connected-servers' command.")

        elif(user_input.startswith("recover")):
            filename = user_input.split()[1]
            send_recover_message(filename, proxy_address)
            recover_file(filename.split(".")[0]+"-recovered.txt")
        elif(user_input.startswith("connected-servers")):
            status = send_status_message(proxy_address)
            print(status)
        elif(user_input.startswith("modify")):
            filename = user_input.split()[1]
            copies = user_input.split()[2]
            max_copies = int(send_status_message(proxy_address).split()[2])

            send_modify_message(filename, proxy_address, copies)

            if (int(copies) <= max_copies):
                client_socket, client_address = server_socket.accept()
                response = client_socket.recv(1024).decode('utf-8')

                if(response.startswith("RESEND:")):
                    new_copies = response.split(":")[1]
                    send_file(filename, proxy_address)


            else:
                print("Number of copies requested exceeds the number of servers.")
                print("You can check the number of connected servers by the 'connected-servers' command.")

            



            client_socket.close()

            if (response.startswith("RESEND:")):
                copies = int(response.split(":")[1])
                

        elif(user_input.startswith("quit")):
            break
        else:
            print(f"{user_input} não é um comando reconhecido desta aplicação")




