import socket
import threading
SERVER=socket.gethostbyname(socket.gethostname())
PORT = 8000
FORMAT = "utf_16"
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM: giao thức TCP

#Hàm gửi danh sách
def SendList(client, list):
    for data in list:
        client.send(data.encode(FORMAT))
        client.recv(1024)
    msg = "end"
    client.send(msg.encode(FORMAT))

#Hàm đăng nhập
def Signin(client,id, pw):
    list = []
    #id = input("ID: ")
    list.append(id)
    #pw = input("Password: ")
    list.append(pw)
    SendList(client,list)
#Hàm đăng ký
def Signup(client):
    list = []
    id = input("ID: ")
    list.append(id)
    pw = input("Password: ")
    list.append(pw)
    pwa = input("Input password again: ")
    list.append(pwa)
    SendList(client,list)


#Hàm nhận kết quả đăng nhập
def ResultSignin(result):
    result = client.recv(1024).decode(FORMAT)
    if(result=="ID does not exist."):
        #return 1
        print("ID was wrong")
    elif(result=="Login successfully!"):
        #return 2
        print("Successfully!")
    elif(result=="Wrong password."):
        #return 3
        print("Password was wrong! Enter again!")
    else:
        #return 4
        print("Connection was corrupted!")
        
#Hàm nhận kết quả đăng ký
def ResultSignup(client):
    result = client.recv(1024).decode(FORMAT)
    if(result=="ID already exists."):
        #return 1
        print("ID already exists. Please choose other ID")
    elif(result == "Successfully!"):
        #return 2
        print("Sign up successfully! Sign in now!")
    elif(result=="Confirm password do not match."):
        #return 3
        print("Confirm password do not match. Enter again!")


####################################### MAIN #############################################
end = ""    
try:
    client.connect((SERVER, PORT))
    print("Connect successfully!")
    print("Do you have an account? {Y/N]")
    temp =  input()
    if temp == "Y":
        client.send(temp.encode(FORMAT))
        client.recv(1024)
        Signin(client)
        #result = client.recv(1024).decode(FORMAT)
        ResultSignin(client)
    elif temp == "N":
        client.send(temp.encode(FORMAT))
        client.recv(1024)
        Signup(client)
        ResultSignup(client)
    else:
        print("Wrong input!")
    
    message = ""    
    #while(message != "x"):      
    message=input("press any key to end: ")
    client.send(message.encode(FORMAT))

        
except: 
    print("CAN NOT CONNECT TO SERVER") #Nếu server chưa mở => không kết nối được => báo lỗi 
                                       #=> vẫn chạy dòng client.close => không bị treo
client.close()