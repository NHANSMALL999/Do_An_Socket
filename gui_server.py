################# HÀM XỬ LÝ #####################
import socket
import threading
import pyodbc #thêm thư viện để kết nối với sql
from bs4 import BeautifulSoup #Hiển thị data dưới dạng xml
import requests #Gửi yêu cầu đến web
import time #set thời gian

PORT=8000
SERVER=socket.gethostbyname(socket.gethostname())
FORMAT="utf_16"

LOGIN="logIn"
SIGNUP="signUp"
table = "EXCHANGE_RATE_9_12_21"   

#################### LẤY DỮ LIỆU TỪ WEBSITE ####################

#Hàm insert dữ liệu mới vào sql
def InsertCurrencyToSQL(conx,cursor,list_ThoiGian,list_TenNT,list_MaNT,list_MuaTienMat,list_MuaChuyenKhoan,list_Ban):
    i = 0
    for data in list_TenNT:
        cursor.execute("insert EXCHANGE_RATE_DATA values (?,?,?,?,?,?)", list_ThoiGian[0], list_TenNT[i], list_MaNT[i], list_MuaTienMat[i], list_MuaChuyenKhoan[i], list_Ban[i])
        i = i+1
        conx.commit() 

#Hàm update dữ liệu trong sql
def UpDateCurrencyInSQL(conx,cursor,list_ThoiGian,list_TenNT,list_MaNT,list_MuaTienMat,list_MuaChuyenKhoan, list_Ban):
    i = 0
    for data in list_MaNT:
        cursor.execute("UPDATE EXCHANGE_RATE_DATA SET TenNgoaiTe=?,MaNT=?,MuaTienMat=?,MuaChuyenKhoan=?,Ban=? where ThoiGian=? AND MaNT = ?",
        list_TenNT[i], 
        list_MaNT[i], 
        list_MuaTienMat[i], 
        list_MuaChuyenKhoan[i], 
        list_Ban[i],
        list_ThoiGian[0],
        list_MaNT[i])
        i = i + 1
        conx.commit()

#Hàm lấy dữ liệu từ web và insert/update vào sql
def CrawlDataFromWeb():
    print("Runing...")
    url = "https://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx"
    try:
        response = requests.get(url)
    #Không thể gửi request tới trang web
    except:
        print("CAN NOT CONNECT TO WEBSITE!!!")
    
    #Hiển thị dưới dạng xml
    soup = BeautifulSoup(response.text, features="lxml")


    list_ThoiGian = []
    list_TenNT = []
    list_MaNT = []
    list_MuaTienMat = []
    list_MuaChuyenKhoan = []
    list_Ban = []

    ### Crawl thời gian ###
    
    tag = soup.find("datetime")
    list_ThoiGian.append(tag.next)
    list_ThoiGian = [w[:10] for w in list_ThoiGian] #Tách string trong list từ ['12/23/2021 1:21:55 PM'] thành ['12/23/2021']

    ### Crawl tỷ giá tiền tệ ###
    for tag in soup.find_all("exrate"):
        list_TenNT.append(tag.get("currencyname"))
        list_MaNT.append(tag.get("currencycode"))
        list_MuaTienMat.append(tag.get("buy"))
        list_MuaChuyenKhoan.append(tag.get("transfer"))
        list_Ban.append(tag.get("sell"))
        
    ### Tạo kết nối ###
    conx = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-S8G0HJG\SQLEXPRESS;"
    "Database=EXCHANGE_RATE;"
    "Trusted_Connection=yes;")
    cursor = conx.cursor()

    check = ""
    MaNT = "USD"

    #Kiểm tra nếu data của ngày đó đã có trong csdl thì check = "exist"
    for row in cursor.execute("select * from EXCHANGE_RATE_DATA where ThoiGian = ? AND MaNT = ?", list_ThoiGian[0], MaNT):
        check = "exist"
    
    #Chưa có dữ liệu của ngày ... thì insert
    if(check != "exist"):
        InsertCurrencyToSQL(conx,cursor,list_ThoiGian,list_TenNT,list_MaNT,list_MuaTienMat,list_MuaChuyenKhoan, list_Ban)
   
    #Nếu ngày ... đã có dữ liệu rồi thì update
    else:
        UpDateCurrencyInSQL(conx,cursor,list_ThoiGian,list_TenNT,list_MaNT,list_MuaTienMat,list_MuaChuyenKhoan, list_Ban)
    conx.close()
###################################################
#Hàm thời gian
def Repeat():
    while(True):
        CrawlDataFromWeb()
        time.sleep(1800)
        
    

# Hàm lấy ngày từ sql
def GetDate():
    conx = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-S8G0HJG\SQLEXPRESS;"
    "Database=EXCHANGE_RATE;"
    "Trusted_Connection=yes;")
    cursor = conx.cursor()
    list = []
    for row in cursor.execute("select ThoiGian from EXCHANGE_RATE_DATA where MaNT = ? order by ThoiGian DESC","USD"): #hoặc ASC
        list.append(row[0])
    conx.close()
    return list
    
#Ham xu ly Login hoặc Signup
def choose(choice,conn, sign):
    conn.send(choice.encode(FORMAT))
    username = ""
    if(choice==LOGIN):
        #Nhan ten va password
        username=conn.recv(1024).decode(FORMAT)
        conn.send(username.encode(FORMAT))
        passw=conn.recv(1024).decode(FORMAT)
        conn.send(passw.encode(FORMAT))
        conn.recv(1024)
        #Kiem tra thong tin va gui phan hoi cho client
        sign = AccountCheck(conn, username, passw, sign)
        list = [sign,username]
        return list
    elif(choice==SIGNUP):
        #Nhan ten, password va password again
        username=conn.recv(1024).decode(FORMAT)
        conn.send(username.encode(FORMAT))
        passw=conn.recv(1024).decode(FORMAT)
        conn.send(passw.encode(FORMAT))
        conn.recv(1024)
        #Dang ky cho client
        sign = Signup(conn, username, passw,sign)
        list = [sign,username]
        return list
    else:
       print("enddddddddd")
       return ["",""]
        

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
    print(list)
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

def request(conn,date):
    conn.send(date.encode(FORMAT))
    mnt=conn.recv(1024).decode(FORMAT)
    print(mnt)
    if(mnt=="All"):
        GetAllData(conn, date)
    else:
        GetSpeData(conn, date, mnt)
ab = """
def HandleClient(conn,address,sign):
    #print("Connected to ", address)
    print()
    while(sign != "0"):
        sign = choice(conn,sign)
    while(True):
        request(conn)
    
    print("Connection with ", address, " ended")
    #conn.close()
"""
################# HÀM GUI #######################
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 

from tkinter import font 
from tkinter import scrolledtext 
import time

HEADER_FONT = ("Open Sans", 16,"bold")
BUTTON_FONT = ("Open Sans", 12, "bold")
REGULAR_FONT= ("Open Sans", 10, "bold")
ENTRY_FONT= ("Open Sans", 10, "bold")

#option
ERROR = -1
WARNING = 0
INFO = 1

# colors
WHITE    = '#F2F2F2'
PURPLE_1 = '#A9ABD9'
PURPLE_2 = '#585CA6'
PURPLE_3 = '#3C41A6'
PURPLE_4 = '#040B8C'

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

        self.showFrame(StartPage)

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
        self.configure(bg=PURPLE_1)

        # Main frame --------------------------------------------------------
        frame_left = tk.Frame(self, height=300, width=250, bg=PURPLE_2)
        frame_left.grid(row=0, column=0)

        frame_right = tk.Frame(self, height=300, width=350, bg=PURPLE_1)
        frame_right.grid(row=0, column=1)

        # Frame left --------------------------------------------------------
        canvas = tk.Canvas(frame_left, width=230, height=295, bg=PURPLE_2, bd=0)
        canvas.create_text(113,150, text="SERVER", font=("Open Sans", 36, "bold"), fill="#EBEBF2")
        canvas.pack()

        # Frame right --------------------------------------------------------
        x_show = 90
        
        label_title = tk.Label(frame_right, text="ĐĂNG NHẬP", font=HEADER_FONT, fg=PURPLE_4, bg=PURPLE_1)
        label_title.place(x=x_show+35,y=55)

        label_user = tk.Label(frame_right, text="Tên đăng nhập", font=REGULAR_FONT, fg=PURPLE_4, bg=PURPLE_1)
        label_user.place(x=x_show,y=90)

        label_pwd = tk.Label(frame_right, text="Mật khẩu", font=REGULAR_FONT, fg=PURPLE_4, bg=PURPLE_1)
        label_pwd.place(x=x_show,y=140)

        self.entry_user = tk.Entry(frame_right,width=25,bg='#EBEBF2', font=REGULAR_FONT)
        self.entry_user.place(x=x_show,y=115)

        self.entry_pwd = tk.Entry(frame_right,width=25,bg='#EBEBF2', font=REGULAR_FONT)
        self.entry_pwd.place(x=x_show,y=165)

        button_log = tk.Button(frame_right,text="ĐĂNG NHẬP",font=BUTTON_FONT, bg=PURPLE_3, fg=WHITE, command=lambda:self.click_log_in(controller)) 
        button_log.configure(width=10)
        button_log.place(x=x_show+37, y=205)
        #########################################################################
    def click_log_in(self, controller):
        id = str(self.entry_user.get())
        pwd = str(self.entry_pwd.get())

        self.entry_user.delete(0, tk.END)
        self.entry_pwd.delete(0, tk.END)

        list_account = [("1", "1"),("server123", "server123")]

        input = (id, pwd)

        for account in list_account:
            if input == account:
                controller.showFrame(HomePage)
                return     
        notification(ERROR, "Tên đăng nhập hoặc mật khẩu sai!!!\nVui lòng nhập lại.")


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        self.configure(bg=PURPLE_2)

        self.run = False

        # Main frame
        frame_top = tk.Frame(self, bg=PURPLE_2, height=50, width=880)
        frame_top.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        frame_options = tk.LabelFrame(self, text = "Tùy chọn", font=("Open Sans", 12, 'bold'), bg=PURPLE_1, fg=PURPLE_4, bd=3, height=100, width=880)
        frame_options.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        frame_show = tk.LabelFrame(self, bg="#FFFFFF", height=300, width=880, bd=3)
        frame_show.grid(row=2, column=0, padx=10, ipady=5, sticky='w')
        
        # Frame top --------------------------------------
        #button_logOut = tk.Button(frame_top, text="Log out", font=("Open Sans", 12, 'bold'), fg="#000000", bg="#FFFFFF")
        #button_logOut.place(x=770, y=15)
        canvas_name_top = tk.Canvas(frame_top, bg=PURPLE_2, height=30, width=400, highlightthickness=0)
        ##
        canvas_name_top.create_text(110,15,text="VndEx Server",font=("Open Sans", 25, 'bold'),fill=WHITE)
        ##
        canvas_name_top.place(x=0, y=10)

        # Frame options --------------------------------------
        self.button_run = tk.Button(frame_options, text="Chạy", font=("Open Sans", 10, 'bold'), fg=WHITE, bg=PURPLE_3, command=lambda:self.click_run(controller))
        self.button_run.config(height=0, width=12)
        self.button_run.place(x=550, y=25)

        self.button_stop = tk.Button(frame_options, text="Dừng", font=("Open Sans", 10, 'bold'), fg=WHITE, bg=PURPLE_3, command=lambda:self.click_stop(controller))
        self.button_stop.config(height=0, width=12)
        self.button_stop.place(x=700, y=25)

        canvas_name_option = tk.Canvas(frame_options, bg=PURPLE_1, height=20, width=340, highlightthickness=0)
        ##
        canvas_name_option.create_text(131,12,text="Địa chỉ IP",font=("Arial", 10, 'bold'),fill=PURPLE_4)
        canvas_name_option.create_text(284,12,text="Port",font=("Open Sans", 10, 'bold'),fill=PURPLE_4)
        ##
        canvas_name_option.place(x=0, y=10)

        self.entry_ip = tk.Entry(frame_options, width=13 ,bg=WHITE, font=REGULAR_FONT, bd=2)
        self.entry_ip.place(x=100, y=30)

        self.entry_port = tk.Entry(frame_options, width=9,bg=WHITE, font=REGULAR_FONT, bd=2)
        self.entry_port.place(x=270, y=30)

        # Frame show --------------------------------------
        self.text_show = scrolledtext.ScrolledText(frame_show, bd=0)
        self.text_show.configure(state='disable', font=("Arial", 10, 'bold'), width=122, height=21)
        self.text_show.pack(side='left')
        
        # Default run -------------------------------------
        self.print_default_IP_Port()
        self.print_show_server_close()
        
        if self.run:
            self.button_run.config(state='disable')
            self.button_stop.config(state='normal')
        else:
            self.button_run.config(state='normal')
            self.button_stop.config(state='disable')
        ############################################################################
    def client_login(self, ip, port, username):
        self.print_show_client_login(ip, port, username)

    def click_stop(self, controller): 
        if self.run:
            self.run = False
            self.button_stop.config(state='disable')
            self.button_run.config(state='normal')
            self.delay(controller, float(0.5))
            self.clear_text_show()
            self.print_show_server_close()
            
            #self.close_server()
            
    def click_run(self, controller):
        if self.run == False:
            self.run = True
            self.button_stop.config(state='normal')
            self.button_run.config(state='disable')
            self.clear_text_show()
            self.print_show_server_start()
            #server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #self.run_server()
            server.bind((SERVER, PORT))
            server.listen()
            print("Server is waiting...")
            print()

            try:
                ServerThread=threading.Thread(target=self.HandleServer, args=())
                ServerThread.daemon = True
                ServerThread.start()
            except:
                print("Client is disconnected.") #Nếu client thoát đột ngột => chạy dòng này => server không bị treo.

                        
            #input()
            #print("client is connected")
            #self.print_show_client_login("Client is connected")
            #self.print_show_client_logout(address[0], address[1], "tuan123")

    def HandleClient(self,conn,address,sign):
        #print("Connected to ", address)
        print("send successfull")
        
        print()
        while(sign != "0"):
            choice=conn.recv(1024).decode(FORMAT)
            if(self.run == False):
                print("Connect is closed")
                conn.close()
                return
            list = choose(choice, conn,sign)
            sign = list[0]
            id = list[1]
            if sign == "0":
                self.print_show_client_login(address[0], address[1], id)
        list = GetDate()
        SendList(conn,list)
        try:
            while(True):
                date=conn.recv(1024).decode(FORMAT)                        
                if(self.run == False):
                    print("Connect iss closed")
                    conn.close()
                    return
                request(conn,date)
        except:
            self.print_show_client_logout(address[0],address[1],id)

        print("Connection with ", address, " ended")
        #conn.close()

    def HandleServer(self):
        nClient = 0
        sign = ""
        while(True):
            try:
                conn, address = server.accept()
                print("Accepted")
                if (self.run == True):
                    print("nhay vao if")
                    conn.send("1".encode(FORMAT))
                    print("Sent 1")
                    conn.recv(1024).decode(FORMAT)
                    clientThread=threading.Thread(target=self.HandleClient, args=(conn, address, sign))
                    clientThread.daemon = True
                    clientThread.start()
                    print("Connected to ", address)

                else:
                    print("nhay vao else")
                    conn.send("0".encode(FORMAT))
                    print("Sent 0")
                    conn.recv(1024).decode(FORMAT)
                    conn.close()
            
            except:
                print("Client ",address, "is disconnectedddddddddd.") #Nếu client thoát đột ngột => chạy dòng này => server không bị treo.
            
    def close_server(self,conn): 
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
        self.text_show.insert('insert', "[Server][Closed]\n\n")
        self.text_show.configure(state='disable')

    def print_show_client_login(self, ip, port, username):
        self.text_show.configure(state='normal')
        self.text_show.insert('insert', f"\n[Client][Logged in]   IP:{ip} - Port:{port} - User:{username}")
        self.text_show.configure(state='disable')

    def print_show_client_logout(self, ip, port, username):
        self.text_show.configure(state='normal')
        self.text_show.insert('insert', f"\n[Client][Logged out] IP:{ip} - Port:{port} - User:{username}")
        self.text_show.configure(state='disable')

    def print_default_IP_Port(self):
        self.entry_ip.insert(0, SERVER)
        self.entry_port.insert(0, PORT)
        
        


############################################# HÀM MAIN ##################################################
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM: giao thức TCP
#server.bind((SERVER, PORT))


DataThread=threading.Thread(target= Repeat, args=())
DataThread.daemon = True
DataThread.start()


app = VndEx_App()
app.mainloop()
server.close()

