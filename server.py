# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 11:45:14 2023

@author: Saulo
"""
import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 5555  # Choose a port number

    proxy_host = '192.168.1.5'  # Replace with the actual proxy server IP address
    proxy_port = 8888  # Use the same port number as in the proxy server

    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server connecting to proxy at {proxy_host}:{proxy_port}")
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((proxy_host, proxy_port))
    
    print(f"Server listening on {host}:{port}")

    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    return client_socket

def receive_file(client_socket:socket.socket, filename):
    with open(filename, 'wb') as file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)

def send_file(filename, port, proxy_ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((proxy_ip, port))

    with open(filename, 'rb') as file:
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)

    client_socket.close()

if __name__ == "__main__":
    client_socket = start_server()
    receive_file(client_socket, "received_file.txt")
