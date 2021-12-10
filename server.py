import socket
import pyodbc #thêm thư viện để kết nối với sql
PORT=8000
SERVER=socket.gethostbyname(socket.gethostname())
FORMAT="utf_16"

#Hàm nhận danh sách từ client
def RecieveList(conn):
    list = []
    data = None
    while(data!="end"):
        
        list.append(data)
        conn.send(data.encode(FORMAT))
        data= conn.recv(1024).decode(FORMAT)
    return list
    print("recieve:")
    print(list)

#Hàm kiểm tra id và pw
def AccountCheck(id,pw):
    conx = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-S8G0HJG\SQLEXPRESS;"
    "Database=ACCOUNT;"
    "Trusted_Connection=yes;")
    temp = ""
    account = RecieveList(conn)
    cursor = conx.cursor()
    for row in cursor.execute("select PASSWORD from INFORMATION where ID = ?",id):
        result = cursor.fetchone()
        password = result[0]
        temp = account[0]

    if(temp != account[0]):
        return 1
        #ans = "ID does not exist."
    else:       
        if(accoun[1]==passord):
            return 2
            #ans = "Login successfully!"
        else:
            return 3
            #ans = "Wrong password."
    #conn.send(ans.encode(FORMAT
    conx.close()    
    
#Hàm đăng ký
def Signup(id,pw,pwa):
    conx = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-S8G0HJG\SQLEXPRESS;"
    "Database=ACCOUNT;"
    "Trusted_Connection=yes;")
    temp = ""
    account = RecieveList(conn)
    cursor = conx.cursor()
    for row in cursor.execute("select * from INFORMATION where ID = ?",id):
        result = cursor.fetchone() 
        temp = account[0]
    if(temp == account[0]):
        return 1
        #ans = "ID already exists."
    else:       
        if(pw==pwa):
            return 2
            #ans = "Successfully!"
        else:
            return 3
            #ans = "Confirm password do not match."
    #conn.send(ans.encode(FORMAT))
    conx.close()

#Hàm thêm id và pw vào database
def Insert_ID_PW(id,pw):
    conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-S8G0HJG\SQLEXPRESS;"
    "Database=ACCOUNT;"
    "Trusted_Connection=yes;")
    cursor = conn.cursor()
    cursor.execute("insert INFORMATION values (?,?)", id, pw)
    conn.commit()   
    conn.close()

###################################### MAIN ##########################################
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM: giao thức TCP
server.bind((SERVER, PORT))

server.listen()
print("Server is waiting...")
print()

try:
    conn, address = server.accept()
    print("Connected to ", address)
    print()
    #nickname=client.recv(1024).decode(FORMAT)
    #print("Nickname of the client: ", nickname)
    conn.send("Connected to the server! Do you have an account? [Y/N]".encode(FORMAT))
    
    while(True):
        message=conn.recv(1024).decode(FORMAT)
        if(message=="Y"):
            #Gửi yêu cầu nhập ID và nhận ID client trả về
            Answer = "Enter ID:"
            conn.send(Answer.encode(FORMAT))
            id = conn.recv(1024).decode(FORMAT)
            print(id)
            
            #Gửi yêu cầu client nhập pw và nhận pw trả về 
            Answer = "Enter Password: "
            conn.send(Answer.encode(FORMAT))
            pw = conn.recv(1024).decode(FORMAT)
            print(pw)
            
            #Kiểm tra id, pw và gửi kết quả cho client.
            temp = AccountCheck(id,pw)
            print(temp)

        elif(message=="N"):
            Answer = "Create ID:"
            conn.send(Answer.encode(FORMAT))
            id = conn.recv(1024).decode(FORMAT)
            print(id)
            
            #Gửi yêu cầu client nhập pw và nhận pw trả về 
            Answer = "Enter Password: "
            conn.send(Answer.encode(FORMAT))
            pw = conn.recv(1024).decode(FORMAT)
            print(pw)

            #gửi yêu cầu nhập lại mật khẩu
            Answer = "Enter Password again."
            conn.send(Answer.encode(FORMAT))
            pw = conn.recv(1024).decode(FORMAT)
            print(pwa)

            #Kiểm tra id, pw và gửi kết quả cho client.
            temp =  Signup(id,pw,pwa) 
            print(temp)
            

        elif(message=="quit"):   #Nếu đặt break dưới 2 lệnh sau thì server sẽ phải gửi thêm 1 tin cho client 
            break              #dù client đã yêu cầu ngắt kết nối và không có nhu cầu nhận thêm tin.
            
        
        
except:
   print("Client ",address, "is disconnected.") #Nếu client thoát đột ngột => chạy dòng này => server không bị treo.


conn.close()
print("Connection with ", address, " ended")
server.close()
#conn = pyodbc.connect(
#   "Driver={ODBC Driver 17 for SQL Server};"
#    "Server=DESKTOP-S8G0HJG\SQLEXPRESS;"
#    "Database=ACCOUNT;"
#    "Trusted_Connection=yes;")

#cursor = conn.cursor()

#for row in cursor.execute("select * from INFORMATION where ID = 'phanthiennhan'"):
#   print(row.ID)
#   print(row[0])
#   print(row)

#cursor.execute("select * from INFORMATION")
#data = cursor.fetchall()
#print(data)
#print(data[1][0])
#print(data[1][1])

#cursor.execute("insert INFORMATION values ('test','321')") #thêm id và pass vào database
#conn.commit()  #lưu lại thông tin được insert

#id = 'abc'
#pw = '111'
#cursor.execute("insert INFORMATION values (?,?)", id, pw)
#conn.commit()   
#conn.close()

#server.close()



