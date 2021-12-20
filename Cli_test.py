import socket
import threading
SERVER=socket.gethostbyname(socket.gethostname())
PORT = 8000
FORMAT = "utf_16"
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM: giao thức TCP
        
def RecieveList(client, list):
    data = ""
    data= client.recv(1024).decode(FORMAT)
    while(data!="end"):
        list.append(data)
        client.send(data.encode(FORMAT))
        data= client.recv(1024).decode(FORMAT)
    client.send(data.encode(FORMAT))
    return list

client.connect((SERVER, PORT))
list = []
RecieveList(client,list)

print(list)