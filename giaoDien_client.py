import tkinter as tk
from PIL import Image, ImageTk


# Beginning GUI object
window = tk.Tk()
window.geometry("800x500")
window.configure(bg = "#FFFFFF")
window.title('Client')
# fixed size window
window.resizable(0,0)


def click_dangNhap():
    user = input_User.get()
    password = input_Password.get()
    print(user)
    print(password)


canvas = tk.Canvas(
    window, 
    bg="#FFFFFF",
    height=500,
    width=800,
    highlightthickness=0,
    relief="flat"
    #https://www.tutorialspoint.com/python/tk_relief.htm
)
canvas.place(x=0,y=0)

# Hinh nen
my_img = (Image.open("hinhNen.jpg"))
resized_img=my_img.resize((300,500), Image.ANTIALIAS)
new_img= ImageTk.PhotoImage(resized_img)
canvas.create_image(0,0,anchor="nw", image=new_img)

# Logo
canvas.create_text(
    550.0,
    75.0,  
    anchor="center",
    #https://www.tutorialspoint.com/python/tk_anchors.htm
    text="VndEx",
    fill="#79C947",
    font=('Open Sans','50','bold')
    #https://www.tutorialspoint.com/how-to-set-the-font-size-of-a-tkinter-canvas-text-item
)
canvas.create_text(
    400.0,
    155.0,  
    anchor="w",
    #https://www.tutorialspoint.com/python/tk_anchors.htm
    text="Tên đăng nhập",
    fill="#6F6F7C",
    font=('Open Sans','14')
    #https://www.tutorialspoint.com/how-to-set-the-font-size-of-a-tkinter-canvas-text-item
)
canvas.create_text(
    400.0,
    240.0,  
    anchor="w",
    #https://www.tutorialspoint.com/python/tk_anchors.htm
    text="Mật khẩu",
    fill="#6F6F7C",
    font=('Open Sans','14')
    #https://www.tutorialspoint.com/how-to-set-the-font-size-of-a-tkinter-canvas-text-item
)
canvas.create_text(
    400.0,
    450.0, 
    anchor="w",
    #https://www.tutorialspoint.com/python/tk_anchors.htm
    text="Chưa có tài khoản?",
    fill="#6F6F7C",
    font=('Open Sans','12')
    #https://www.tutorialspoint.com/how-to-set-the-font-size-of-a-tkinter-canvas-text-item
)

input_User=tk.Entry(window, borderwidth=1 , font=('Open Sans', 14), bg="#6F6F7C", fg="#FFFFFF", width=26)
input_User.place(x=400, y=167)

input_Password=tk.Entry(window, borderwidth=1 , font=('Open Sans', 14), bg="#6F6F7C", fg="#FFFFFF", width=26)
input_Password.place(x=400, y=252)

button_Dangnhap = tk.Button(
    canvas,
    text="Đăng nhập", 
    font=("Open Sans", 16, 'bold'),
    bg="#79C947", 
    fg="#FFFFFF",
    relief="flat",
    command=click_dangNhap
)
button_Dangnhap.place(x=485,y=320)

button_Dangky = tk.Button(
    canvas,
    text="Đăng ký", 
    font=("Open Sans", 14, 'bold'),
    bg="#FFFFFF", 
    fg="#79C947",
    relief="flat"
)
button_Dangky.place(x=545,y=430)



window.mainloop()

