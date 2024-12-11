import time
import os
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from employee import EmployeeClass
from supplier import SupplierClass
from category import CategoryClass  # Add this if `CategoryClass` exists in the category.py file
from product import ProductClass
from sales import salesClass
import sqlite3
from tkinter import messagebox

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Warehouse Management System | Developed by Kusumanjali and Sneha Priya")
        self.root.config(bg="#f4f4f4")

        # Load and display the background image
        self.bg_image = Image.open("images/firstback.jpg").resize((1540, 800), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        bg_label = Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title bar with icon
        self.icon_title = PhotoImage(file="images/logo.jpeg")
        title = Label(
            self.root,
            text="     SMART WAREHOUSE MANAGEMENT SYSTEM",
            image=self.icon_title,
            compound=LEFT,
            font=("Times new roman", 30, "bold"),
            bg="#2d2d2d",
            fg="white",
            anchor="w",
            padx=20
        )
        title.place(x=0, y=0, relwidth=1, height=70)

        # Logout button with hover effect
        btn_logout = Button(
            self.root,
            text="Logout",
            command=self.logout,
            font=("black", 15, "bold"),
            bg="light gray",
            fg="black",
            cursor="hand2",
            activebackground="gray",
            activeforeground="white"
        )
        btn_logout.place(x=1290, y=10, height=50, width=150)

        # Clock
        self.lbl_clock = Label(
            self.root,
            text="Welcome to Warehouse Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",
            font=("Times new roman", 14),
            bg="#f2f5f6",
            fg="#2d2d2d"
        )
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # Hidden menu setup
        self.is_menu_open = False
        self.menu_frame = Frame(self.root, bg="#2d2d2d", bd=2, relief=RIDGE)
        self.menu_frame.place(x=0, y=104, width=0, height=565)

        # Add menu items
        menu_items = [
            ("Employee", self.employee),
            ("Supplier", self.supplier),
            ("Category", self.category),
            ("Product", self.product),
            ("Sales", self.sales),
            ("Tracking", self.front),  # Add this line
            ("Exit", root.quit)
        ]

        for text, command in menu_items:
            btn = Button(
                self.menu_frame,
                text=text,
                font=("Times new roman", 18, "bold"),
                bg="#4d4d4d",
                fg="white",
                cursor="hand2",
                activebackground="#5c5c5c",
                activeforeground="white",
                command=command
            )
            btn.pack(side=TOP, fill=X, pady=2)

        # Toggle menu button
        btn_toggle_menu = Button(
            self.root,
            text="☰",
            font=("Times new roman", 18, "bold"),
            bg="#4d4d4d",
            fg="white",
            command=self.toggle_menu,
            cursor="hand2",
            activebackground="#5c5c5c",
            activeforeground="white"
        )
        btn_toggle_menu.place(x=0, y=70, width=50, height=35)

        # Dashboard widgets
        self.dashboard_widgets()

        # Footer
        lbl_footer = Label(
            self.root,
            text="Warehouse Management System | Developed by Kusumanjali and Sneha Priya\nFor any technical issue contact: +91xxxxxx02",
            font=("Times new roman", 12),
            bg="#2d2d2d",
            fg="white"
        )
        lbl_footer.pack(side=BOTTOM, fill=X)

        # Update content
        self.update_content()

    def dashboard_widgets(self):
        stats = [
            ("Total Employees", "0", "#333333"),  # Dark Gray (Professional and Neutral)
            # ("Total Suppliers", "0", "#444444"),  # Slightly Lighter Gray
            ("Total Suppliers", "0","#777777"),
            ("Total Categories", "0", "#333333"),  # Medium Gray
            ("Total Products", "0", "#777777"),  # Light Gray
            
            ("Total Sales", "0", "#333333")      # Even Lighter Gray

        ]


        x_positions = [220, 480, 740, 1000, 1260]
        y_positions = [170, 170, 170, 170, 170]

        self.labels = []

        for i, (text, value, color) in enumerate(stats):
            label = Label(
                self.root,
                text=f"{text}\n[ {value} ]",
                bd=5,
                relief=RIDGE,
                bg=color,
                fg="white",
                font=("Times new roman", 18, "bold"),
                justify=CENTER
            )
            label.place(x=x_positions[i], y=y_positions[i], height=120, width=200)
            self.labels.append(label)

    def toggle_menu(self):
        if self.is_menu_open:
            self.menu_frame.place(x=0, y=104, width=0, height=565)
        else:
            self.menu_frame.place(x=0, y=104, width=200, height=565)
        self.is_menu_open = not self.is_menu_open

    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = EmployeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = SupplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = CategoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = ProductClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)


    def front(self):
        self.new_win = Toplevel(self.root)  # Open a new window
        self.new_win.title("RFID Tracking Database")
        self.new_win.geometry("800x600")  # Set appropriate dimensions for the front.py interface
        exec(open("front.py").read())  # Load and execute the front.py script


    def update_content(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("select * from product")
            product = cur.fetchall()
            self.labels[3].config(text=f'Total Products\n[ {len(product)} ]')

            cur.execute("select * from employee")
            employee = cur.fetchall()
            self.labels[0].config(text=f'Total Employees\n[ {len(employee)} ]')

            cur.execute("select * from supplier")
            supplier = cur.fetchall()
            self.labels[1].config(text=f'Total Suppliers\n[ {len(supplier)} ]')

            cur.execute("select * from category")
            category = cur.fetchall()
            self.labels[2].config(text=f'Total Categories\n[ {len(category)} ]')

            bill = len(os.listdir('bill'))
            self.labels[4].config(text=f'Total Sales\n[ {bill} ]')

            time_ = time.strftime("%I:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(
                text=f"Welcome to Warehouse Management System\t\t Date: {date_}\t\t Time: {time_}"
            )
            self.lbl_clock.after(200, self.update_content)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python sample_login.py")

if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
