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
        self.configure(bg="#CED0F2")

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

        button_log = tk.Button(frame_1,text="LOG IN",font=BUTTON_FONT, bg="#6B8DF2",fg='#EBEBF2',command=lambda:controller.showFrame(HomePage)) 
        button_log.configure(width=10)
        button_sign = tk.Button(frame_1,text="SIGN UP",font=BUTTON_FONT,bg="#6B8DF2",fg='floral white', command=lambda:notification(ERROR, "Wrong password or username!!!\nPlease try again.")) 
        button_sign.configure(width=10)

        #########################################################################
        canvas = tk.Canvas(self, width=230, height=300, bg='#6B8DF2', bd=0)
        canvas.create_text(113,150, text="SERVER", font=("Open Sans", 36, "bold"), fill="#EBEBF2")

        
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
        
        label_title = tk.Label(self, text="HOME PAGE", font=HEADER_FONT,fg='#20639b',bg="bisque2")
        button_back = tk.Button(self, text="Go back",bg="#20639b",fg='#f5ea54')
        button_list = tk.Button(self, text="List all", bg="#20639b",fg='#f5ea54')

        self.entry_search = tk.Entry(self)
        button_search = tk.Button(self, text="Search for ID",bg="#20639b",fg='#f5ea54', command=lambda:controller.showFrame(StartPage))

        label_title.pack(pady=10)

        button_search.configure(width=10)
        button_list.configure(width=10)
        button_back.configure(width=10)

        self.entry_search.pack()

        self.label_notice = tk.Label(self, text="", bg="bisque2")
        self.label_notice.pack(pady=4)

        button_search.pack(pady=2)
        button_list.pack(pady=2) 
        button_back.pack(pady=2)

        self.frame_detail = tk.Frame(self, bg="steelblue1")
        
        self.label_score = tk.Label(self.frame_detail,bg="steelblue1", text="", font=HEADER_FONT)
        self.label_time = tk.Label(self.frame_detail,bg="steelblue1", text="", font=HEADER_FONT)
        self.label_status = tk.Label(self.frame_detail,bg="steelblue1", text="", font=HEADER_FONT)

        self.tree_detail = ttk.Treeview(self.frame_detail)
        self.tree_detail["column"] = ("Time", "Player", "Team", "Event")
        
        self.tree_detail.column("#0", width=0, stretch=tk.NO)
        self.tree_detail.column("Time", anchor='c', width=50)
        self.tree_detail.column("Player", anchor='c', width=200)
        self.tree_detail.column("Team", anchor='c', width=200)
        self.tree_detail.column("Event", anchor='c', width=180)

        self.tree_detail.heading("0", text="", anchor='c')
        self.tree_detail.heading("Time", text="Time", anchor='c')
        self.tree_detail.heading("Player", text="Player", anchor='c')
        self.tree_detail.heading("Team", text="Team", anchor='c')
        self.tree_detail.heading("Event", text="Event", anchor='c')


        self.label_score.pack(pady=5)
        self.label_time.pack(pady=5)
        self.label_status.pack(pady=5)
        self.tree_detail.pack()


        self.frame_list = tk.Frame(self, bg="tomato")
        
        self.tree = ttk.Treeview(self.frame_list)

        
        self.tree["column"] = ("ID", "TeamA", "Score", "TeamB", "Status")
        
        
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor='c', width=30)
        self.tree.column("TeamA", anchor='e', width=140)
        self.tree.column("Score", anchor='c', width=40)
        self.tree.column("TeamB", anchor='w', width=140)
        self.tree.column("Status", anchor='c', width=80)

        self.tree.heading("0", text="", anchor='c')
        self.tree.heading("ID", text="ID", anchor='c')
        self.tree.heading("TeamA", text="TeamA", anchor='e')
        self.tree.heading("Score", text="Score", anchor='c')
        self.tree.heading("TeamB", text="TeamB", anchor='w')
        self.tree.heading("Status", text="Status", anchor='c')
        
        self.tree.pack(pady=20)



app = VndEx_App()
app.mainloop()