import socket
import threading
SERVER=socket.gethostbyname(socket.gethostname())
PORT = 8000
FORMAT = "utf_16"
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM: giao thức TCP

#Hàm gửi danh sách
def SendList(client, list):
    for element in list:
        client.send(data.encode(FORMAT))
        client.recv(1024).decode(FORMAT)
    msg = "end"
    client.send(msg.encode(FORMAT))

#Hàm yêu cầu nhập id và pw
def Signin(client):
    account = []
    id = input("ID: ")
    pw = input("Password: ")
    account.append(id)
    account.append(pw)
    SendList(client,list)

#Hàm nhận kết quả đăng nhập
def ResultSignin(client):
    result = client.recv(1024).encode(FORMAT)
    if(result=="ID does not exist."):
        return 1
        #print("ID was wrong)
    elif(result=="Login successfully!"):
        return 2
        #print("Successfully!)"
    elif(result=="Wrong password."):
        return 3
        #print("Password was wrong! Enter again!"
    else:
        return 4
        #print("Connection was corrupted!"
        
#Hàm nhận kết quả đăng ký
def ResultSignup(client):
    result = client.recv(1024).encode(FORMAT)
    if(result=="ID already exists."):
        return 1
        #print("Please choose other ID)
    elif(result == "Successfully!"):
        return 2
        #print("Sign up successfully! Sign in now!")
    elif(result=="Confirm password do not match."):
        return 3
        #print("Confirm password do not match. Enter again!")

####################################### MAIN #############################################
try:
    client.connect((SERVER, PORT))
    print("CHAT")
    #nickname=input("Enter your nickname: ")
    #client.send(nickname.encode(FORMAT))
    #client.send()
    print(client.recv(1024).decode(FORMAT))
    print()
    while(True):
        message=input()
        client.send(message.encode(FORMAT))
        Answer=client.recv(1024).decode(FORMAT)
        print(Answer)
        if(message=="quit"):
            break
        
except: 
    print("CAN NOT CONNECT TO SERVER") #Nếu server chưa mở => không kết nối được => báo lỗi 
                                       #=> vẫn chạy dòng client.close => không bị treo
client.close()
