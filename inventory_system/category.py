from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

class CategoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("SMART WAREHOUSE MANAGEMENT | DEVELOPED BY KUSUMANJALI AND SNEHA PRIYA")
        self.root.config(bg="white")
        self.root.focus_force()

         # Load and set the background image
        self.bg3_image = Image.open(r"images/bg3.jpeg")  # Replace with your image path
        self.bg3_image = self.bg3_image.resize((1350, 700), Image.Resampling.LANCZOS)  # Resize to match window size
        self.bg3_photo = ImageTk.PhotoImage(self.bg3_image)
        bg_label = Label(self.root, image=self.bg3_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.im1 = Image.open("images/cat2.jpeg").resize((500, 200))
        self.im1 = ImageTk.PhotoImage(self.im1)
        self.lb1_im1 = Label(self.root, image=self.im1, bd=2, relief=RAISED)
        self.lb1_im1.place(x=50, y=220)

        self.im2 = Image.open("images/cat.jpeg").resize((500, 200))
        self.im2 = ImageTk.PhotoImage(self.im2)
        self.lb1_im2 = Label(self.root, image=self.im2, bd=2, relief=RAISED)
        self.lb1_im2.place(x=580, y=220)

        self.var_cat_id = StringVar()
        self.var_name = StringVar()

        lb1_title = Label(self.root, text="Manage Product Category", font=("goudy old style", 30), bg="#184a45",
                          fg="white", bd=3, relief=RIDGE)
        lb1_title.pack(side=TOP, fill=X, padx=10, pady=20)

        lb1_name = Label(self.root, text="Enter Category Name", font=("goudy old style", 30), bg="white")
        lb1_name.place(x=50, y=100)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 18), bg="lightyellow")
        txt_name.place(x=50, y=170, width=300)

        btn_add = Button(self.root, text="Add", font=("goudy old style", 15), bg="#4caf50", fg="white",
                         cursor="hand2", command=self.add)
        btn_add.place(x=360, y=170, width=150, height=30)

        btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15), bg="red", fg="white",
                            cursor="hand2", command=self.delete)
        btn_delete.place(x=520, y=170, width=150, height=30)

        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=700, y=120, width=380, height=100)

        scrolly = Scrollbar(cat_frame, orient=VERTICAL)
        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)

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
        self.categoryTable.bind("<ButtonRelease-1>",self.get_data)

    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Category Name must be required", parent=self.root)
            else:
                cur.execute("Select * from category where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Category already exists,try different",parent=self.root)
                else:
                    cur.execute("Insert into category (name) values(?)",(self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success","Category added successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        # Connect to the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            # Fetch all category records from the database
            cur.execute("Select * from category")
            rows = cur.fetchall()
            # Clear the categoryTable before inserting new records
            self.categoryTable.delete(*self.categoryTable.get_children())
            # Insert each record into the categoryTable
            for row in rows:
                self.categoryTable.insert('', END, values=row)
        except Exception as ex:
            # Show error message if any exception occurs
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            # Close the database connection
            con.close()

    def delete(self):
        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Category ID must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE cid=?", (self.var_cat_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Category ID", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete ?", parent=self.root)
                    if op==True:
                        cur.execute("DELETE FROM category WHERE cid=?", (self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Category Deleted Successfully", parent=self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self,ev):
        f=self.categoryTable.focus()
        content=(self.categoryTable.item(f))
        row=content['values']
        #print(row)
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])


if __name__ == "__main__":
    root = Tk()
    obj = CategoryClass(root)
    root.mainloop()
