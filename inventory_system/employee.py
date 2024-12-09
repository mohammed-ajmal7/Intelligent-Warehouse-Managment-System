# Import necessary modules
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

# Define the EmployeeClass
class EmployeeClass:
    def __init__(self, root):
        # Initialize the root window
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

        # Search frame
        SearchFrame = LabelFrame(self.root, text="Search Employee", font=("goudy old style", 12, "bold"),
                                 bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=250, y=20, width=600, height=70)

        # Options
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby,
                                   values=("Select", "Email", "Name", "Contact"), state='readonly',
                                   justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15),
                           bg="lightyellow")
        txt_search.place(x=200, y=10)
        btn_search = Button(SearchFrame, text="Search", font=("goudy old style", 15), bg="#4caf50",
                            fg="white", cursor="hand2", command=self.search)
        btn_search.place(x=410, y=9, width=150, height=30)

        # Title
        title = Label(self.root, text="Employee Details", font=("goudy old style", 15), bg="#0f4d7d", fg="white")
        title.place(x=50, y=100, width=1000)

        # Content
        # Row1
        lbl_empid = Label(self.root, text="Emp ID", font=("goudy old style", 15), bg="white")
        lbl_empid.place(x=50, y=150)
        lbl_gender = Label(self.root, text="Gender", font=("goudy old style", 15), bg="white")
        lbl_gender.place(x=350, y=150)
        lbl_contact = Label(self.root, text="Contact", font=("goudy old style", 15), bg="white")
        lbl_contact.place(x=750, y=150)

        txt_empid = Entry(self.root, textvariable=self.var_emp_id, font=("goudy old style", 15),
                          bg="lightyellow")
        txt_empid.place(x=150, y=150, width=180)
        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select", "Male", "Female", "Others"),
                                  state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_gender.place(x=500, y=150, width=180)
        cmb_gender.current(0)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15),
                            bg="lightyellow")
        txt_contact.place(x=850, y=150, width=180)

        # Row2
        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15), bg="white")
        lbl_name.place(x=50, y=190)
        lbl_dob = Label(self.root, text="DOB", font=("goudy old style", 15), bg="white")
        lbl_dob.place(x=350, y=190)
        lbl_doj = Label(self.root, text="DOJ", font=("goudy old style", 15), bg="white")
        lbl_doj.place(x=750, y=190)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow")
        txt_name.place(x=150, y=190, width=180)
        txt_dob = Entry(self.root, textvariable=self.var_dob, font=("goudy old style", 15), bg="lightyellow")
        txt_dob.place(x=500, y=190, width=180)
        txt_doj = Entry(self.root, textvariable=self.var_doj, font=("goudy old style", 15), bg="lightyellow")
        txt_doj.place(x=850, y=190, width=180)

        # Row3
        lbl_email = Label(self.root, text="E-Mail", font=("goudy old style", 15), bg="white")
        lbl_email.place(x=50, y=230)
        lbl_pass = Label(self.root, text="Password", font=("goudy old style", 15), bg="white")
        lbl_pass.place(x=350, y=230)
        lbl_utype = Label(self.root, text="User Type", font=("goudy old style", 15), bg="white")
        lbl_utype.place(x=750, y=230)

        txt_email = Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15), bg="lightyellow")
        txt_email.place(x=150, y=230, width=180)
        txt_pass = Entry(self.root, textvariable=self.var_pass, font=("goudy old style", 15), bg="lightyellow")
        txt_pass.place(x=500, y=230, width=180)
        cmb_utype = ttk.Combobox(self.root, textvariable=self.var_utype, values=("Admin", "Employee"),
                                  state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_utype.place(x=850, y=230, width=180)
        cmb_utype.current(0)

        # Row4
        lbl_address = Label(self.root, text="Address", font=("goudy old style", 15), bg="white")
        lbl_address.place(x=50, y=270)
        lbl_salary = Label(self.root, text="Salary", font=("goudy old style", 15), bg="white")
        lbl_salary.place(x=500, y=270)

        self.txt_address = Text(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_address.place(x=150, y=270, width=300, height=60)
        txt_salary = Entry(self.root, textvariable=self.var_salary, font=("goudy old style",15), bg="lightyellow")
        txt_salary.place(x=600, y=270, width=180)
        
        # Buttons
        btn_add = Button(self.root, text="Save", font=("goudy old style", 15), bg="#2196f3", fg="white",
                         cursor="hand2", command=self.add)
        btn_add.place(x=500, y=305, width=110, height=28)
        btn_update = Button(self.root, text="Update", font=("goudy old style", 15), bg="#4caf50", fg="white",
                            cursor="hand2", command=self.update)
        btn_update.place(x=620, y=305, width=110, height=28)
        btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15), bg="#f44336", fg="white",
                            cursor="hand2", command=self.delete)
        btn_delete.place(x=740, y=305, width=110, height=28)
        btn_clear = Button(self.root, text="Clear", font=("goudy old style", 15), bg="#607d8b", fg="white",
                            cursor="hand2", command=self.clear)
        btn_clear.place(x=860, y=305, width=110, height=28)

        # Employee details
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=350, relwidth=1, height=150)

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
