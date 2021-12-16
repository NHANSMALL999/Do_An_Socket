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
        self.configure(bg="#6B8DF2")
        #self.pack()

        button_signout = tk.Button(self,text="SIGN OUT",font=BUTTON_FONT, bg="#6B8DF2",fg='#EBEBF2',command=lambda:controller.showFrame(StartPage)) 
        button_signout.configure(width=10)
        button_signout.pack(side='bottom', padx=10, pady=5)

        top_frame = tk.LabelFrame(self, text="Client connection", font=BUTTON_FONT,  fg="#EBEBF2", bg="#6B8DF2", bd=0)

        top_frame.pack(fill='both', expand=1, padx=10, pady=10)

        #Create a canvas
        my_canvas_top = tk.Canvas(top_frame, bg="#CED0F2")
        my_canvas_top.pack(side="left", fill='both', expand=1)

        #Add a scrollbar to the canvas
        my_scrollbar = ttk.Scrollbar(top_frame, orient='vertical', command=my_canvas_top.yview)
        my_scrollbar.pack(side='right', fill='y')

        #Configure the canvas
        my_canvas_top.configure(yscrollcommand=my_scrollbar.set)
        my_canvas_top.bind('<Configure>', lambda e: my_canvas_top.configure(scrollregion=my_canvas_top.bbox("all")))

        #Create another frame inside the canvas
        second_frame = tk.Frame(my_canvas_top)

        #Add that new frame to the window in the canvas
        my_canvas_top.create_window((0,0), window=second_frame, anchor='nw')
        
        



app = VndEx_App()
app.mainloop()
