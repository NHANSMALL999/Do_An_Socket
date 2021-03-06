import socket
import threading
import pyodbc #thêm thư viện để kết nối với sql
PORT=8000
SERVER=socket.gethostbyname(socket.gethostname())
FORMAT="utf_16"

LOGIN="logIn"
SIGNUP="signUp"
table = "EXCHANGE_RATE_9_12_21"   

#Ham xu ly Login hoặc Signup
def choice(conn):
    choice=conn.recv(1024).decode(FORMAT)
    conn.send(choice.encode(FORMAT))
    if(choice==LOGIN):
        #Nhan ten va password
        username=conn.recv(1024).decode(FORMAT)
        conn.send(username.encode(FORMAT))
        passw=conn.recv(1024).decode(FORMAT)
        conn.send(passw.encode(FORMAT))
        #Kiem tra thong tin va gui phan hoi cho client
        AccountCheck(conn, username, passw)
    elif(choice==SIGNUP):
        #Nhan ten, password va password again
        username=conn.recv(1024).decode(FORMAT)
        conn.send(username.encode(FORMAT))
        passw=conn.recv(1024).decode(FORMAT)
        conn.send(passw.encode(FORMAT))
       
        #Dang ky cho client
        Signup(conn, username, passw)
        

#Hàm kiểm tra id và pw      
def AccountCheck(conn, user, pw):
    temp = ""
    for row in cursor.execute("select PASSWORD from INFORMATION where ID = ?", user):
        #row trả về hàng chứa id. vd: ('nhan','123456')
        password = row[0] 
        temp = "checked"
    #conx.close() 
    if(temp != "checked"):
        ans = "ID does not exist."
        conn.send("1".encode(FORMAT))
    else:       
        if(pw==password):
            ans = "Login successfully!"
            sign = "0"
            conn.send("0".encode(FORMAT))
        else:
            ans = "Wrong password."
            conn.send("2".encode(FORMAT))
            
    print(ans)

#Hàm thêm id và pw vào database
def Insert_ID_PW(id,pw):
    cursor = conx.cursor()
    cursor.execute("insert INFORMATION values (?,?)", id, pw)
    conx.commit() 

#Hàm đăng ký
def Signup(conn, username, passw):
    temp = ""
    for row in cursor.execute("select * from INFORMATION where ID = ?", username):
        temp = "checked"
    if(temp == "checked"):
        ans = "ID already exists."
        conn.send("1".encode(FORMAT))
    else:
        ans = "Sign up successfully!"
        sign = "0"
        conn.send("0".encode(FORMAT))
        Insert_ID_PW(username, passw)

    print(ans)

#Gửi danh sách sang client
def SendList(conn, list):
    for data in list:
        conn.send(str(data).encode(FORMAT))
        conn.recv(1024)
    msg = "end"
    conn.send(msg.encode(FORMAT))
#Hàm lấy dữ liệu toàn bộ bảng và gửi clien
def GetAllData(conn):
    for row in cursor.execute("select * from ? where ID = ?", table, user):
        list = []
        list.append(row[0])
        list.append(row[1])
        list.append(row[2])
        list.append(row[3])
        list.append(row[4])
        print(list)
        SendList(list)

#Hàm lấy dữ liệu theo tên ngoại tệ
def GetSpeData(conn):
    for row in cursor.execute("select MaNT, MuaTienMat, MuaChuyenKhoan, Ban from EXCHANGE_RATE_9_12_21 where TenNgoaiTe = ?",TenNgoaiTe):
        #print(row)
        list = []
        list.append(row[0])
        list.append(row[1])
        list.append(row[2])
        list.append(row[3])
        print(list)
        SendList(list)


def HandleClient(conn,address):
    print("Connected to ", address)
    print()
    while(sign != "0"):
        choice(conn)
    GetData(conn)
    print("Connection with ", address, " ended")
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


nClient=0
sign = ""
while(nClient<2):
    try:
        conn, address = server.accept()
        clientThread=threading.Thread(target=HandleClient, args=(conn, address))
        clientThread.daemon = False
        clientThread.start()
                                   
    except:
        print("Client ",address, "is disconnected.") #Nếu client thoát đột ngột => chạy dòng này => server không bị treo.
        
    nClient+=1

input()
print("End")
server.close()
