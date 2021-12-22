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
a = """
def RecieveList(client, list):
    data=""
    for i in range(5):
        data= client.recv(1024).decode(FORMAT)
        list.append(data)
        client.send(data.encode(FORMAT))
    return list
"""

#Hàm nhận danh sách
def RecieveList(client, list):
    list = []
    data = ""
    data= client.recv(1024).decode(FORMAT)
    while(data!="end"):
        list.append(data)
        client.send(data.encode(FORMAT))
        data= client.recv(1024).decode(FORMAT)
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
            self.geometry("1000x500")
        else:
            self.geometry("600x300")
        frame.tkraise()
        
    # Ham chuc nang nut [X]
    def click_X(self):
        if messagebox.askyesno("Exit", "Do you want to quit the app?"):
            # Them cac chuc nang khac trong nay
            try:
                client.send("0".encode(FORMAT))
                client.recv(1024)
                client.close
                ###################################
                self.destroy()
            except:
                client.close()
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
        self.configure(bg="#FFFFFF")
        self.contacts = []
        
        # Main frame ----------------------------------------------------------
        frame_top = tk.Frame(self, bg="#FFFFFF", height=50, width=980)
        frame_top.grid(row=0, column=0, padx=5, pady=5)
        
        frame_options = tk.LabelFrame(self, text = "Options", font=("Open Sans", 12, 'bold'), bg="#FFFFFF", fg="#000000", bd=3, height=100, width=970)
        frame_options.grid(row=1, column=0, padx=15, pady=0, sticky='w')
        
        frame_show = tk.LabelFrame(self, bg="#FFFFFF", height=500, width=980)
        frame_show.grid(row=2, column=0, padx=5, pady=5)

        # frame top ----------------------------------------------------------
        button_logOut = tk.Button(frame_top, text="Log out", font=("Open Sans", 12, 'bold'), fg="#000000", bg="#FFFFFF")
        button_logOut.place(x=870, y=15)

        # frame options ----------------------------------------------------------
        button_search = tk.Button(frame_options, text="Search", font=("Open Sans", 10, 'bold'), fg="#000000", bg="#FFFFFF", command=lambda:self.ClickSearch(client,str(click_list_day.get()),str(click_list_type.get())))
        button_search.config(height=0, width=12)
        button_search.place(x=520, y=26)

        button_clear = tk.Button(frame_options, text="Clear", font=("Open Sans", 10, 'bold'), fg="#000000", bg="#FFFFFF")
        button_clear.config(height=0, width=12)
        button_clear.place(x=670, y=26)

        list_day = [
            "09/12/2021", 
            "10/12/2021"
        ]

        list_type = [
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

        click_list_day = tk.StringVar()
        click_list_day.set(list_day[0])
        
        canvas_name_option = tk.Canvas(frame_options, bg="#FFFFFF", height=20, width=340, highlightthickness=0)
        ##
        canvas_name_option.create_text(112,10,text="Day",font=("Open Sans", 10, 'bold'),fill="#000000")
        canvas_name_option.create_text(315,10,text="Type",font=("Open Sans", 10, 'bold'),fill="#000000")
        ##
        canvas_name_option.place(x=0, y=6)

        dropBox_day = tk.OptionMenu(frame_options, click_list_day, *list_day)
        dropBox_day.config(font=("Open Sans", 10, 'bold'), fg="#000000", bg="#FFFFFF", width=15, highlightthickness=0)
        dropBox_day.place(x=100, y=27)

        click_list_type = tk.StringVar()
        click_list_type.set(list_type[0])

        dropBox_type = tk.OptionMenu(frame_options, click_list_type, *list_type)
        dropBox_type.config(font=("Open Sans", 10, 'bold'), fg="#000000", bg="#FFFFFF", width=10, highlightthickness=0)
        dropBox_type.place(x=300, y=27)

        # frame show ----------------------------------------------------------
        self.treeView_show = ttk.Treeview(frame_show, column=(1,2,3,4,5), show="headings", height=19)
        self.treeView_show.grid(row=0, column=0, sticky='nsew')

        self.treeView_show.column("# 1", anchor='center', width=200)
        self.treeView_show.column("# 2", anchor='center', width=150)
        self.treeView_show.column("# 3", anchor='center', width=200)
        self.treeView_show.column("# 4", anchor='center', width=200)
        self.treeView_show.column("# 5", anchor='center', width=200)

        self.treeView_show.heading(1, text="Tên ngoại tệ")
        self.treeView_show.heading(2, text="Mã ngoại tệ")
        self.treeView_show.heading(3, text="Mua tiền mặt")
        self.treeView_show.heading(4, text="Mua chuyển khoản")
        self.treeView_show.heading(5, text="Bán")

        # Add Scrollbar
        scrollbar = ttk.Scrollbar(frame_show, orient=tk.VERTICAL, command=self.treeView_show.yview)
        self.treeView_show.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Create Example data

        
        #contacts.append((f'Ten {n}', f'Ma {n}', f'1010{n}', f'1000{n}', f'1100{n}'))

        # Add Example data to table
        #for contact in self.contacts:
   
    ###############################################################################
    def ClickSearch(self,client,ngay, ma):
        client.send(ngay.encode(FORMAT))
        client.recv(1024)
        client.send(ma.encode(FORMAT))
        list = []
        list = RecieveList(client,list)
        print(list)
        self.contacts = list
        print(self.contacts)
        self.treeView_show.insert('', tk.END, values=self.contacts)

    def click_clear(self):
        pass

    def click_search(self):
        pass

    def click_log_out(self):
        pass
  
        
        
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
