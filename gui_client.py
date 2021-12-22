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

#Hàm nhận danh sách
def RecieveList(client, list):
    data=""
    for i in range(5):
        data= client.recv(1024).decode(FORMAT)
        list.append(data)
        client.send(data.encode(FORMAT))
    return list

#Hàm nhận toàn bộ bảng data từ server
def GetAllDataFromServer(client,list):
    RecieveList(client, list)

#Hàm nhận data theo tên từ server
def GetSpeDataFromServer(client, list):
    RecieveList(client, list)


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

        # Cai dat nut [X]
        self.protocol("WM_DELETE_WINDOW", self.click_X)
        
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
            self.geometry("800x500")
        else:
            self.geometry("600x300")
        frame.tkraise()
        
    # Ham chuc nang nut [X]
    def click_X(self):
        if messagebox.askyesno("Exit", "Do you want to quit the app?"):
            # Them cac chuc nang khac trong nay
            client.send("0".encode(FORMAT))
            client.recv(1024)
            client.close
            ###################################
            self.destroy()


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
        button_goLogIn.configure(width=14)

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
        self.configure(bg="#6B8DF2")
        
        buttons_frame = tk.Frame(self, bg="#6B8DF2")
        buttons_frame.grid(row=0, column=0, sticky='we')    

        btn_signOut = tk.Button(buttons_frame, text='Sign out', font=("Open Sans", 10, 'bold'), fg="#164DF2", bg="#EBEBF2")
        btn_signOut.grid(row=0, column=5, padx=(10), pady=(20))

        btn_search = tk.Button(buttons_frame, text='Search', font=("Open Sans", 10, 'bold'), fg="#164DF2", bg="#EBEBF2", command=lambda:ClickSearch(client,str(clicked_1.get()),str(clicked_2.get())))
        btn_search.grid(row=0, column=2, padx=(10), pady=(20))

        # Drop down boxes

        listOption_1 = [
            "09/12/2021", 
            "10/12/2021"
        ]

        listOption_2 = [
            "All",
            "AUD",
            "CAD",
            "CHF",
            "CNY",
            "DKK",
            "EUR",
            "GBP",
            "HKD",
            "INR",
            "JPY",
            "KRW",
            "KWD",
            "MYR",
            "NOK",
            "RUB",
            "SAR",
            "SEK",
            "SGD",
            "THB",
            "USD"
        ]


        clicked_1 = tk.StringVar()
        clicked_1.set(listOption_1[0])
        #name_option_1 = tk.Label(buttons_frame, text="Day", font=("Open Sans", 10, "bold"), fg="#EBEBF2", bg="#6B8DF2")
        #name_option_1.grid(row=0, column=0)

        drop_1 = tk.OptionMenu(buttons_frame, clicked_1, *listOption_1)
        drop_1.config(font=("Open Sans", 10, 'bold'), fg="#164DF2", bg="#EBEBF2", width=15, highlightthickness=0)
        drop_1.grid(row=0, column=0, padx=(10), pady=(20))


        clicked_2 = tk.StringVar()
        clicked_2.set(listOption_2[0])
        #name_option_1 = tk.Label(buttons_frame, text="Day", font=("Open Sans", 10, "bold"), fg="#EBEBF2", bg="#6B8DF2")
        #name_option_1.grid(row=0, column=0)

        drop_2 = tk.OptionMenu(buttons_frame, clicked_2, *listOption_2)
        drop_2.config(font=("Open Sans", 10, 'bold'), fg="#164DF2", bg="#EBEBF2", width=10, highlightthickness=0)
        drop_2.grid(row=0, column=1, padx=(10), pady=(20))


        #######################################################################################################
        frame_showInfo = tk.Frame(self, bg="#6B8DF2", bd=2)
        #frame_showInfo.pack(fill='both', expand=1, padx=10, pady=10)
        frame_showInfo.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        my_canvas_top = tk.Canvas(frame_showInfo, bg="#CED0F2", width=755, height=390)
        my_canvas_top.pack(side="left", fill='both', expand=1)
        #my_canvas_top.grid(row=0, column=0, sticky='nsew')

        #Add a scrollbar to the canvas
        my_scrollbar = ttk.Scrollbar(frame_showInfo, orient='vertical', command=my_canvas_top.yview)
        my_scrollbar.pack(side='left', fill='y')

        #Configure the canvas
        my_canvas_top.configure(yscrollcommand=my_scrollbar.set)
        my_canvas_top.bind('<Configure>', lambda e: my_canvas_top.configure(scrollregion=my_canvas_top.bbox("all")))

        #Create another frame inside the canvas
        second_frame = tk.Frame(my_canvas_top)

        #Add that new frame to the window in the canvas
        my_canvas_top.create_window((0,0), window=second_frame, anchor='nw')

        ########################################################################################################
    #Nhấn nút seacrch
  
        
        
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

def ClickSearch(client,ngay, ma):
    client.send(ngay.encode(FORMAT))
    client.recv(1024)
    client.send(ma.encode(FORMAT))
    list = []
    list = RecieveList(client,list)
    print(list)


def click_finish_connection(controller, client):
    client.send("finish".encode(FORMAT))
    client.recv(1024)
    client.close()
try:
    client.connect((SERVER, PORT))
    app = VndEx_App()
    app.mainloop()

            
except: 
    print("CAN NOT CONNECT TO SERVER") #Nếu server chưa mở => không kết nối được => báo lỗi 
                                        #=> vẫn chạy dòng client.close => không bị treo
client.close()
