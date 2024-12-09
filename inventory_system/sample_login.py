from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import sqlite3
import os

class Login_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Login for IMS | Developed by KUSUMANJALI AND SNEHA PRIYA")
        self.root.geometry("1350x700+0+0")

        # Load and set the background image for the main window
        self.bg2_image = Image.open(r"images/bg2.jpg")  # Replace with your image path
        self.bg2_image = self.bg2_image.resize((1350, 700), Image.Resampling.LANCZOS)  # Resize to match window size
        self.bg2_photo = ImageTk.PhotoImage(self.bg2_image)
        bg_label = Label(self.root, image=self.bg2_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Login frame
        login_frame = Frame(self.root, bd=5, relief=RIDGE, bg="white")
        login_frame.place(x=380, y=20, width=600, height=650)

        # Add background image inside the login frame
        self.bg_image_frame = Image.open(r"images/bg4.jpg")  # Background for the login frame
        self.bg_image_frame = self.bg_image_frame.resize((600, 650), Image.Resampling.LANCZOS)  # Resize to fit the frame
        self.bg_image_frame = ImageTk.PhotoImage(self.bg_image_frame)

        bg_label_frame = Label(login_frame, image=self.bg_image_frame)
        bg_label_frame.place(x=0, y=0, relwidth=1, relheight=1)  # Place the background image inside the frame

        # Add the logo inside the login frame
        self.logo_image = Image.open(r"images/login.png")  # Path to logo image
        self.logo_image = self.logo_image.resize((120, 120), Image.Resampling.LANCZOS)  # Resize the image
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        logo_label = Label(login_frame, image=self.logo_photo, bg="white")  # Add logo to frame
        logo_label.place(x=230, y=10)  # Adjust position as required

        # Login title
        title = Label(login_frame, text="Login", bg="white", font=("Elephant", 30, "bold"))
        title.place(x=0, y=140, relwidth=1)

        # Employee ID field
        lbl_user = Label(login_frame, text="Employee ID", font=("Andalus", 15), bg="white", fg="#767171")
        lbl_user.place(x=30, y=210)
        self.employee_id = StringVar()
        self.password = StringVar()
        txt_employee_id = Entry(login_frame, textvariable=self.employee_id, font=("times new roman", 15), bg="#ECECEC")
        txt_employee_id.place(x=30, y=250, width=535)

        # Password field
        lbl_pass = Label(login_frame, text="Password", font=("Andalus", 15), bg="white", fg="#767171")
        lbl_pass.place(x=30, y=290)
        txt_pass = Entry(login_frame, textvariable=self.password, font=("times new roman", 15), show="*", bg="#ECECEC")
        txt_pass.place(x=30, y=330, width=535)

        # User Type (Employee/Admin)
        self.user_type = StringVar()
        self.user_type.set("Employee")  # Default selection
        lbl_type = Label(login_frame, text="Login As:", font=("Andalus", 15), bg="white", fg="#767171")
        lbl_type.place(x=30, y=370)
        Radiobutton(login_frame, text="Employee", variable=self.user_type, value="Employee", bg="white").place(x=150, y=370)
        Radiobutton(login_frame, text="Admin", variable=self.user_type, value="Admin", bg="white").place(x=240, y=370)

        # Login Button
        btn_login = Button(login_frame, text="Log in", command=self.login, font=("Arial Rounded MT Bold", 15), bg="#00B0F0", activebackground="#00B0F0", fg="white", activeforeground="white", cursor="hand2")
        btn_login.place(x=50, y=460, width=490, height=45)

        # Welcome frame
        register_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        register_frame.place(x=420, y=560, width=520, height=60)
        lbl_reg = Label(register_frame, text="Welcome to WareHouse", font=("times new roman", 14, "bold"), bg="white")
        lbl_reg.place(x=160, y=15)

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

# Initialize the application
root = Tk()
obj = Login_System(root)
root.mainloop()
