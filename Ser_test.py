
import socket
import threading
import pyodbc #thêm thư viện để kết nối với sql
PORT=8000
SERVER=socket.gethostbyname(socket.gethostname())
FORMAT="utf_16"
#Gửi danh sách sang client
def SendList(conn, list):
    for data in list:
        conn.send(data.encode(FORMAT))
        conn.recv(1024)
    msg = "end"
    conn.send(msg.encode(FORMAT))
    conn.recv(1024)

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM: giao thức TCP
server.bind((SERVER, PORT))

server.listen()
print("Server is waiting...")
print()
list = ['a','b','c']
conn, address = server.accept()
SendList(conn,list)
server.close()