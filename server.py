import socket
import threading
import pyodbc #thêm thư viện để kết nối với sql
PORT=8000
SERVER=socket.gethostbyname(socket.gethostname())
FORMAT="utf_16"

#Hàm nhận danh sách từ client
def RecieveList(conn):
    list = []
    data = None
    data= conn.recv(1024).decode(FORMAT)
    while(data!="end"):
        
        list.append(data)
        conn.send(data.encode(FORMAT))
        data= conn.recv(1024).decode(FORMAT)
    return list

#Hàm kiểm tra id và pw      
def AccountCheck(conn):
    temp = ""
    client_account = RecieveList(conn)
    for row in cursor.execute("select PASSWORD from INFORMATION where ID = ?", client_account[0]):
        #row trả về hàng chứa id. vd: ('nhan','123456')
        password = row[0] 
        temp = "checked"
    #conx.close() 
    if(temp != "checked"):
        #return 1
        ans = "ID does not exist."
    else:       
        if(client_account[1]==password):
            #return 2
            ans = "Login successfully!"
        else:
            #return 3
            ans = "Wrong password."
    conn.send(ans.encode(FORMAT))
    print(ans)

#Hàm thêm id và pw vào database
def Insert_ID_PW(id,pw):
    cursor = conx.cursor()
    cursor.execute("insert INFORMATION values (?,?)", id, pw)
    conx.commit() 

#Hàm đăng ký
def Signup(conn):
    temp = ""
    client_account = RecieveList(conn)
    for row in cursor.execute("select * from INFORMATION where ID = ?",client_account[0]):
        temp = "checked"
    if(temp == "checked"):
        #return 1
        ans = "ID already exists."
    else:
        if(client_account[1]==client_account[2]):
            #return 2
            ans = "Successfully!"
            Insert_ID_PW(client_account[0],client_account[1])
        else:
            #return 3
            ans = "Confirm password do not match."
    conn.send(ans.encode(FORMAT))
    conn.close()

def HandleClient(conn,address):
    print("Connected to ", address)
    print()
    msg = conn.recv(1024).decode(FORMAT)
    temp = " "
    conn.send(temp.encode(FORMAT))
    if msg == "Y":
        AccountCheck(conn)
    elif msg == "N":
        Signup(conn)
    #msg = conn.recv(1024).decode(FORMAT)
    #print(msg)
    #if msg == "x":
    #print("Connection with ", address, " ended")
    conn.close()

###################################### MAIN ##########################################
conx = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-S8G0HJG\SQLEXPRESS;"
    "Database=ACCOUNT;"
    "Trusted_Connection=yes;")
cursor = conx.cursor()
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM: giao thức TCP
server.bind((SERVER, PORT))

server.listen()
print("Server is waiting...")
print()

msg = ""
nClient=0
while(nClient<2):
    try:
        conn, address = server.accept()
        clientThread=threading.Thread(target=HandleClient, args=(conn, address))
        clientThread.daemon = False
        clientThread.start()
        #msg = HandleClient(conn,address)                    
    except:
        print("Client ",address, "is disconnected.") #Nếu client thoát đột ngột => chạy dòng này => server không bị treo.
        #msg = "end"
    nClient+=1
#conn.close()
input()
server.close()
