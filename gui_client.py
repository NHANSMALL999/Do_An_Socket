#Hàm xử lý
import socket
import threading
SERVER=socket.gethostbyname(socket.gethostname())
PORT = 8000
FORMAT = "utf_16"
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM: giao thức TCP
        

#Hàm cho GUI
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 


HEADER_FONT = ("Open Sans", 16,"bold")
BUTTON_FONT = ("Open Sans", 12, "bold")
REGULAR_FONT= ("Open Sans", 12)


#option
ERROR = -1
WARNING = 0
INFO = 1


##################
def notification(type, message):
    if type == ERROR:
        messagebox.showerror("Error", message)
    elif type == WARNING:
        messagebox.showwarning("Warning", message)
    else:
        messagebox.showinfo("Info", message)


class VndEx_App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("400x300")
        self.resizable(width=False, height=False)
        self.title("VndEx - Client")
        self.configure(bg="#CED0F2")

        container = tk.Frame(self)
        container.pack(side="top",fill='both',expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, SignUpPage, HomePage):
            frame = F(container, self)

            self.frames[F] = frame 

            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(StartPage)

    def showFrame(self, container):
        frame = self.frames[container]
        if container==HomePage:
            self.geometry("700x500")
        else:
            self.geometry("600x300")
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#CED0F2")
        self.pack()

        #FRAME 1 
        frame_1 = tk.Frame(self, bd=0, relief='flat')
        frame_1.configure(bg="#CED0F2")

        label_title = tk.Label(frame_1, text="LOG IN PAGE", font=HEADER_FONT,fg='#164DF2',bg="#CED0F2")
        label_user = tk.Label(frame_1, text="username",fg='#164DF2',bg="#CED0F2",font=REGULAR_FONT)
        label_user.config(anchor='center')
        label_pswd = tk.Label(frame_1, text="password",fg='#164DF2',bg="#CED0F2",font=REGULAR_FONT)

        self.label_blank_1 = tk.Label(frame_1,text="",bg="#CED0F2")
        self.label_blank_2 = tk.Label(frame_1,text="",bg="#CED0F2")
        self.label_blank_3 = tk.Label(frame_1,text="",bg="#CED0F2")

        self.entry_user = tk.Entry(frame_1,width=20,bg='#EBEBF2', font=REGULAR_FONT)
        self.entry_pswd = tk.Entry(frame_1,width=20,bg='#EBEBF2', font=REGULAR_FONT)

        
        button_logIn = tk.Button(frame_1,text="LOG IN",font=BUTTON_FONT, bg="#6B8DF2",fg='#EBEBF2',command=lambda:click_login(controller, client, str(self.entry_user.get()), str(self.entry_pswd.get()))) 
        button_logIn.configure(width=10)
        button_goSignUp = tk.Button(frame_1,text="GO TO SIGN UP",font=("Open Sans", 10, "bold"),bg="#6B8DF2",fg='floral white', command=lambda:controller.showFrame(SignUpPage)) 
        button_goSignUp.configure(width=15)

        #########################################################################
        canvas = tk.Canvas(self, width=230, height=300, bg='#6B8DF2', bd=0)
        canvas.create_text(110,150, text="CLIENT", font=("Open Sans", 36, "bold"), fill="#EBEBF2")

        
        ## PACK
        self.label_blank_1.grid(row=1,column=2)
        label_title.grid(row=1,column=3, columnspan=3)

        label_user.grid(row=2,column=3, sticky='w')
        self.entry_user.grid(row=3,column=3, sticky='nsew')

        label_pswd.grid(row=4,column=3, sticky='w')
        self.entry_pswd.grid(row=5,column=3, sticky='nsew')

        self.label_blank_2.grid(row=6,column=3)
        button_logIn.grid(row=7,column=3)

        self.label_blank_3.grid(row=8,column=3)
        button_goSignUp.grid(row=9,column=3)

        canvas.place(x=0,y=0)
        frame_1.place(x=320, y=30)
        ####################################################################


class SignUpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#CED0F2")
        # ? khong dung pack() o day duoc?
        #self.pack()

        #FRAME 1 
        frame_1 = tk.Frame(self, bd=0, relief='flat')
        frame_1.configure(bg="#CED0F2")

        label_title = tk.Label(frame_1, text="SIGN UP PAGE", font=HEADER_FONT,fg='#164DF2',bg="#CED0F2")
        label_user = tk.Label(frame_1, text="username",fg='#164DF2',bg="#CED0F2",font=REGULAR_FONT)
        label_user.config(anchor='center')
        label_pswd = tk.Label(frame_1, text="password",fg='#164DF2',bg="#CED0F2",font=REGULAR_FONT)

        self.label_blank_1 = tk.Label(frame_1,text="",bg="#CED0F2")
        self.label_blank_2 = tk.Label(frame_1,text="",bg="#CED0F2")
        self.label_blank_3 = tk.Label(frame_1,text="",bg="#CED0F2")

        self.entry_user = tk.Entry(frame_1,width=20,bg='#EBEBF2', font=REGULAR_FONT)
        self.entry_pswd = tk.Entry(frame_1,width=20,bg='#EBEBF2', font=REGULAR_FONT)

        #id = self.entry_user.get()
        #pw = self.entry_pswd.get()

        button_signUp = tk.Button(frame_1,text="SIGN UP",font=BUTTON_FONT, bg="#6B8DF2",fg='#EBEBF2',command=lambda:click_signup(controller, client, str(self.entry_user.get()), str(self.entry_pswd.get()))) 

        button_signUp.configure(width=10)
        button_goLogIn = tk.Button(frame_1,text="GO TO LOG IN",font=("Open Sans", 10, "bold"),bg="#6B8DF2",fg='floral white', command=lambda:controller.showFrame(StartPage)) 
        button_goLogIn.configure(width=15)

        #########################################################################
        canvas = tk.Canvas(self, width=230, height=300, bg='#6B8DF2', bd=0)
        canvas.create_text(110,150, text="CLIENT", font=("Open Sans", 36, "bold"), fill="#EBEBF2")

        
        ## PACK
        self.label_blank_1.grid(row=1,column=2)
        label_title.grid(row=1,column=3, columnspan=3)

        label_user.grid(row=2,column=3, sticky='w')
        self.entry_user.grid(row=3,column=3, sticky='nsew')

        label_pswd.grid(row=4,column=3, sticky='w')
        self.entry_pswd.grid(row=5,column=3, sticky='nsew')

        self.label_blank_2.grid(row=6,column=3)
        button_signUp.grid(row=7,column=3)

        self.label_blank_3.grid(row=8,column=3)
        button_goLogIn.grid(row=9,column=3)

        canvas.place(x=0,y=0)
        frame_1.place(x=320, y=30)
        ####################################################################


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="bisque2")
        
###################
def click_login(controller, client, id, pw):
    try:
        #Gui lua chon
        client.send("logIn".encode(FORMAT))
        client.recv(1024)
        #Gui username
        client.send(id.encode(FORMAT))
        client.recv(1024)
        #Gui password
        client.send(pw.encode(FORMAT))
        client.recv(1024)
    
        check = int(client.recv(1024).decode(FORMAT))
        if check==0:
            controller.showFrame(HomePage)
        elif check==1:
            notification(ERROR, "Wrong username!!!\nPlease try again.")
        elif check==2:
            notification(ERROR, "Wrong password!!!\nPlease try again.")
        else:
            notification(ERROR, "Connection was corrupted!!!")
    except:
        notification(ERROR, "Connection was corrupted!!!")
           
def click_signup(controller, client, id, pw):
    try:
        #Gui lua chon
        client.send("signUp".encode(FORMAT))
        client.recv(1024)
        #Gui username
        client.send(id.encode(FORMAT))
        client.recv(1024)
        #Gui password
        client.send(pw.encode(FORMAT))
        client.recv(1024)

        check=int(client.recv(1024).decode(FORMAT))
        if check==0:
            controller.showFrame(HomePage)
        elif check==1:
            notification(ERROR, "User has already existed!!!\nPlease choose other user.")

        else:
             notification(ERROR, "Connection was corrupted!!!")
    except: 
        notification(ERROR, "Connection was corrupted!!!")
try:
    client.connect((SERVER, PORT))
    app = VndEx_App()
    app.mainloop()

            
except: 
    print("CAN NOT CONNECT TO SERVER") #Nếu server chưa mở => không kết nối được => báo lỗi 
                                        #=> vẫn chạy dòng client.close => không bị treo
client.close()
