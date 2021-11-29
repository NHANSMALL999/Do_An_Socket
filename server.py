import socket

PORT=8000
SERVER=socket.gethostbyname(socket.gethostname())
FORMAT="utf_16"

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

server.listen()
print("Server is waiting...")
print()

client, address =server.accept()
print("Connected to ", address)
print()


nickname=client.recv(1024).decode(FORMAT)

print("Nickname of the client: ", nickname)

client.send("Connected to the server!".encode(FORMAT))


while(True):
    message=client.recv(1024).decode(FORMAT)
    print("Client ", address,": ", message)
    Answer=input("Answer: ")
    client.send(Answer.encode(FORMAT))
    if(message=="thanks"):
        break


client.close()
print("Connection with ", address, " ended")

server.close()