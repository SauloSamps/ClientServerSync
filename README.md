# ClientServerSync Prototype

This is a simple python script to sync files between machines. This was made as a project for college and it was written fully in Python utilizing the Socket library (requirement). The project fulfilled the following requirements:
-Must use Socket
-Connects a client machine to a 'proxy', and the proxy can connect to any number of server machines
-The client must be able to send copies of files through the proxy to a specified number of machines
-The client to should also be able to retrieve the file from any machine connected and modify the number of copies
-Each machine must hold only one copy

## Implementation

The following requirements were added as a bonus:
-Machines must connect through the local network autonomously, just running the script is sufficient for roles to be attributed
-We limited the scope of the prototype for text (.txt) files only


The requirements were fulfilled (mostly) except the ability to modify number of copies. An error still happens where the application isn't reacting correctly to the signals sent by the proxy in that specific instance. 
The program functions through a series of messages that allows the machines to react correctly, so that TCP can be used for file transfers between them. This script also uses UDP to initially connect the machines and figure out each others' IP addresses.
Overall the program still lacks some functionalities that would be nice to have but were not the priority for this project, including some error messages for wrong user input and better logs. Also it could be VERY simplified by letting the user do some setup and giving up on the autonomous connection feature.
This project took between 1 and 2 weeks to be finished and it absolutely is a prototype.

https://docs.google.com/presentation/d/1D7sUDnKXfndX3jjsaxohzKVYVysqz5OHTcMW3Cv0dvQ/edit?usp=sharing

This slide presentation above briefly explains how the connection works here. It's portuguese only.

## How to run

No installation is required. Simply run the python script on any number of machines, but one must run the client, another the server and yet another the proxy. 
Start the proxy first. The three scripts can be running on the same machine if you want but ideally you want at least three machines connected on the same network.
