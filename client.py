import socket

SERVER=socket.gethostbyname(socket.gethostname())
PORT = 8000
FORMAT = "utf_16"

client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))


print("CHAT")

nickname=input("Enter your nickname: ")
client.send(nickname.encode(FORMAT))

print(client.recv(1024).decode(FORMAT))
print()
print("Start a chat")

while(True):
    message=input()
    client.send(message.encode(FORMAT))
    Answer=client.recv(1024).decode(FORMAT)
    print("Reply: ",Answer)
    if(message=="thanks"):
        break


client.close()