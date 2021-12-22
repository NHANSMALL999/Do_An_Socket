################# HÀM XỬ LÝ #####################
import socket
import threading
import pyodbc #thêm thư viện để kết nối với sql
PORT=8000
SERVER=socket.gethostbyname(socket.gethostname())
FORMAT="utf_16"

LOGIN="logIn"
SIGNUP="signUp"
table = "EXCHANGE_RATE_9_12_21"   

#Ham xu ly Login hoặc Signup
def choice(conn, sign):
    choice=conn.recv(1024).decode(FORMAT)
    conn.send(choice.encode(FORMAT))
    if(choice==LOGIN):
        #Nhan ten va password
        username=conn.recv(1024).decode(FORMAT)
        conn.send(username.encode(FORMAT))
        passw=conn.recv(1024).decode(FORMAT)
        conn.send(passw.encode(FORMAT))
        #Kiem tra thong tin va gui phan hoi cho client
        sign = AccountCheck(conn, username, passw, sign)
        
    elif(choice==SIGNUP):
        #Nhan ten, password va password again
        username=conn.recv(1024).decode(FORMAT)
        conn.send(username.encode(FORMAT))
        passw=conn.recv(1024).decode(FORMAT)
        conn.send(passw.encode(FORMAT))
       
        #Dang ky cho client
        sign = Signup(conn, username, passw,sign)
    else:
        print("end")

    return sign
        

#Hàm kiểm tra id và pw      
def AccountCheck(conn, user, pw, sign):
    conx = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-S8G0HJG\SQLEXPRESS;"
    "Database=EXCHANGE_RATE;"
    "Trusted_Connection=yes;")
    cursor = conx.cursor()
    temp = ""
    for row in cursor.execute("select PASSWORD from INFORMATION where ID = ?", user):
        #row trả về hàng chứa id. vd: ('nhan','123456')
        password = row[0] 
        temp = "checked"
    #conx.close() 
    if(temp != "checked"):
        ans = "ID does not exist."
        conn.send("1".encode(FORMAT))
    else:       
        if(pw==password):
            ans = "Login successfully!"
            sign = "0"
            conn.send("0".encode(FORMAT))
        else:
            ans = "Wrong password."
            conn.send("2".encode(FORMAT))
            
    print(ans)
    conx.close()
    return sign

#Hàm thêm id và pw vào database
def Insert_ID_PW(conx, id,pw):
    cursor = conx.cursor()
    cursor.execute("insert INFORMATION values (?,?)", id, pw)
    conx.commit() 

#Hàm đăng ký
def Signup(conn, username, passw, sign):
    conx = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-S8G0HJG\SQLEXPRESS;"
    "Database=EXCHANGE_RATE;"
    "Trusted_Connection=yes;")
    cursor = conx.cursor()
    temp = ""
    for row in cursor.execute("select * from INFORMATION where ID = ?", username):
        temp = "checked"
    if(temp == "checked"):
        ans = "ID already exists."
        conn.send("1".encode(FORMAT))
    else:
        ans = "Sign up successfully!"
        sign = "0"
        conn.send("0".encode(FORMAT))
        Insert_ID_PW(conx, username, passw)

    print(ans)
    conx.close()
    return sign

#Gửi danh sách sang client
#def SendList(conn, list):
#    for data in list:
#        conn.send(data.encode(FORMAT))
#        conn.recv(1024)

def SendList(conn, list):
    for data in list:
        conn.send(str(data).encode(FORMAT))
        conn.recv(1024)
    msg = "end"
    conn.send(msg.encode(FORMAT))

#Hàm lấy dữ liệu toàn bộ bảng theo ngày và gửi client
def GetAllData(conn, ThoiGian):
    conx = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-S8G0HJG\SQLEXPRESS;"
    "Database=EXCHANGE_RATE;"
    "Trusted_Connection=yes;")
    cursor = conx.cursor()
    list = []
    for row in cursor.execute("select TenNgoaiTe, MaNT, MuaTienMat, MuaChuyenKhoan, Ban from EXCHANGE_RATE_DATA where ThoiGian = ?",ThoiGian):
        
        list.append(row[0])
        list.append(row[1])
        list.append(row[2])
        list.append(row[3])
        list.append(row[4])
        print(list[0])
        SendList(conn, list)
    conx.close()

#Hàm lấy dữ liệu theo tên ngoại tệ và theo ngày
def GetSpeData(conn, ThoiGian, MaNT):
    conx = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-S8G0HJG\SQLEXPRESS;"
    "Database=EXCHANGE_RATE;"
    "Trusted_Connection=yes;")
    cursor = conx.cursor()
    for row in cursor.execute("select TenNgoaiTe, MaNT, MuaTienMat, MuaChuyenKhoan, Ban from EXCHANGE_RATE_DATA where ThoiGian = ? AND MaNT = ?",ThoiGian, MaNT):
        #print(row)
        list = []
        list.append(row[0])
        list.append(row[1])
        list.append(row[2])
        list.append(row[3])
        list.append(row[4])
        #print(list)
        SendList(conn, list)  
    conx.close()

def request(conn):
    date=conn.recv(1024).decode(FORMAT)
    conn.send(date.encode(FORMAT))
    mnt=conn.recv(1024).decode(FORMAT)
    print(mnt)
    if(mnt=="All"):
        GetAllData(conn, date)
    else:
        GetSpeData(conn, date, mnt)

def HandleClient(conn,address,sign):
    print("Connected to ", address)
    print()
    while(sign != "0"):
        sign = choice(conn,sign)

    request(conn)
    
    print("Connection with ", address, " ended")
    conn.close()

################# HÀM GUI #######################
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 

from tkinter import font 
from tkinter import scrolledtext 
import time

HEADER_FONT = ("Open Sans", 16,"bold")
BUTTON_FONT = ("Open Sans", 12, "bold")
REGULAR_FONT= ("Open Sans", 12)
ENTRY_FONT= ("Open Sans", 10, "bold")

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
        self.title("VndEx - server")
        self.configure(bg="#CED0F2")
        
        # Cai dat nut [X]
        self.protocol("WM_DELETE_WINDOW", self.click_X)
        
        container = tk.Frame(self)
        container.pack(side="top",fill='both',expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, HomePage):
            frame = F(container, self)

            self.frames[F] = frame 

            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(HomePage)

    def showFrame(self, container):
        frame = self.frames[container]
        if container==HomePage:
            self.geometry("900x550")
        else:
            self.geometry("600x300")
        frame.tkraise()
    
    # Ham chuc nang nut [X]
    def click_X(self):
        if messagebox.askyesno("Exit", "Do you want to quit the app?"):
            # Them cac chuc nang khac trong nay

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

        self.entry_user = tk.Entry(frame_1,width=20,bg='#EBEBF2', font=REGULAR_FONT)
        self.entry_pswd = tk.Entry(frame_1,width=20,bg='#EBEBF2', font=REGULAR_FONT)

        button_log = tk.Button(frame_1,text="LOG IN",font=BUTTON_FONT, bg="#6B8DF2",fg='#EBEBF2',command=lambda:controller.showFrame(HomePage)) 
        button_log.configure(width=10)

        #########################################################################
        canvas = tk.Canvas(self, width=230, height=300, bg='#6B8DF2', bd=0)
        canvas.create_text(113,150, text="SERVER", font=("Open Sans", 36, "bold"), fill="#EBEBF2")

        
        ## PACK
        self.label_blank_1.grid(row=0,column=2)
        label_title.grid(row=1,column=3, columnspan=3)

        label_user.grid(row=2,column=3, sticky='w')
        self.entry_user.grid(row=3,column=3, sticky='nsew')

        label_pswd.grid(row=4,column=3, sticky='w')
        self.entry_pswd.grid(row=5,column=3, sticky='nsew')

        self.label_blank_2.grid(row=6,column=3)
        button_log.grid(row=7,column=3)

        canvas.place(x=0,y=0)
        frame_1.place(x=320, y=30)
        ####################################################################



class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        self.configure(bg="#FFFFFF")

        self.run = False

        # Main frame
        frame_top = tk.Frame(self, bg="#FFFFFF", height=50, width=880)
        frame_top.grid(row=0, column=0, padx=5, pady=10, sticky='e')

        frame_options = tk.LabelFrame(self, text = "Options", font=("Open Sans", 12, 'bold'), bg="#FFFFFF", fg="#000000", bd=3, height=100, width=880)
        frame_options.grid(row=1, column=0, padx=0, pady=5, sticky='e')

        frame_show = tk.LabelFrame(self, bg="#FFFFFF", height=300, width=880, bd=3)
        frame_show.grid(row=2, column=0, padx=0, ipady=5, sticky='e')

        
        # Frame top --------------------------------------
        button_logOut = tk.Button(frame_top, text="Log out", font=("Open Sans", 12, 'bold'), fg="#000000", bg="#FFFFFF")
        button_logOut.place(x=770, y=15)

        # Frame options --------------------------------------
        button_run = tk.Button(frame_options, text="Run", font=("Open Sans", 10, 'bold'), fg="#000000", bg="#FFFFFF", command=lambda:self.click_run(controller))
        button_run.config(height=0, width=12)
        button_run.place(x=550, y=25)

        button_stop = tk.Button(frame_options, text="Stop", font=("Open Sans", 10, 'bold'), fg="#000000", bg="#FFFFFF", command=lambda:self.click_stop(controller))
        button_stop.config(height=0, width=12)
        button_stop.place(x=700, y=25)

        canvas_name_option = tk.Canvas(frame_options, bg="#FFFFFF", height=20, width=340, highlightthickness=0)
        ##
        canvas_name_option.create_text(133,12,text="IP address",font=("Arial", 10, 'bold'),fill="#000000")
        canvas_name_option.create_text(283,12,text="Port",font=("Open Sans", 10, 'bold'),fill="#000000")
        ##
        canvas_name_option.place(x=0, y=6)

        self.entry_ip = tk.Entry(frame_options, width=13 ,bg='#F2F2F2', font=REGULAR_FONT, bd=2)
        self.entry_ip.place(x=100, y=30)

        self.entry_port = tk.Entry(frame_options, width=9,bg='#F2F2F2', font=REGULAR_FONT, bd=2)
        self.entry_port.place(x=270, y=30)

        # Frame show --------------------------------------
        self.text_show = scrolledtext.ScrolledText(frame_show, bd=0)
        self.text_show.configure(state='disable', font=("Arial", 10, 'bold'), width=122, height=21)
        self.text_show.pack()

        # Default run -------------------------------------
        self.print_default_IP_Port()
        self.print_show_server_close()
        ############################################################################
    def client_login(self, ip, port, username):
        self.print_show_client_login(ip, port, username)

    def click_restart(self):
        pass
    
    def click_logout(self):
        pass

    def click_stop(self, controller):
        if self.run:
            self.run = False
            self.delay(controller, float(0.5))
            self.clear_text_show()
            self.print_show_server_close()
            self.close_server()
            
    def click_run(self, controller):
        if self.run == False:
            self.run = True
            self.clear_text_show()
            self.print_show_server_start()

            #self.run_server()
            server.bind((SERVER, PORT))
            server.listen()
            print("Server is waiting...")
            print()
            sign = ""
            conn, address = server.accept()
            print("client is connected")
            #self.print_show_client_login("Client is connected")
            self.print_show_client_logout(address[0], address[1], "tuan123")

    def close_server(self):
        pass

    def run_server(self):
        server.bind((SERVER, PORT))
        server.listen()
        print("Server is waiting...")
        
       



    def log_out(self):
        pass

    def delay(self, controller, second):
        controller.after(int(second*1000))

    def clear_text_show(self):
        self.text_show.configure(state='normal')
        self.text_show.delete(1.0, tk.END)
        self.text_show.configure(state='disable')

    def print_show_server_start(self):
        self.text_show.configure(state='normal')
        self.text_show.insert('insert', f"[Server][Opened]     IP:{self.entry_ip.get()} - Port:{self.entry_port.get()}\n")
        self.text_show.configure(state='disable')

    def print_show_server_close(self):
        self.text_show.configure(state='normal')
        self.text_show.insert('insert', "[Server][Closed]\n")
        self.text_show.configure(state='disable')

    def print_show_client_login(self, ip, port, username):
        self.text_show.configure(state='normal')
        self.text_show.insert('insert', f"[Client][Logged in]   IP:{ip} - Port:{port} - User:{username}\n")
        self.text_show.configure(state='disable')

    def print_show_client_logout(self, ip, port, username):
        self.text_show.configure(state='normal')
        self.text_show.insert('insert', f"[Client][Logged out] IP:{ip} - Port:{port} - User:{username}\n")
        self.text_show.configure(state='disable')

    def print_default_IP_Port(self):
        self.entry_ip.insert(0, "127.0.0.1")
        self.entry_port.insert(0, "8888")
        
        


############################################# HÀM MAIN ##################################################
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM: giao thức TCP

#nClient=0
t = """
while(nClient<2):
    try:
       

        conn, address = server.accept()
        clientThread=threading.Thread(target=HandleClient, args=(conn, address, sign))
        clientThread.daemon = False
        clientThread.start()
                                   
    except:
        print("Client ",address, "is disconnected.") #Nếu client thoát đột ngột => chạy dòng này => server không bị treo.
        
    nClient+=1

input()
print("End")
"""


app = VndEx_App()
app.mainloop()
server.close()
HandleClient(conn,address,sign)
