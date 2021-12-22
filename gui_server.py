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

            self.run_server()

            self.print_show_client_login("127.0.0.1", "53490", "tuan123")
            self.print_show_client_logout("127.0.0.1", "53490", "tuan123")

    def close_server(self):
        pass

    def run_server(self):
        pass

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
        
        



app = VndEx_App()
app.mainloop()
