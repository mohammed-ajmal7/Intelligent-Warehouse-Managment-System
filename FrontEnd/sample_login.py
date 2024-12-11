from tkinter import *
from tkinter import messagebox
import sqlite3
import os
from PIL import Image, ImageTk

class Login_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Login for IMS | Developed by Kusumanjali and sneha priya")
        self.root.geometry("1350x700+0+0")

        # Load and scale the background image
        self.bg_image = Image.open("images/login1.jpeg")
        self.bg_image = self.bg_image.resize((1550, 800), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        # Set the background image
        self.lbl_bg = Label(self.root, image=self.bg_photo)
        self.lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        # Login frame
       # Login Frame with Semi-Transparent Effect
        login_frame = Frame(self.root, bd=5, relief=RIDGE, bg="#ECE9F0")
        login_frame.place(x=525, y=140, width=450, height=480)
  

        title = Label(login_frame, text="Login", bg="#ECE9F0", font=("Elephant", 30, "bold")).place(x=0, y=30, relwidth=1)

        lbl_user = Label(login_frame, text="Employee ID", font=("Andalus", 15), bg="#ECE9F0", fg="BLACK").place(x=30, y=100)
        self.employee_id = StringVar()
        self.password = StringVar()
        txt_employee_id = Entry(login_frame, textvariable=self.employee_id, font=("times new roman", 15), bg="white")
        txt_employee_id.place(x=30, y=140, width=380, height=35)

        lbl_pass = Label(login_frame, text="Password", font=("Andalus", 15), bg="#ECE9F0", fg="black").place(x=30, y=190)
        txt_pass = Entry(login_frame, font=("times new roman", 15), show="*", textvariable=self.password, bg="white")
        txt_pass.place(x=30, y=220, width=380, height=35)

        self.user_type = StringVar()
        self.user_type.set("Employee")  # Default selection
        lbl_type = Label(login_frame, text="Login As:", font=("Andalus", 16), bg="#ECE9F0", fg="black").place(x=30, y=270)
        Radiobutton(login_frame, text="Employee", variable=self.user_type, value="Employee", bg="#ECE9F0").place(x=150, y=270)
        Radiobutton(login_frame, text="Admin", variable=self.user_type, value="Admin", bg="#ECE9F0").place(x=240, y=270)

        btn_login = Button(login_frame, text="Log in", command=self.login, font=("Arial Rounded MT Bold", 17), bg="#00B0F0", activebackground="#00B0F0", fg="white", activeforeground="white", cursor="hand2")
        btn_login.place(x=70, y=320, width=300, height=40)

        # Frame 2
        register_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        register_frame.place(x=570, y=520, width=350, height=60)

        lbl_reg = Label(register_frame, text="Welcome to KS IMS", font=("times new roman", 15, "bold"), bg="white").place(x=90, y=15)

    def login(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.employee_id.get() == "" or self.password.get() == "":
                messagebox.showerror('Error', "All fields are required", parent=self.root)
            else:  
                cur.execute("select utype from employee where eid=? AND pass=?", (self.employee_id.get(), self.password.get()))
                user = cur.fetchone()
                if user is None:
                    messagebox.showerror('Error', "Invalid Username/Password", parent=self.root)
                else:
                    if user[0] == "Employee" and self.user_type.get() == "Employee":
                        self.root.destroy()
                        os.system("python billing.py")    
                    elif user[0] == "Admin" and self.user_type.get() == "Admin":
                        self.root.destroy()
                        os.system("python d.py")
                    else:
                        messagebox.showerror('Error', "Invalid User Type", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
            
root = Tk()
obj = Login_System(root)
root.mainloop()