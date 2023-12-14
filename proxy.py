# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 11:45:14 2023

@author: Saulo
"""
"""CLIENT -> PROXY -> SERVER  """
import socket

def start_proxy(port1, port2, lista:list):
    proxy_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '0.0.0.0'  # Listen on all available interfaces

    proxy_socket1.bind((host, port1))
    proxy_socket2.bind((host, port2))

    proxy_socket1.listen(1)
    proxy_socket2.listen(1)

    print(f"Proxy listening on {host}:{port1}")
    print(f"Proxy listening on {host}:{port2}")

    while True:
        try:
            client_socket, client_address = proxy_socket1.accept()
            print(f"Connection from Server: {client_address}")
            lista.append(client_address[0])
            print(client_address)
            client_socket.close()
        except KeyboardInterrupt:
            break

    proxy_socket1.close()
    #proxy_socket2.close()



def receive_file(client_socket:socket.socket, filename):
    with open(filename, 'wb') as file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            file.write(data)

def send_file(filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = '192.168.1.2'  # Replace with the actual server IP address
    server_port = 5555  # Use the same port number as in the server

    client_socket.connect((server_host, server_port))

    with open(filename, 'rb') as file:
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)

    client_socket.close()

if __name__ == "__main__":
    lista = []
    start_proxy(8888, 4444, lista)
