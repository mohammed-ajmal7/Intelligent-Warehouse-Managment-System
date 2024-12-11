from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os

class SupplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x540+220+130")
        self.root.title("WAREHOUSE MANAGEMENT SYSTEM | DEVELOPED BY KUSUMANJALI AND SNEHA PRIYA")
        self.root.config(bg="white")
        self.root.focus_force()
        


        # Load the background image
        self.bg_image = Image.open("images/category back.jpg")  # Replace with your image path

        # Resize the image (Set your desired width and height)
        desired_width = 1700  # Replace with your preferred width
        desired_height = 900  # Replace with your preferred height
        self.bg_image = self.bg_image.resize((desired_width, desired_height), Image.LANCZOS)


        # Convert to PhotoImage
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Set as background
        bg_label = Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)


        # Title
        title = Label(self.root, text="Suppliers Details", font=("Times new roman", 22), bg="black", fg="#dcdcdc")
        title.place(x=50, y=50, width=1440)


        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_sup_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()
        
        # Search frame
        SearchFrame = LabelFrame(self.root, text="Search Employee", font=("Times new roman", 17, "bold"),
                                bg="#fcf4ee", relief=RIDGE)
        SearchFrame.place(x=350, y=130, width=900, height=80)


        lb1_search = Label(SearchFrame, text="Search by Invoice No", bg="white" ,
                                   font=("Times new roman", 16), relief=RIDGE)
        lb1_search.place(x=10, y=10)
        
        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("Times new roman", 17),
                           bg="white")
        txt_search.place(x=210, y=10)
        btn_search = Button(SearchFrame, text="Search", font=("Times new roman", 17), bg="#4caf50",
                            fg="black", cursor="hand2", command=self.search)
        btn_search.place(x=480, y=9, width=170, height=30)

        

        lbl_supplier_invoice = Label(self.root, text="Invoice No.", font=("Times new roman", 17))
        lbl_supplier_invoice.place(x=380, y=230)
        
        txt_supplier_invoice = Entry(self.root, textvariable=self.var_sup_invoice, font=("Times new roman", 17),
                          bg="white")
        txt_supplier_invoice.place(x=540, y=230, width=180)
        
        lbl_name = Label(self.root, text="Name", font=("Times new roman", 17))
        lbl_name.place(x=380, y=280)
        
        txt_name = Entry(self.root, textvariable=self.var_name, font=("Times new roman", 17), bg="white")
        txt_name.place(x=540, y=280, width=340)
        
        # Contact field
        lbl_contact = Label(self.root, text="Contact", font=("Times new roman", 12))
        lbl_contact.place(x=380, y=330)

        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("Times new roman", 12))
        txt_contact.place(x=540, y=330, width=250)
        txt_contact.bind("<FocusOut>", self.validate_contact)

        lbl_desc= Label(self.root, text="Description", font=("Times new roman", 17))
        lbl_desc.place(x=380, y=380)
        
        self.txt_desc = Text(self.root, font=("Times new roman", 17), bg="white")
        self.txt_desc.place(x=540, y=380, width=300, height=60)
       
        btn_add = Button(self.root, text="Save", font=("Times new roman", 17), bg="#2196f3", fg="white",
                         cursor="hand2", command=self.add)
        btn_add.place(x=540, y=460, width=110, height=28)
        btn_update = Button(self.root, text="Update", font=("Times new roman", 17), bg="#4caf50", fg="white",
                            cursor="hand2", command=self.update)
        btn_update.place(x=670, y=460, width=110, height=28)
        btn_delete = Button(self.root, text="Delete", font=("Times new roman", 17), bg="#f44336", fg="white",
                            cursor="hand2", command=self.delete)
        btn_delete.place(x=800, y=460, width=110, height=28)
        btn_clear = Button(self.root, text="Clear", font=("Times new roman", 17), bg="#607d8b", fg="white",
                            cursor="hand2", command=self.clear)
        btn_clear.place(x=930, y=460, width=110, height=28)


        

        emp_frame = Frame(self.root, bd=3, relief=RIDGE)  # Initialize emp_frame
        emp_frame.place(x=2, y=565, relwidth=1, height=230)
        emp_frame.pack()  # Add this line to display the frame

        label = Label(emp_frame, text="Supplier Details", font=("Times New Roman", 17))
        label.pack()

        emp_frame.place(x=2, y=565, relwidth=1, height=230)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        # Set up Treeview with custom styles
        style = ttk.Style()
        style.configure("Treeview", font=("Times new roman", 17), rowheight=25)
        style.configure("Treeview.Heading", font=("Times new roman", 17, "bold"))

        self.supplierTable = ttk.Treeview(emp_frame,
                                          columns=("invoice", "name", "contact", "desc"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)
        self.supplierTable.column("invoice", width=90)
        self.supplierTable.column("name", width=100)
        self.supplierTable.column("contact", width=100)
        self.supplierTable.column("desc", width=100)
        self.supplierTable["show"] = "headings"

        self.supplierTable.heading("invoice", text="Invoice")
        self.supplierTable.heading("name", text="Name")
        self.supplierTable.heading("contact", text="Contact")
        self.supplierTable.heading("desc", text="Description")
        
        self.supplierTable.pack(fill=BOTH,expand=1)
        self.supplierTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()  # Populate supplierTable initially
        
    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This Invoice already assigned, try different", parent=self.root)
                else:
                    cur.execute("INSERT INTO supplier(invoice,name,contact,desc) VALUES(?,?,?,?)", (
                        self.var_sup_invoice.get(),
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0', END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from supplier")
            rows = cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def validate_contact(self, event):
        if not re.match(r"^\d{10}$", self.var_contact.get()):
            messagebox.showerror("Invalid Contact", "Enter a valid 10-digit contact number")
            self.var_contact.set("")
    
    def get_data(self,ev):
        f=self.supplierTable.focus()
        content=(self.supplierTable.item(f))
        row=content['values']
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete('1.0', END)
        self.txt_desc.insert(END,row[3])

    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Invoice", parent=self.root)
                else:
                    cur.execute("update supplier set name=?,contact=?,desc=? where invoice=?", (
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0', END),
                        self.var_sup_invoice.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search Invoice no. should be required", parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=?", (self.var_searchtxt.get(),))
                row = cur.fetchone()
                if row != None:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    self.supplierTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()


    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete ?",parent=self.root)
                    if op==True:
                        cur.execute("delete from supplier where invoice=?",(self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Supplier Deleted Successfully",parent=self.root)
                        self.show()
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0', END)
        self.var_searchtxt.set("")
        self.show()

if __name__ == "__main__":
    root = Tk()
    obj = SupplierClass(root)
    root.mainloop()
