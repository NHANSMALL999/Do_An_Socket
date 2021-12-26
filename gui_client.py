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

# colors
WHITE    = '#F2F2F2'
PURPLE_1 = '#A9ABD9'
PURPLE_2 = '#585CA6'
PURPLE_3 = '#3C41A6'
PURPLE_4 = '#040B8C'

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
def RecieveList(client):
    list = []
    data = ""
    data= client.recv(1024).decode(FORMAT)
    while(data!="end"):
        list.append(data)
        client.send(data.encode(FORMAT))
        data= client.recv(1024).decode(FORMAT)
    #print(list)
    return list

#
#Hàm nhận toàn bộ bảng data từ server
def GetAllDataFromServer(client,list):
    RecieveList(client)

#Hàm nhận data theo tên từ server
def GetSpeDataFromServer(client):
    RecieveList(client)


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
            self.geometry("1000x600")
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
                client.close()
                ###################################
                self.destroy()
            except:
                client.close()
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
        canvas.create_text(113,150, text="CLIENT", font=("Open Sans", 36, "bold"), fill="#EBEBF2")
        canvas.pack()

        # Frame right --------------------------------------------------------
        label_title = tk.Label(frame_right, text="ĐĂNG NHẬP", font=HEADER_FONT, fg=PURPLE_4, bg=PURPLE_1)
        label_title.place(x=120,y=40)

        x_show = 95

        label_user = tk.Label(frame_right, text="Tên đăng nhập", font=REGULAR_FONT, fg=PURPLE_4, bg=PURPLE_1)
        label_user.place(x=x_show,y=80)

        label_pwd = tk.Label(frame_right, text="Mật khẩu", font=REGULAR_FONT, fg=PURPLE_4, bg=PURPLE_1)
        label_pwd.place(x=x_show,y=130)

        self.entry_user = tk.Entry(frame_right,width=25,bg='#EBEBF2', font=REGULAR_FONT)
        self.entry_user.place(x=x_show,y=100)

        self.entry_pwd = tk.Entry(frame_right,width=25,bg='#EBEBF2', font=REGULAR_FONT)
        self.entry_pwd.place(x=x_show,y=150)
        
        button_log = tk.Button(frame_right,text="Đăng nhập",font=BUTTON_FONT, bg=PURPLE_3, fg=WHITE, command=lambda:click_login(controller, client, str(self.entry_user.get()), str(self.entry_pswd.get()))) 
        button_log.configure(width=10)
        button_log.place(x=x_show+35, y=190)

        label_gosign = tk.Label(frame_right, text="Chưa có tài khoản?", font=REGULAR_FONT, fg=PURPLE_4, bg=PURPLE_1)
        label_gosign.place(x=x_show-60,y=250)

        button_gosign = tk.Button(frame_right,text="Đăng ký",font=REGULAR_FONT, bg=PURPLE_3, fg=WHITE, command=lambda:controller.showFrame(SignUpPage)) 
        button_gosign.configure(width=10)
        button_gosign.place(x=x_show+80, y=245)
        #########################################################################


class SignUpPage(tk.Frame):
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
        canvas.create_text(113,150, text="CLIENT", font=("Open Sans", 36, "bold"), fill="#EBEBF2")
        canvas.pack()

        # Frame right --------------------------------------------------------
        x_show = 95

        label_title = tk.Label(frame_right, text="ĐĂNG KÝ", font=HEADER_FONT, fg=PURPLE_4, bg=PURPLE_1)
        label_title.place(x=x_show+40,y=40)

        label_user = tk.Label(frame_right, text="Tên đăng nhập", font=REGULAR_FONT, fg=PURPLE_4, bg=PURPLE_1)
        label_user.place(x=x_show,y=80)

        label_pwd = tk.Label(frame_right, text="Mật khẩu", font=REGULAR_FONT, fg=PURPLE_4, bg=PURPLE_1)
        label_pwd.place(x=x_show,y=130)

        self.entry_user = tk.Entry(frame_right,width=25,bg='#EBEBF2', font=REGULAR_FONT)
        self.entry_user.place(x=x_show,y=100)

        self.entry_pwd = tk.Entry(frame_right,width=25,bg='#EBEBF2', font=REGULAR_FONT)
        self.entry_pwd.place(x=x_show,y=150)

        button_sign = tk.Button(frame_right,text="Đăng ký",font=BUTTON_FONT, bg=PURPLE_3, fg=WHITE, command=lambda:click_signup(controller, client, str(self.entry_user.get()), str(self.entry_pswd.get()))) 
        button_sign.configure(width=10)
        button_sign.place(x=x_show+35, y=190)

        label_golog = tk.Label(frame_right, text="Đã có tài khoản?", font=REGULAR_FONT, fg=PURPLE_4, bg=PURPLE_1)
        label_golog.place(x=x_show-60,y=250)

        button_golog = tk.Button(frame_right,text="Đăng nhập",font=REGULAR_FONT, bg=PURPLE_3, fg=WHITE, command=lambda:controller.showFrame(StartPage)) 
        button_golog.configure(width=10)
        button_golog.place(x=x_show+60, y=245)
        #########################################################################


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=PURPLE_2)
        self.contacts = []
        
        # Main frame ----------------------------------------------------------
        frame_top = tk.Frame(self, bg=PURPLE_2, height=50, width=980)
        frame_top.grid(row=0, column=0, padx=5, pady=5)
        
        frame_options = tk.LabelFrame(self, text = "Tùy chọn", font=("Open Sans", 12, 'bold'), bg=PURPLE_1, fg=PURPLE_4, bd=3, height=100, width=970)
        frame_options.grid(row=1, column=0, padx=15, pady=0, sticky='w')
        
        frame_show = tk.LabelFrame(self, bg="#FFFFFF", height=500, width=980)
        frame_show.grid(row=2, column=0, padx=5, pady=5)

        # frame top ----------------------------------------------------------
        #button_logOut = tk.Button(frame_top, text="Log out", font=("Open Sans", 12, 'bold'), fg="#000000", bg="#FFFFFF", command=lambda:self.click_log_out(controller))
        #button_logOut.place(x=870, y=15)
        canvas_name_top = tk.Canvas(frame_top, bg=PURPLE_2, height=30, width=400, highlightthickness=0)
        ##
        canvas_name_top.create_text(110,15,text="VndEx Client",font=("Open Sans", 25, 'bold'),fill=WHITE)
        ##
        canvas_name_top.place(x=0, y=10)

        # frame options ----------------------------------------------------------
        button_search = tk.Button(frame_options, text="Tra cứu", font=("Open Sans", 12, 'bold'), fg=WHITE, bg=PURPLE_3, command=lambda:self.ClickSearch(client,str(click_list_day.get()),str(click_list_type.get())))
        button_search.config(height=0, width=12)
        button_search.place(x=740, y=17)

        #button_clear = tk.Button(frame_options, text="Clear", font=("Open Sans", 10, 'bold'), fg="#000000", bg="#FFFFFF")
        #button_clear.config(height=0, width=12)
        #button_clear.place(x=670, y=26)
        list_day = RecieveList(client)

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
        
        canvas_name_option = tk.Canvas(frame_options, bg=PURPLE_1, height=20, width=400, highlightthickness=0)
        ##
        canvas_name_option.create_text(155,10,text="Tháng/Ngày/Năm",font=("Open Sans", 10, 'bold'),fill=PURPLE_4)
        canvas_name_option.create_text(337,10,text="Mã ngoại tệ",font=("Open Sans", 10, 'bold'),fill=PURPLE_4)
        ##
        canvas_name_option.place(x=0, y=6)
        
        drop_style = ttk.Style()
        drop_style.configure('Dropbox',
            background=PURPLE_3,
            foreground=WHITE,    
            fieldbackground = PURPLE_1,
            font=('Open Sans', 10, 'bold')
        )
        
        dropBox_day = tk.OptionMenu(frame_options, click_list_day, *list_day)
        dropBox_day.config(font=("Open Sans", 10, 'bold'), fg=WHITE, bg=PURPLE_3, width=15, highlightthickness=0)
        dropBox_day.place(x=100, y=27)

        click_list_type = tk.StringVar()
        click_list_type.set(list_type[0])

        dropBox_type = tk.OptionMenu(frame_options, click_list_type, *list_type)
        dropBox_type.config(font=("Open Sans", 10, 'bold'), fg=WHITE, bg=PURPLE_3, width=10, highlightthickness=0)
        dropBox_type.place(x=300, y=27)

        # frame show ----------------------------------------------------------
        # add style 
        style = ttk.Style()
        
        # pick a theme
        style.theme_use('alt')
        
        #configure treeview color
        style.configure("Treeview",
            background=WHITE,
            foreground=PURPLE_4,    
            fieldbackground = PURPLE_1,
            rowheight=25,
            font=('Open Sans', 10, 'bold')
        )
        style.configure("Treeview.Heading",
            background=PURPLE_1,
            foreground=PURPLE_4,    
            fieldbackground = PURPLE_2,
            rowheight=25,
            font=('Open Sans', 11, 'bold')
        )
        
        # change selected color
        style.map('Treeview',
            background=[('selected', PURPLE_3)]
        )
        
        # Create table
        self.treeView_show = ttk.Treeview(frame_show, column=(1,2,3,4,5), show="headings", height=15)
        self.treeView_show.grid(row=0, column=0, sticky='nsew')

        self.treeView_show.column("# 1", anchor='w', width=200)
        self.treeView_show.column("# 2", anchor='w', width=150)
        self.treeView_show.column("# 3", anchor='w', width=200)
        self.treeView_show.column("# 4", anchor='w', width=200)
        self.treeView_show.column("# 5", anchor='w', width=200)

        self.treeView_show.heading(1, text="Tên ngoại tệ",anchor='w')
        self.treeView_show.heading(2, text="Mã ngoại tệ",anchor='w')
        self.treeView_show.heading(3, text="Mua tiền mặt",anchor='w')
        self.treeView_show.heading(4, text="Mua chuyển khoản",anchor='w')
        self.treeView_show.heading(5, text="Bán",anchor='w')

        # Add Scrollbar
        scrollbar = ttk.Scrollbar(frame_show, orient=tk.VERTICAL, command=self.treeView_show.yview)
        self.treeView_show.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')
    ###############################################################################
    def ClickSearch(self,client,ngay, ma):
        #xóa bảng
        for selected_item in self.treeView_show.get_children():
            self.treeView_show.delete(selected_item)
        try:
            #Gửi yêu cầu cho server
            client.send(ngay.encode(FORMAT))
            client.recv(1024)
            client.send(ma.encode(FORMAT))
            list = []
            list = RecieveList(client)
            list = self.Convert(list)
            #if (list == []):

            print(list)
            for data in list:
                self.treeView_show.insert('', tk.END, values=data)
        except:
            notification(ERROR, "Server closed!!!")

        
    def Convert(self, list):
        new_list = []
        temp_list = []
        i = 0
        for data in list:
            if i < 5: 
                i = i + 1
                temp_list.append(data)
            else:
                new_list.append(temp_list)
                i = 1
                temp_list = []
                temp_list.append(data)
        new_list.append(temp_list)

               
        return new_list    
    def click_clear(self):
        pass

    def click_search(self):
        pass

    def click_log_out(self, controller):
        try:
            client.send("0".encode(FORMAT))
            client.recv(1024)
            client.close()
            ###################################
            client.connect((SERVER, PORT))
            controller.showFrame(StartPage)

        except:
            client.close()
            self.destroy()
        
        
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
        notification(ERROR, "Serser closed!!!")
           
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
