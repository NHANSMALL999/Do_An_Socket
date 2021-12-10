################File nháp. Đừng quan tâm file này.################
##################################################################
import socket
import pyodbc #thêm thư viện để kết nối với sql
PORT=8000
SERVER=socket.gethostbyname(socket.gethostname())
FORMAT="utf_16"

#print(pyodbc.drivers())
conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-S8G0HJG\SQLEXPRESS;"
    "Database=ACCOUNT;"
    "Trusted_Connection=yes;")
#conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=DESKTOP-S8G0HJG\SQLEXPRESS; Database=ACCOUNT; UID=nhan; PWS=123456')

cursor = conn.cursor()
temp = ""
id = "nhn"
for row in cursor.execute("select * from INFORMATION where ID = ?",id):
    #print(row.ID)
    temp = row[0]    
    print(row[0])
if(temp==id):
    print("NICE!")
else:
    print("WRONG")
    #print(row)
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
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM: giao thức TCP
server.bind((SERVER, PORT))

server.listen()
print("Server is waiting...")
print()

try:
    client, address = server.accept()
    print("Connected to ", address)
    print()
    nickname=client.recv(1024).decode(FORMAT)
    print("Nickname of the client: ", nickname)
    client.send("Connected to the server!".encode(FORMAT))
    
    while(True):
        message=client.recv(1024).decode(FORMAT)
        print("Client ", address,": ", message)
        if(message=="thanks"): #Nếu đặt break dưới 2 lệnh sau thì server sẽ phải gửi thêm 1 tin cho client 
            break              #dù client đã yêu cầu ngắt kết nối và không có nhu cầu nhận thêm tin.
            
        Answer=input("Answer: ")
        client.send(Answer.encode(FORMAT))
        
except:
   print("Client ",address, "is disconnected.") #Nếu client thoát đột ngột => chạy dòng này => server không bị treo.


client.close()
print("Connection with ", address, " ended")

server.close()


##Đọc dữ liệu
def read(connect_sql):
    print("Read")
    cursor = connect_sql.cursor()
    cursor.execute("select * from INFORMATION")
    for row in cursor:
        print(f'row={row}')
    print()

#def create()
##Kết nối với sql
##connect_sql = pyodbc.connect(
  #  "Driver={SQL Server Native Client 11.0}"
  #"Database = SQLDBQUERY;"
  #  "Trusted connection = yes"
   # )


