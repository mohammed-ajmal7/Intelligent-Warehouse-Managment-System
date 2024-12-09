import time
import os
from tkinter import *
from PIL import Image, ImageTk  # Import for handling images
from employee import EmployeeClass
from supplier import SupplierClass  
from category import CategoryClass
from product import ProductClass  
from sales import salesClass
import sqlite3
from tkinter import messagebox

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("SMART WAREHOUSE MANAGEMENT | DEVELOPED BY KUSUMANJALI AND SNEHA PRIYA")

        # Load and set the background image
        self.bg_image = Image.open(r"images/back.jpg")  # Replace with your image path
        self.bg_image = self.bg_image.resize((1350, 700), Image.Resampling.LANCZOS)  # Resize to match window size
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        bg_label = Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        ## Title
        # Load and resize the logo image
        self.logo_image = Image.open("images/logo.png")  # Load the logo
        self.logo_image = self.logo_image.resize((80, 80), Image.Resampling.LANCZOS)  # Resize to desired dimensions
        self.icon_title = ImageTk.PhotoImage(self.logo_image)  # Convert to Tkinter-compatible format

        title = Label(self.root, text="SMART WAREHOUSE MANAGEMENT", image=self.icon_title, compound=LEFT, font=("times new roman", 36, "bold"), bg="black", fg="white", anchor="w", padx=20)
        title.place(x=0, y=0, relwidth=1, height=70)

        # Logout button
        btn_logout = Button(self.root, text="Logout",command=self.logout, font=("times new roman", 15, "bold"), bg="yellow", cursor="hand2")
        btn_logout.place(x=1200, y=10, height=50, width=140)

        # Clock
        self.lbl_clock = Label(self.root, text="Welcome to SMART WAREHOUSE MANAGEMENT\t\t Date:DD-MM-YYYY\t\t Time:HH:MM:SS", font=("times new roman", 15), bg="grey", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # Left menu
        # Left menu frame
        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        LeftMenu.place(x=0, y=104, width=200, height=565)

        # Resized menu logo
        self.menu_image = Image.open("images/menu_im.png")  # Load the menu image
        self.menu_image = self.menu_image.resize((150, 150), Image.Resampling.LANCZOS)  # Resize the image
        self.MenuLogo = ImageTk.PhotoImage(self.menu_image)  # Convert to PhotoImage

        lbl_menuLogo = Label(LeftMenu, image=self.MenuLogo)  # Display the resized image
        lbl_menuLogo.pack(side=TOP, fill=X)

        # Add a menu label
        lbl_menu = Label(LeftMenu, text="Menu", font=("times new roman", 20), bg="black", fg="white", cursor="hand2")
        lbl_menu.pack(side=TOP, fill=X)


        buttons = [
            ("Employee", self.employee),
            ("Supplier", self.supplier),
            ("Category", self.category),
            ("Product", self.product),
            ("Sales", self.sales),
            ("Exit", root.quit)
        ]

        for text, command in buttons:
            btn = Button(LeftMenu, text=text, compound=LEFT, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2", command=command)
            btn.pack(side=TOP, fill=X)

        # Content
        self.lbl_employee = Label(self.root, text="Total Employee\n[ 0 ]", bd=5, relief=RIDGE, bg="#2b6777", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_employee.place(x=300, y=200, height=150, width=300)

        self.lbl_supplier = Label(self.root, text="Total Supplier\n[ 0 ]", bd=5, relief=RIDGE, bg="white", fg="black", font=("goudy old style", 20, "bold"))
        self.lbl_supplier.place(x=650, y=200, height=150, width=300)

        self.lbl_category = Label(self.root, text="Total Category\n[ 0 ]", bd=5, relief=RIDGE, bg="white", fg="black", font=("goudy old style", 20, "bold"))
        self.lbl_category.place(x=650, y=400, height=150, width=300)

        self.lbl_product = Label(self.root, text="Total Product\n[ 0 ]", bd=5, relief=RIDGE, bg="#2b6777", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_product.place(x=300, y=400, height=150, width=300)

        self.lbl_sales = Label(self.root, text="Total Sales\n[ 0 ]", bd=5, relief=RIDGE, bg="#2b6777", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_sales.place(x=1000, y=200, height=350, width=300)

        # Footer
        lbl_footer = Label(self.root, text="SMART WAREHOUSE MANAGEMENT | Developed by Kusumanjali and Sneha priya\nFor any technical issue contact: 91xxxxxx02", font=("times new roman", 12), bg="grey", fg="white")
        lbl_footer.pack(side=BOTTOM, fill=X)
        self.update_content()

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

    def update_content(self):
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            try:
                cur.execute("select * from product")
                product=cur.fetchall()
                self.lbl_product.config(text=f'Total Product\n[ {str(len(product))}]')

                cur.execute("select * from employee")
                employee=cur.fetchall()
                self.lbl_employee.config(text=f'Total Employees\n[ {str(len(employee))}]')

                cur.execute("select * from supplier")
                supplier=cur.fetchall()
                self.lbl_supplier.config(text=f'Total Suppliers\n[ {str(len(supplier))}]')

                cur.execute("select * from category")
                category=cur.fetchall()
                self.lbl_category.config(text=f'Total Category\n[ {str(len(category))}]')

                bill=len(os.listdir('bill'))
                self.lbl_sales.config(text=f'Total Sales\n [{str(bill)}]')

                time_=time.strftime("%I:%M:%S")
                date_=time.strftime("%d-%m-%Y")
                self.lbl_clock.config( text=f"Welcome to SMART WAREHOUSE MANAGEMENT\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
                self.lbl_clock.after(200,self.update_content)

            except Exception as ex:
                messagebox.showerror("Error",f"Error dur to: {str(ex)}",parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python sample_login.py")


if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
