# Import necessary modules
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk


# Define the EmployeeClass
class EmployeeClass:
    def __init__(self, root):
        # Initialize the root window
        self.root = root
        self.root.geometry("1100x685+225+130")
        self.root.title("WAREHOUSE MANAGEMENT SYSTEM | DEVELOPED BY KUSUMANJALI AND SNEHA PRIYA")
        self.root.config(bg="#fcf4ee")
        self.root.focus_force()
        

        # Load and set the background image
        self.bg_image = Image.open("images/category back.jpg")  # Replace with your image file
        self.bg_image = self.bg_image.resize((1540, 800), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
      


        # All variables
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_emp_id = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()


         
          # Title
        title = Label(self.root, text="Employee Details", font=("Times new roman", 22), bg="black", fg="#fcf4ee")
        title.place(x=50, y=50, width=1450)
        
        # Search frame
        SearchFrame = LabelFrame(self.root, text="Search Employee", font=("Times new roman", 17, "bold"),
                                bg="#fcf4ee", relief=RIDGE)
        SearchFrame.place(x=350, y=130, width=900, height=80)

        # Options
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby,
                                   values=("Select", "Email", "Name", "Contact"), state='readonly',
                                   justify=CENTER, font=("Times new roman", 17))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("Times new roman", 17),
                           bg="white")
        txt_search.place(x=200, y=10)
        btn_search = Button(SearchFrame, text="Search", font=("Times new roman", 17), bg="#4caf50",
                            fg="black", cursor="hand2", command=self.search)
        btn_search.place(x=460, y=9, width=170, height=30)

       

        # Content
        # Row1
        lbl_empid = Label(self.root, text="Emp ID", font=("Times new roman", 17))
        lbl_empid.place(x=305, y=225)
        lbl_gender = Label(self.root, text="Gender", font=("Times new roman", 17))
        lbl_gender.place(x=680, y=225)
        lbl_contact = Label(self.root, text="Contact", font=("Times new roman", 17))
        lbl_contact.place(x=1010, y=225)

        txt_empid = Entry(self.root, textvariable=self.var_emp_id, font=("Times new roman", 17), bg="#fcf4ee")
        txt_empid.place(x=410, y=225, width=180)
        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select", "Male", "Female", "Others"),
                                  state='readonly', justify=CENTER, font=("Times new roman", 17))
        cmb_gender.place(x=790, y=225, width=180)
        cmb_gender.current(0)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("Times new roman", 17),
                            bg="#fcf4ee")
        txt_contact.place(x=1100, y=225, width=180)

        # Row2
        lbl_name = Label(self.root, text="Name", font=("Times new roman", 17))
        lbl_name.place(x=305, y=275)
        lbl_dob = Label(self.root, text="DOB", font=("Times new roman", 17))
        lbl_dob.place(x=680, y=275)
        lbl_doj = Label(self.root, text="DOJ", font=("Times new roman", 17))
        lbl_doj.place(x=1010, y=275)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("Times new roman", 17), bg="#fcf4ee")
        txt_name.place(x=410, y=275, width=180)
        txt_dob = Entry(self.root, textvariable=self.var_dob, font=("Times new roman", 17), bg="#fcf4ee")
        txt_dob.place(x=790, y=275, width=180)
        txt_doj = Entry(self.root, textvariable=self.var_doj, font=("Times new roman", 17), bg="#fcf4ee")
        txt_doj.place(x=1100, y=275, width=180)

        # Row3
        lbl_email = Label(self.root, text="E-Mail", font=("Times new roman", 17))
        lbl_email.place(x=305, y=320)
        lbl_pass = Label(self.root, text="Password", font=("Times new roman", 17))
        lbl_pass.place(x=680, y=320)
        lbl_utype = Label(self.root, text="User Type", font=("Times new roman", 17))
        lbl_utype.place(x=1010, y=320)

        txt_email = Entry(self.root, textvariable=self.var_email, font=("Times new roman", 17), bg="#fcf4ee")
        txt_email.place(x=410, y=320, width=180)
        txt_pass = Entry(self.root, textvariable=self.var_pass, font=("Times new roman", 17), bg="#fcf4ee")
        txt_pass.place(x=790, y=320, width=180)
        cmb_utype = ttk.Combobox(self.root, textvariable=self.var_utype, values=("Admin", "Employee"),
                                  state='readonly', justify=CENTER, font=("Times new roman", 17))
        cmb_utype.place(x=1010, y=320, width=180)
        cmb_utype.current(0)

        # Row4
        lbl_address = Label(self.root, text="Address", font=("Times new roman", 17))
        lbl_address.place(x=305, y=370)
        lbl_salary = Label(self.root, text="Salary", font=("Times new roman", 17))
        lbl_salary.place(x=680, y=370)

        self.txt_address = Text(self.root, font=("Times new roman", 17), bg="#fcf4ee")
        self.txt_address.place(x=410, y=370, width=255, height=80)
        txt_salary = Entry(self.root, textvariable=self.var_salary, font=("Times new roman",17), bg="#fcf4ee")
        txt_salary.place(x=790, y=370, width=180)
        
        # Buttons
        btn_add = Button(self.root, text="Save", font=("Times new roman", 17), bg="#2196f3", fg="black",
                         cursor="hand2", command=self.add)
        btn_add.place(x=1010, y=370, width=110, height=28)
        btn_update = Button(self.root, text="Update", font=("Times new roman", 17), bg="#4caf50", fg="black",
                            cursor="hand2", command=self.update)
        btn_update.place(x=790, y=420, width=110, height=28)
        btn_delete = Button(self.root, text="Delete", font=("Times new roman", 17), bg="#f44336", fg="black",
                            cursor="hand2", command=self.delete)
        btn_delete.place(x=920, y=420, width=110, height=28)
        btn_clear = Button(self.root, text="Clear", font=("Times new roman", 17), bg="#607d8b", fg="black",
                            cursor="hand2", command=self.clear)
        btn_clear.place(x=1040, y=420, width=110, height=28)



        style = ttk.Style()
        style.configure("Treeview", font=("Times New Roman", 16), rowheight=30)  # Set font size and row height
        style.configure("Treeview.Heading", font=("Times New Roman", 16, "bold"))  # 

        # Employee details
        emp_frame = Frame(self.root, bd=5, relief=RIDGE)
        emp_frame.place(x=0, y=570, relwidth=1, height=225)
        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.EmployeeTable = ttk.Treeview(emp_frame,
                                          columns=("eid", "name", "email", "gender", "contact", "dob", "doj",
                                                   "pass", "utype", "address", "salary"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)
        self.EmployeeTable.column("eid", width=90)
        self.EmployeeTable.column("name", width=100)
        self.EmployeeTable.column("email", width=100)
        self.EmployeeTable.column("gender", width=100)
        self.EmployeeTable.column("contact", width=100)
        self.EmployeeTable.column("dob", width=100)
        self.EmployeeTable.column("doj", width=100)
        self.EmployeeTable.column("pass", width=100)
        self.EmployeeTable.column("utype", width=100)
        self.EmployeeTable.column("address", width=100)
        self.EmployeeTable.column("salary", width=100)
        self.EmployeeTable["show"] = "headings"

        self.EmployeeTable.heading("eid", text="EMP ID")
        self.EmployeeTable.heading("name", text="Name")
        self.EmployeeTable.heading("email", text="E-Mail")
        self.EmployeeTable.heading("gender", text="Gender")
        self.EmployeeTable.heading("contact", text="Contact")
        self.EmployeeTable.heading("dob", text="DOB")
        self.EmployeeTable.heading("doj", text="Doj")
        self.EmployeeTable.heading("pass", text="Password")
        self.EmployeeTable.heading("utype", text="Usertype")
        self.EmployeeTable.heading("address", text="Address")
        self.EmployeeTable.heading("salary", text="Salary")
        self.EmployeeTable.pack(fill=BOTH,expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()  # Populate EmployeeTable initially
        
    # Function to add an employee
    def add(self):
        # Connect to the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            # Validate if Employee ID is provided
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            else:
                # Check if the Employee ID already exists
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This Employee ID already assigned, try different", parent=self.root)
                else:
                    # Insert the employee details into the database
                    cur.execute("INSERT INTO employee(eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) VALUES(?,?,?,?,?,?,?,?,?,?,?)", (
                        self.var_emp_id.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get('1.0', END),
                        self.var_salary.get(),
                    ))
                    # Commit changes to the database
                    con.commit()
                    messagebox.showinfo("Success", "Employee added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            # Show error message if any exception occurs
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            # Close the database connection
            con.close()

    # Function to display all employees
    def show(self):
        # Connect to the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            # Fetch all employee records from the database
            cur.execute("Select * from employee")
            rows = cur.fetchall()
            # Clear the EmployeeTable before inserting new records
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            # Insert each record into the EmployeeTable
            for row in rows:
                self.EmployeeTable.insert('', END, values=row)
        except Exception as ex:
            # Show error message if any exception occurs
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            # Close the database connection
            con.close()
    def get_data(self,ev):
        f=self.EmployeeTable.focus()
        content=(self.EmployeeTable.item(f))
        row=content['values']
        #print(row)
        self.var_emp_id.set(row[0])
        self.var_name .set(row[1])
        self.var_email .set(row[2])
        self.var_gender .set(row[3])
        self.var_contact .set(row[4])
        self.var_dob .set(row[5])
        self.var_doj .set(row[6])
        self.var_pass .set(row[7])
        self.var_utype .set(row[8])
        self.txt_address.delete('1.0', END)
        self.txt_address.insert(END,row[9])
        self.var_salary .set(row[10])

    def update(self):
        
        # Connect to the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            # Validate if Employee ID is provided
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            else:
                # Check if the Employee ID already exists
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
                else:
                    # Insert the employee details into the database
                    cur.execute("update employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? where eid=?", (
                        
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.txt_address.get('1.0', END),
                        self.var_salary.get(),
                        self.var_emp_id.get(),
                    ))
                    # Commit changes to the database
                    con.commit()
                    messagebox.showinfo("Success", "Employee updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            # Show error message if any exception occurs
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            # Close the database connection
            con.close()


    # Function to search for an employee
    def search(self):
    # Implement search functionality
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
        # Validate the search criteria
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Please select a search criteria.", parent=self.root)
                return

        # Fetch employee records from the database based on search criteria
            cur.execute("SELECT * FROM employee WHERE {} LIKE ?".format(self.var_searchby.get()),
                    ('%' + self.var_searchtxt.get() + '%',))
            rows = cur.fetchall()
            if rows:
            # Clear the EmployeeTable before inserting new records
                self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            # Insert each record into the EmployeeTable
                for row in rows:
                    self.EmployeeTable.insert('', END, values=row)
            else:
                messagebox.showerror("Error", "No record found.", parent=self.root)
        except Exception as ex:
        # Show error message if any exception occurs
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
        # Close the database connection
            con.close()


    # Function to delete an employee record
    def delete(self):
        # Implement delete functionality
         # Connect to the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            else:
                # Check if the Employee ID already exists
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete ?",parent=self.root)
                    if op==True:

                        cur.execute("delete from employee where eid=?",(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Employee Deleted Successfully",parent=self.root)
                        self.show()
                        self.clear()

        except Exception as ex:
            # Show error message if any exception occurs
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
    # Function to clear all input fields
    def clear(self):
        # Clear all input fields
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("")
        self.txt_address.delete('1.0', END)
        self.var_salary.set("")


    
# Main function
if __name__ == "__main__":
    root = Tk()
    obj = EmployeeClass(root)
    root.mainloop()
