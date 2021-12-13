import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 
import pyodbc


HEADER_FONT = ("Open Sans", 16,"bold")
BUTTON_FONT = ("Open Sans", 12, "bold")
REGULAR_FONT= ("Open Sans", 12)


#option
ERROR = -1
WARNING = 0
INFO = 1


################# HÀM XỬ LÝ ###############
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
def ResultSignin():
    result = client.recv(1024).decode(FORMAT)
    if(result=="Login successfully!"):
        return 0
        #print("ID was wrong")
    elif(result=="ID does not exist."):
        return 1
        #print("Successfully!")
    elif(result=="Wrong password."):
        return 2
        #print("Password was wrong! Enter again!")
    else:
        return -1
        #print("Connection was corrupted!")
        
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

###################
def click_login(controller, client, id, pw):
    Signin(client, id, pw)
    check = ResultSignin(client)
    if check==0:
        controller.showFrame(HomePage)
    elif check==1 || check==2:
        notification(ERROR, "Wrong password or username!!!\nPlease try again.")
    else:
        notification(ERROR, "Connection was corrupted!!!")

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

        button_log = tk.Button(frame_1,text="LOG IN",font=BUTTON_FONT, bg="#6B8DF2",fg='#EBEBF2',command=lambda:click_login(controller, self.entry_user.get(), self.entry_pswd.get())) 
        button_log.configure(width=10)
        button_sign = tk.Button(frame_1,text="SIGN UP",font=BUTTON_FONT,bg="#6B8DF2",fg='floral white', command=lambda:controller.showFrame(SignUpPage)) 
        button_sign.configure(width=10)

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
        button_log.grid(row=7,column=3)

        self.label_blank_3.grid(row=8,column=3)
        button_sign.grid(row=9,column=3)

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

        button_log = tk.Button(frame_1,text="SIGN UP",font=BUTTON_FONT, bg="#6B8DF2",fg='#EBEBF2',command=lambda:controller.showFrame(HomePage)) 
        button_log.configure(width=10)
        button_sign = tk.Button(frame_1,text="LOG IN",font=BUTTON_FONT,bg="#6B8DF2",fg='floral white', command=lambda:notification(ERROR, "Wrong password or username!!!\nPlease try again.")) 
        button_sign.configure(width=10)

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
        button_log.grid(row=7,column=3)

        self.label_blank_3.grid(row=8,column=3)
        button_sign.grid(row=9,column=3)

        canvas.place(x=0,y=0)
        frame_1.place(x=320, y=30)
        ####################################################################




class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="bisque2")
        
        



app = VndEx_App()
app.mainloop()
