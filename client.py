# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 11:46:06 2023

@author: Saulo
"""

import socket

def upload_file():
    print("upload...")

def fetch_file():
    print("fetch...")

def send_file(filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = '192.168.1.5'  # Replace with the actual server IP address
    server_port = 4444  # Use the same port number as in the server

    client_socket.connect((server_host, server_port))

    with open(filename, 'rb') as file:
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)

    client_socket.close()
    
def initiate_interface():
    user_choice = None
    quit_confirm = None
    
    
    print("\n*** File Sync starting... ***\n")
    while True:
        
        print("Possible actions:\n1)Upload a file\n2)Fetch a file\n3)Quit\n")
    
    
        while True:
            try:
                user_choice = int(input("Choose your next action: "))
                
                if user_choice in (1, 2, 3):
                    break  # Exit the loop if input is valid
                else:
                    print("Invalid choice. Please enter a valid choice.")
            
            except ValueError:
                print("Error. please enter a number\n")
                
        if user_choice == 1:
            upload_file()
        if user_choice == 2:
            fetch_file()
        if user_choice == 3:
            quit_confirm = input("\nAre you sure (y/n)? ")
            if quit_confirm == 'y':
                return

def recover_file(filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 4444
    proxy: int

    client_socket.recv()

    pass

            
    
    
    
if __name__ == "__main__":
    send_file("arquivo_teste.txt")
    #initiate_interface()
    #pass
