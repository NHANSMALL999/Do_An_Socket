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
def choice(conn,sign):
    choice=conn.recv(1024).decode(FORMAT)
    conn.send(choice.encode(FORMAT))
    if(choice==LOGIN):
        #Nhan ten va password
        username=conn.recv(1024).decode(FORMAT)
        conn.send(username.encode(FORMAT))
        passw=conn.recv(1024).decode(FORMAT)
        conn.send(passw.encode(FORMAT))
        #Kiem tra thong tin va gui phan hoi cho client
        sign = AccountCheck(conn, username, passw,sign)
        
    elif(choice==SIGNUP):
        #Nhan ten, password va password again
        username=conn.recv(1024).decode(FORMAT)
        conn.send(username.encode(FORMAT))
        passw=conn.recv(1024).decode(FORMAT)
        conn.send(passw.encode(FORMAT))
       
        #Dang ky cho client
        sign = Signup(conn, username, passw,sign)
    else:
        print("end")

    return sign
        

#Hàm kiểm tra id và pw      
def AccountCheck(conn, user, pw, sign):
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
    return sign

#Hàm thêm id và pw vào database
def Insert_ID_PW(id,pw):
    cursor = conx.cursor()
    cursor.execute("insert INFORMATION values (?,?)", id, pw)
    conx.commit() 

#Hàm đăng ký
def Signup(conn, username, passw,sign):
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
    return sign

#Gửi danh sách sang client
def SendList(conn, list):
    for data in list:
        conn.send(data.encode(FORMAT))
        conn.recv(1024)

#Hàm lấy dữ liệu toàn bộ bảng theo ngày và gửi client
def GetAllData(conn, ThoiGian):
    for row in cursor.execute("select * from EXCHANGE_RATE_DATA where ThoiGian = ?",ThoiGian):
        list = []
        list.append(row[0])
        list.append(row[1])
        list.append(row[2])
        list.append(row[3])
        list.append(row[4])
        list.append(row[5])
        #print(list)
        SendList(list)

#Hàm lấy dữ liệu theo tên ngoại tệ và theo ngày
def GetSpeData(conn, ThoiGian, MaNT):
    for row in cursor.execute("select TenNgoaiTe, MaNT, MuaTienMat, MuaChuyenKhoan, Ban from EXCHANGE_RATE_DATA where ThoiGian = ? AND MaNT = ?",ThoiGian, MaNT):
        #print(row)
        list = []
        list.append(row[0])
        list.append(row[1])
        list.append(row[2])
        list.append(row[3])
        #print(list)
        SendList(list)  


def request(conn):
    date=conn.recv(1024).decode(FORMAT)
    conn.send(date.encode(FORMAT))
    mnt=conn.recv(1024).decode(FORMAT)
    print(mnt)
    if(mnt=="All"):
        GetAllData(conn,date)
    else:
        GetSpeData(conn, date, mnt)

def HandleClient(conn,address,sign):
    print("Connected to ", address)
    print()
    while(sign != "0"):
        sign = choice(conn,sign)
  
    request(conn)
    
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

sign = ""
nClient=0
conn, address = server.accept()
HandleClient(conn,address,sign)
server.close()

t = """
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
"""
