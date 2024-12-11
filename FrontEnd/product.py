from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk


class ProductClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("WAREHOUSE MANAGEMENT SYSTEM | DEVELOPED BY KUSUMANJALI AND SNEHA PRIYA")
        self.root.config(bg="white")
        self.root.focus_force()

        # Load and set the background image
        self.bg_image = Image.open("images/category back.jpg")
        self.bg_image = self.bg_image.resize((1540, 800), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title
        title = Label(self.root, text="Product Details", font=("Times New Roman", 22), bg="black", fg="white")
        title.place(x=50, y=50, width=1450)

        # Variables
        self.var_pid = StringVar()
        self.cat_list = []
        self.sup_list = []
        self.var_cat = StringVar()
        self.var_sup = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.fetch_cat_sup()

        # Product Frame
       # Create the Frame and set all required properties
        product_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="#fcf4ee")

# Use place() to position the Frame
        product_Frame.place(x=170, y=150, width=550, height=580)



        title = Label(product_Frame, text="Manage Products Details", font=("Times New Roman", 20), bg="#0f4d7d", fg="white")
        title.pack(side=TOP, fill=X)

        Label(product_Frame, text="Category", font=("Times New Roman", 18)).place(x=30, y=60)
        Label(product_Frame, text="Supplier", font=("Times New Roman", 18)).place(x=30, y=110)
        Label(product_Frame, text="Name", font=("Times New Roman", 18)).place(x=30, y=160)
        Label(product_Frame, text="Price", font=("Times New Roman", 18)).place(x=30, y=210)
        Label(product_Frame, text="Quantity", font=("Times New Roman", 18)).place(x=30, y=260)
        Label(product_Frame, text="Status", font=("Times New Roman", 18)).place(x=30, y=310)

        ttk.Combobox(product_Frame, textvariable=self.var_cat, values=self.cat_list, state='readonly',
                     justify=CENTER, font=("Times New Roman", 15)).place(x=150, y=60, width=200)
        ttk.Combobox(product_Frame, textvariable=self.var_sup, values=self.sup_list, state='readonly',
                     justify=CENTER, font=("Times New Roman", 15)).place(x=150, y=110, width=200)
        Entry(product_Frame, textvariable=self.var_name, font=("Times New Roman", 15), bg="white").place(x=150, y=160, width=200)
        Entry(product_Frame, textvariable=self.var_price, font=("Times New Roman", 15), bg="white").place(x=150, y=210, width=200)
        Entry(product_Frame, textvariable=self.var_qty, font=("Times New Roman", 15), bg="white").place(x=150, y=260, width=200)

        ttk.Combobox(product_Frame, textvariable=self.var_status, values=("Active", "Inactive"), state='readonly',
                     justify=CENTER, font=("Times New Roman", 15)).place(x=150, y=310, width=200)
        self.var_status.set("Active")

        Button(product_Frame, text="Save", font=("Times New Roman", 15), bg="#2196f3", fg="white", cursor="hand2",
               command=self.add).place(x=10, y=400, width=100, height=40)
        Button(product_Frame, text="Update", font=("Times New Roman", 15), bg="#4caf50", fg="white", cursor="hand2",
               command=self.update).place(x=120, y=400, width=100, height=40)
        Button(product_Frame, text="Delete", font=("Times New Roman", 15), bg="#f44336", fg="white", cursor="hand2",
               command=self.delete).place(x=230, y=400, width=100, height=40)
        Button(product_Frame, text="Clear", font=("Times New Roman", 15), bg="#607d8b", fg="white", cursor="hand2",
               command=self.clear).place(x=340, y=400, width=100, height=40)

        # Search Box
        SearchFrame = LabelFrame(self.root, text="Search Product", font=("Times New Roman", 12, "bold"),
                                 bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=750, y=150, width=700, height=80)

        ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=("Select", "Category", "Supplier", "Name"),
                     state='readonly', justify=CENTER, font=("Times New Roman", 15)).place(x=10, y=10, width=180)
        self.var_searchby.set("Select")

        Entry(SearchFrame, textvariable=self.var_searchtxt, font=("Times New Roman", 15), bg="white").place(x=200, y=10)
        Button(SearchFrame, text="Search", font=("Times New Roman", 15), bg="#4caf50", fg="white", cursor="hand2",
               command=self.search).place(x=410, y=9, width=150, height=30)

        # Table Frame
        p_frame = Frame(self.root, bd=3, relief=RIDGE)
        p_frame.place(x=750, y=235, width=700, height=490)

        scrolly = Scrollbar(p_frame, orient=VERTICAL)
        scrollx = Scrollbar(p_frame, orient=HORIZONTAL)

        self.product_table = ttk.Treeview(p_frame, columns=("pid", "Category", "Supplier", "name", "price", "qty", "status"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)
        self.product_table["show"] = "headings"

        for col in ("pid", "Category", "Supplier", "name", "price", "qty", "status"):
            self.product_table.heading(col, text=col.capitalize())
            self.product_table.column(col, width=100)

        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)
        self.show()

        # Set up Treeview with custom styles
        style = ttk.Style()
        style.configure("Treeview", font=("Times new roman", 15), rowheight=35)
        style.configure("Treeview.Heading", font=("Times new roman", 15, "bold"))


    def fetch_cat_sup(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM category")
            self.cat_list = ["Select"] + [row[0] for row in cur.fetchall()]
            cur.execute("SELECT name FROM supplier")
            self.sup_list = ["Select"] + [row[0] for row in cur.fetchall()]
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_cat.get() == "Select" or self.var_sup.get() == "Select" or self.var_name.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE name=?", (self.var_name.get(),))
                if cur.fetchone():
                    messagebox.showerror("Error", "Product already exists", parent=self.root)
                else:
                    cur.execute("INSERT INTO product (Category, Supplier, name, price, qty, status) VALUES (?, ?, ?, ?, ?, ?)", (
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Product added successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.product_table.focus()
        content = self.product_table.item(f)
        row = content['values']
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_sup.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_status.set(row[6])

    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Please select a product from the list", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
                if not cur.fetchone():
                    messagebox.showerror("Error", "Invalid Product", parent=self.root)
                else:
                    cur.execute("UPDATE product SET Category=?, Supplier=?, name=?, price=?, qty=?, status=? WHERE pid=?", (
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                        self.var_pid.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Product updated successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Please select a product from the list", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
                if not cur.fetchone():
                    messagebox.showerror("Error", "Invalid Product", parent=self.root)
                else:
                    if messagebox.askyesno("Confirm", "Do you really want to delete this product?", parent=self.root):
                        cur.execute("DELETE FROM product WHERE pid=?", (self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Success", "Product deleted successfully", parent=self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_pid.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.var_status.set("Active")
        self.show()

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select a search by option", parent=self.root)
            elif not self.var_searchtxt.get():
                messagebox.showerror("Error", "Search input is required", parent=self.root)
            else:
                query = f"SELECT * FROM product WHERE {self.var_searchby.get()} LIKE '%{self.var_searchtxt.get()}%'"
                cur.execute(query)
                rows = cur.fetchall()
                if rows:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert("", END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = ProductClass(root)
    root.mainloop()
