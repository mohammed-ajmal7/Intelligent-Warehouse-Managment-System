from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

class CategoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("WAREHOUSE MANAGEMENT SYSTEM | DEVELOPED BY KUSUMANJALI AND SNEHA PRIYA")
        self.root.config(bg="white")
        self.root.focus_force()

        # Load the background image
        self.bg_image = Image.open("images/category back.jpg")  # Replace with your image path
        desired_width = 1540  # Set your desired width
        desired_height = 900  # Set your desired height
        self.bg_image = self.bg_image.resize((desired_width, desired_height), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        # Attach the background image to a Label
        self.bg_label = Label(self.root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Variables
        self.var_cat_id = StringVar()
        self.var_name = StringVar()

        # Title Label
        lb1_title = Label(self.root, text="Manage Product Category", font=("Times new roman", 25), bg="black",
                          fg="white", bd=3, relief=RIDGE)
        lb1_title.pack(side=TOP, fill=X, padx=40, pady=90)

        # Category Name Label and Entry
        lb1_name = Label(self.root, text="Enter Category Name", font=("Times new roman", 22))
        lb1_name.place(x=170, y=210)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("Times new roman", 20), bg="#f2f5f6")
        txt_name.place(x=170, y=270, width=300)

        # Buttons
        btn_add = Button(self.root, text="Add", font=("Times new roman", 20), bg="#4caf50", fg="white",
                         cursor="hand2", command=self.add)
        btn_add.place(x=170, y=320, width=140, height=30)

        btn_delete = Button(self.root, text="Delete", font=("Times new roman", 20), bg="red", fg="white",
                            cursor="hand2", command=self.delete)
        btn_delete.place(x=320, y=320, width=140, height=30)

        # Category Table Frame
        cat_frame = Frame(self.root, bd=6, relief=RIDGE)
        cat_frame.place(x=800, y=200, width=500, height=470)

        scrolly = Scrollbar(cat_frame, orient=VERTICAL)
        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)

        # Set up Treeview with custom styles
        style = ttk.Style()
        style.configure("Treeview", font=("Times new roman", 20), rowheight=35)
        style.configure("Treeview.Heading", font=("Times new roman", 20, "bold"))

        self.categoryTable = ttk.Treeview(cat_frame,
                                          columns=("cid", "name"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.categoryTable.xview)
        scrolly.config(command=self.categoryTable.yview)
        self.categoryTable.column("cid", width=90)
        self.categoryTable.column("name", width=100)
        self.categoryTable["show"] = "headings"
        self.categoryTable.heading("cid", text="C ID")
        self.categoryTable.heading("name", text="Name")
        self.categoryTable.pack(fill=BOTH, expand=1)
        self.categoryTable.bind("<ButtonRelease-1>", self.get_data)

        # Show existing categories
        self.show()

    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Category Name must be required", parent=self.root)
            else:
                cur.execute("Select * from category where name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Category already exists, try a different one", parent=self.root)
                else:
                    cur.execute("Insert into category (name) values(?)", (self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Category added successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from category")
            rows = cur.fetchall()
            self.categoryTable.delete(*self.categoryTable.get_children())
            for row in rows:
                self.categoryTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Category Name must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Category Name", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op:
                        cur.execute("DELETE FROM category WHERE name=?", (self.var_name.get(),))
                        con.commit()
                        cur.execute("SELECT rowid, name FROM category ORDER BY rowid")
                        rows = cur.fetchall()
                        for index, (rowid, name) in enumerate(rows, start=1):
                            cur.execute("UPDATE category SET cid=? WHERE rowid=?", (index, rowid))
                        con.commit()
                        messagebox.showinfo("Delete", "Category Deleted Successfully", parent=self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.categoryTable.focus()
        content = self.categoryTable.item(f)
        row = content['values']
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])


if __name__ == "__main__":
    root = Tk()
    obj = CategoryClass(root)
    root.mainloop()
