from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

class ProductClass:
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

        self.var_pid = StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.var_cat = StringVar()
        self.var_sup = StringVar()
        self.fetch_cat_sup()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        product_Frame = Frame(self.root, bd=2, relief=RIDGE)
        product_Frame.place(x=10, y=10, width=450, height=480)

        title = Label(product_Frame, text="Manage Products Details", font=("goudy old style", 18), bg="black",
                      fg="white").pack(side=TOP, fill=X)

        lb1_category = Label(product_Frame, text="Category", font=("goudy old style", 18), bg="white").place(x=30,
                                                                                                              y=60)
        lb1_supplier = Label(product_Frame, text="Supplier", font=("goudy old style", 18), bg="white").place(x=30,
                                                                                                              y=110)
        lb1_product_name = Label(product_Frame, text="Name", font=("goudy old style", 18), bg="white").place(x=30,
                                                                                                                y=160)
        lb1_price = Label(product_Frame, text="Price", font=("goudy old style", 18), bg="white").place(x=30, y=210)
        lb1_qty = Label(product_Frame, text="Quantity", font=("goudy old style", 18), bg="white").place(x=30, y=260)
        lb1_status = Label(product_Frame, text="Status", font=("goudy old style", 18), bg="white").place(x=30, y=310)

        cmb_cat = ttk.Combobox(product_Frame, textvariable=self.var_cat,
                               values=self.cat_list, state='readonly',
                               justify=CENTER, font=("goudy old style", 15))
        cmb_cat.place(x=150, y=60, width=200)

        cmb_sup = ttk.Combobox(product_Frame, textvariable=self.var_sup,
                               values=self.sup_list, state='readonly',
                               justify=CENTER, font=("goudy old style", 15))
        cmb_sup.place(x=150, y=110, width=200)

        txt_name = Entry(product_Frame, textvariable=self.var_name,
                         font=("goudy old style", 15), bg='lightyellow').place(x=150, y=160, width=200)

        txt_price = Entry(product_Frame, textvariable=self.var_price,
                          font=("goudy old style", 15), bg='lightyellow').place(x=150, y=210, width=200)
        txt_qty = Entry(product_Frame, textvariable=self.var_qty,
                        font=("goudy old style", 15), bg='lightyellow').place(x=150, y=260, width=200)

        cmb_status = ttk.Combobox(product_Frame, textvariable=self.var_status,
                                  values=("Active", "Inactive"), state='readonly',
                                  justify=CENTER, font=("goudy old style", 15))
        cmb_status.place(x=150, y=310, width=200)
        cmb_status.current(0)

        btn_add = Button(product_Frame, text="Save", font=("goudy old style", 15), bg="#2196f3", fg="white",
                         cursor="hand2", command=self.add)
        btn_add.place(x=10, y=400, width=100, height=40)
        btn_update = Button(product_Frame, text="Update", font=("goudy old style", 15), bg="#4caf50", fg="white",
                            cursor="hand2", command=self.update)
        btn_update.place(x=120, y=400, width=100, height=40)
        btn_delete = Button(product_Frame, text="Delete", font=("goudy old style", 15), bg="#f44336", fg="white",
                            cursor="hand2", command=self.delete)
        btn_delete.place(x=230, y=400, width=100, height=40)
        btn_clear = Button(product_Frame, text="Clear", font=("goudy old style", 15), bg="#607d8b", fg="white",
                           cursor="hand2", command=self.clear)
        btn_clear.place(x=340, y=400, width=100, height=40)

        SearchFrame = LabelFrame(self.root, text="Search Product", font=("goudy old style", 12, "bold"),
                                 bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=480, y=10, width=600, height=80)

        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby,
                                  values=("Select", "Category", "Supplier", "Name"), state='readonly',
                                  justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15),
                           bg="lightyellow")
        txt_search.place(x=200, y=10)
        btn_search = Button(SearchFrame, text="Search", font=("goudy old style", 15), bg="#4caf50",
                            fg="white", cursor="hand2", command=self.search)
        btn_search.place(x=410, y=9, width=150, height=30)

        p_frame = Frame(self.root, bd=3, relief=RIDGE)
        p_frame.place(x=480, y=100, width=600, height=390)

        scrolly = Scrollbar(p_frame, orient=VERTICAL)
        scrollx = Scrollbar(p_frame, orient=HORIZONTAL)

        self.product_table = ttk.Treeview(p_frame,
                                          columns=("pid", "Supplier", "Category", "name", "price", "qty", "status"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)
        self.product_table.column("pid", width=90)
        self.product_table.column("Category", width=100)
        self.product_table.column("Supplier", width=100)
        self.product_table.column("name", width=100)
        self.product_table.column("price", width=100)
        self.product_table.column("qty", width=100)
        self.product_table.column("status", width=100)
        self.product_table["show"] = "headings"
        self.product_table.heading("pid", text="P ID")
        self.product_table.heading("Category", text="Category")
        self.product_table.heading("Supplier", text="Supplier")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("qty", text="Qty")
        self.product_table.heading("status", text="Status")
        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    def fetch_cat_sup(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        try:
            cur.execute("SELECT name FROM category ")
            cat = cur.fetchall()
            if len(cat) > 0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])

            cur.execute("SELECT name FROM supplier ")
            sup = cur.fetchall()
            if len(sup) > 0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_cat.get() == "Select" or self.var_cat.get() == "Empty" or \
               self.var_sup.get() == "Select" or self.var_sup.get() == "Empty" or \
               self.var_name.get() == "":
                messagebox.showerror("Error", "All fields must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This Product already present, try different", parent=self.root)
                else:
                    cur.execute("INSERT INTO product(Category, Supplier, name, price, qty, status) VALUES(?,?,?,?,?,?)", (
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Product added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from product")
            rows = cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.product_table.focus()
        content = (self.product_table.item(f))
        row = content['values']
        if row:
            self.var_pid.set(row[0])
            self.var_sup.set(row[1])
            self.var_cat.set(row[2])
            self.var_name.set(row[3])
            self.var_price.set(row[4])
            self.var_qty.set(row[5])
            self.var_status.set(row[6])

    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error", "Product ID must be required", parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",
                            (self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    cur.execute("update product set Category=?,Supplier=?,name=?,price=?,qty=?,status=? where pid=?",(
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                        self.var_pid.get()

                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product updated successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Please select a search criteria.", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
            # Correcting SQL query string concatenation
                cur.execute("SELECT * FROM product WHERE " + self.var_searchby.get() + " LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cur.fetchall()
            
                if len(rows) != 0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found.", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
       

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error", "Select product from list", parent=self.root)
            else:
                cur.execute("Select * from product where pid=?", (self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid product",paernt=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==TRUE:
                        cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Success", "Product Deleted Successfully", parent=self.root)
                        self.clear()
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
        self.var_searchby("Select")
        self.var_searchtxt("")
        self.var_status.set("Active")
        self.show()

if __name__ == "__main__":
    root = Tk()
    obj = ProductClass(root)
    root.mainloop()
