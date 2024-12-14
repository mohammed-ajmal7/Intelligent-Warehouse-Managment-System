from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import time
import os
import tempfile


class BillClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("SMART WAREHOUSE MANAGEMENT SYSTEM")
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0


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

        # Logout button
        btn_logout = Button(self.root, text="Logout", command=self.logout,font=("times new roman", 15, "bold"), bg="white", cursor="hand2")
        btn_logout.place(x=1300, y=10, height=50, width=150)

        # Clock
        self.lbl_clock = Label(self.root, text="Welcome to Warehouse Management System\t\t Date:DD-MM-YYYY\t\t Time:HH:MM:SS", font=("times new roman", 15), bg="#f2f5f6", fg="black")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # Product Frame
        
        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=20,y=110,width=488,height=595)

        pTitle=Label(ProductFrame1,text="All Products",font=("Times new roman",20,"bold"),bg="black",fg="white").pack(side=TOP,fill=X)

        #product search frame
        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=475,height=455)

        self.var_search=StringVar()
        lbl_search=Label(ProductFrame2,text="Search Product | By Name",font=("times new roman",17,"bold"),bg="white",fg="black").place(x=2,y=10)

        lbl_search=Label(ProductFrame2,text="Product Name",font=("times new roman",17,"bold"),bg="white").place(x=2,y=50)
        txt_search=Entry(ProductFrame2,font=("times new roman",17),bg="lightgray", textvariable=self.var_search).place(x=160,y=55,width=150,height=22)
        btn_search=Button(ProductFrame2,text="Search",command=self.search,font=("Times new roman",17),bg="lightgray",fg="black",cursor="hand2").place(x=340,y=50,width=100,height=25)
        btn_show_all=Button(ProductFrame2,text="Show All",command=self.show
                            ,font=("Times new roman",17),bg="lightgray",fg="black",cursor="hand2").place(x=340,y=10,width=100,height=25)

        #product detail frame
        ProductFrame3 = Frame(ProductFrame1, bd=3, relief=RIDGE)
        ProductFrame3.place(x=2, y=140, width=475, height=450)

        scrolly = Scrollbar(ProductFrame3, orient=VERTICAL)
        scrollx = Scrollbar(ProductFrame3, orient=HORIZONTAL)

        # Set up Treeview with custom styles
        style = ttk.Style()
        style.configure("Treeview", font=("Times new roman", 15), rowheight=35)
        style.configure("Treeview.Heading", font=("Times new roman", 15, "bold"))


        self.product_Table = ttk.Treeview(ProductFrame3,
                                          columns=("pid", "name", "price", "qty","status"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)
        self.product_Table.column("pid", width=40)
        self.product_Table.column("name", width=100)
        self.product_Table.column("price", width=100)
        self.product_Table.column("qty", width=40)
        self.product_Table.column("status", width=90)
        self.product_Table["show"] = "headings"

        self.product_Table.heading("pid", text="PID")
        self.product_Table.heading("name", text="Name")
        self.product_Table.heading("price", text="Price")
        self.product_Table.heading("qty", text="QTY")
        self.product_Table.heading("status", text="Status")
        self.product_Table.pack(fill=BOTH,expand=1)
        #self.product_Table.bind("<ButtonRelease-1>",self.get_data)
        lbl_note=Label(ProductFrame1,text="Note:'Enter 0 Quantity to remove product from the Cart'",font=("goudy old style",13),anchor="w",bg="white",fg="red").pack(side=BOTTOM,fill=X)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)


        #customer frame
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=530,y=110,width=455,height=90)

        cTitle=Label(CustomerFrame,text="Customer Details",font=("Times new roman",20),bg="lightgray").pack(side=TOP,fill=X)
        lbl_name=Label(CustomerFrame,text="Name",font=("times new roman",17),bg="white").place(x=5,y=40)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",15),bg="lightyellow").place(x=70,y=43,width=120)
        
        lbl_contact=Label(CustomerFrame,text="Contact",font=("times new roman",17),bg="white").place(x=230,y=40)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",15),bg="lightyellow").place(x=313,y=43,width=120)
        
        #cal cart frame
        Cal_cart_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Cal_cart_Frame.place(x=530,y=200,width=455,height=390)
        
     
    
        
        # Set up Treeview with custom styles
        style = ttk.Style()
        style.configure("Treeview", font=("Times new roman", 15), rowheight=35)
        style.configure("Treeview.Heading", font=("Times new roman", 15, "bold"))


        #cart frame
        cart_Frame = Frame(Cal_cart_Frame, bd=3, relief=RIDGE)
        cart_Frame.place(x=10, y=8, width=445, height=342)
        self.cartTitle=Label(cart_Frame,text="Cart \tTotal Product: [0]",font=("goudy old style",15),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)

        scrolly = Scrollbar(cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(cart_Frame, orient=HORIZONTAL)


        self.CartTable = ttk.Treeview(cart_Frame,
                                          columns=("pid", "name", "price", "qty"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)
        self.CartTable.column("pid", width=40)
        self.CartTable.column("name", width=90)
        self.CartTable.column("price", width=90)
        self.CartTable.column("qty", width=30)
        self.CartTable["show"] = "headings"

        self.CartTable.heading("pid", text="PID")
        self.CartTable.heading("name", text="Name")
        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("qty", text="QTY")
        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)

        #Add cart frame
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_qty=StringVar()
        self.var_price=StringVar()
        self.var_stock=StringVar()

        Add_CartWidgetsFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Add_CartWidgetsFrame.place(x=530,y=580,width=455,height=120)

        lblp_name=Label(Add_CartWidgetsFrame,text="Product Name",font=("times new romann",15),bg="white").place(x=10,y=10)
        txt_p_name=Entry(Add_CartWidgetsFrame,textvariable=self.var_pname,font=("times new romann",13),bg="lightyellow",state='readonly').place(x=10,y=40,width=160)
        
        lblp_price=Label(Add_CartWidgetsFrame,text="Price per Qty",font=("times new romann",15),bg="white").place(x=200,y=10)
        txt_p_price=Entry(Add_CartWidgetsFrame,textvariable=self.var_price,font=("times new romann",13),bg="lightyellow",state='readonly').place(x=200,y=40,width=130)

        lblp_qty=Label(Add_CartWidgetsFrame,text="Quantity",font=("times new romann",15),bg="white").place(x=360,y=10)
        txt_p_qty=Entry(Add_CartWidgetsFrame,textvariable=self.var_qty,font=("times new romann",13),bg="lightyellow").place(x=370,y=40,width=60)

        self.lbl_inStock=Label(Add_CartWidgetsFrame,text="In Stock",font=("times new romann",12),bg="white")
        self.lbl_inStock.place(x=10,y=80)

        btn_clear_cart=Button(Add_CartWidgetsFrame,text="Clear",command=self.clear_cart,font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=110,y=70,width=150,height=40)
        btn_add_cart=Button(Add_CartWidgetsFrame,text="Add | Update Cart",command=self.add_update_cart,font=("times new roman",15,"bold"),bg="orange",cursor="hand2").place(x=270,y=70,width=160,height=40)

###########billing area#################
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billFrame.place(x=1005,y=110,width=455,height=590)

        BTitle=Label(billFrame,text="Customer Bill Area",font=("Times new roman",20,"bold"),bg="red",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #############billing functions############
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billMenuFrame.place(x=1010,y=520,width=445,height=175)

        self.lbl_amnt=Label(billMenuFrame,text='Bill Amount\n[0]',font=("Times new roman",15,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amnt.place(x=2,width=147,y=5,height=80)

        self.lbl_dicount=Label(billMenuFrame,text='Discount\n[5%]',font=("Times new roman",15,"bold"),bg="#8bc34a",fg="white")
        self.lbl_dicount.place(x=150,width=147,y=5,height=80)

        self.lbl_net_pay=Label(billMenuFrame,text='Net Pay\n[0]',font=("Times new roman",15,"bold"),bg="#607d8b",fg="white")
        self.lbl_net_pay.place(x=290,width=147,y=5,height=80)

        btn_print=Button(billMenuFrame,text='Print',cursor="hand2",command=self.print_bill,font=("Times new roman",15,"bold"),bg="lightgreen",fg="white")
        btn_print.place(x=2,width=147,y=90,height=80)

        btn_clear_all=Button(billMenuFrame,text='Clear All',command=self.clear_all,cursor="hand2",font=("Times new roman",15,"bold"),bg="gray",fg="white")
        btn_clear_all.place(x=150,width=147,y=90,height=80)

        btn_generate=Button(billMenuFrame,text='Generate/Save Bill',command=self.generate_bill,cursor="hand2",font=("Times new roman",12,"bold"),bg="#009688",fg="white")
        btn_generate.place(x=290,width=147,y=90,height=80)
        ################footer#############
        footer=Label(self.root,text="WAREHOUSE MANAGEMENT SYSTEM | DEVELOPED BY KUSUMANJALI AND SNEHA PRIYA",font=("times new roman",11),bg="#4d636d",fg="white",bd=0,cursor="hand2").pack(side=BOTTOM,fill=X)
        self.show()
        #self.bill_top()
        self.update_date_time()

        #self.lbl_amnt=Label(billMenuFrame,text='Bill Amount',font=("Times new roman",15,"bold"),bg="#3f51b5",fg="white")
        #self.lbl_amnt.place(x=2,width=120,y=5,height=70)


#############all functions###############
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)
    
    def clear_cal(self):
        self.var_cal_input.set('')
    
    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("Select pid,name,price,qty,status from product where status='Active'")
            rows = cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                # Correcting SQL query string concatenation
                cur.execute("SELECT pid,name,price,qty,status FROM product WHERE name LIKE '%" + self.var_search.get() + "%' and status='Active'")
                rows = cur.fetchall()
            
                if len(rows) != 0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found.", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()
    def get_data(self, ev):
        f = self.product_Table.focus()
        content = (self.product_Table.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set('1')
        #pid,name,price,qty,status
        self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        

    def add_update_cart(self):
     if self.var_pid.get() == '':
                 messagebox.showerror('Error', 'Please Select Product from list', parent=self.root)

     elif self.var_qty.get() == '':
        messagebox.showerror('Error', 'Quantity is required', parent=self.root)
     elif int(self.var_qty.get())>int(self.var_stock.get()):
        messagebox.showerror('Error', "Invalid Quantity", parent=self.root)
     
     else:
            #price_calc=float(int(self.var_qty.get())*float(self.var_price.get()))
            price_calc=self.var_price.get()

            cart_data=[self.var_pid.get(),self.var_pname.get(),price_calc,self.var_qty.get(),self.var_stock.get()]
            #######update cart
            present='no'
            _index=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                _index+=1
            if present=='yes':
                op=messagebox.askyesno('Confirm',"Product  already present\nDo you want to update or remove from cart list",parent=self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(_index)
                    else:
                        #self.cart_list[_index][2]=price_calc
                        self.cart_list[_index][3]=self.var_qty.get()
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.bill_amnt = 0
        self.net_pay = 0
        self.discount=0

        for row in self.cart_list:
            self.bill_amnt += float(row[2]) * int(row[3])  # Accumulate the total price of all items

        self.discount = (self.bill_amnt * 5) / 100  # Calculate the discount (5% of the total bill amount)
        # Calculate net pay after applying the discount
        self.net_pay = self.bill_amnt - self.discount
        
        # Update the labels with the calculated amounts
        self.lbl_amnt.config(text=f'Bill Amount\n{self.bill_amnt:.2f}')
        self.lbl_discount.config(text=f'Discount\n{self.discount:.2f}')
        self.lbl_net_pay.config(text=f'Net Pay\n{self.net_pay:.2f}')
        self.cartTitle.config(text=f"Cart \t Total Product: {len(self.cart_list)}")

        
    def show_cart(self):
        try:
            
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        
    def get_data_cart(self, ev):
        f = self.CartTable.focus()
        content = (self.CartTable.item(f))
        row = content['values']

        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        #pid,name,price,qty,status
        self.var_qty.set(row[3])
        self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])

    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error", f"Customer Details are required", parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error", f"Please add product to the cart", parent=self.root)

        else:
            self.bill_top()
            #########Bill top#########
            self.bill_middle()
            #########Bill mid#########
            #########Bill bottom#########
            self.bill_bottom()
            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            self.save_bill_to_file()
            self.store_customer_details()
            messagebox.showinfo('Saved',"Bill has been generated and saved",parent=self.root)
            self.chk_print=1

    def store_customer_details(self):
        # Store customer details in the database
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        
        try:
            cur.execute("""
            INSERT INTO customers (name, contact, invoice, date, amount) 
            VALUES (?, ?, ?, ?, ?)
            """, (
                self.var_cname.get(),
                self.var_contact.get(),
                self.invoice,
                time.strftime("%d/%m/%Y"),
                self.net_pay
            ))
            con.commit()
            print("Customer details saved successfully.")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()
            

    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%y"))
        bill_top_temp=f'''
\t\tSmart Warehouse
\t Phone No.98725*, Bangalore-560083
{str("="*47)}
Customer Name: {self.var_cname.get()}
Ph no. :{self.var_contact.get()}
Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
Product Name\t\t\tQTY\tPrice
{str("="*47)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
 Bill Amount\t\t\t\tRs.{self.bill_amnt}
 Discount\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\tRs.{self.net_pay}
{str("="*47)}\n
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)
        
    def bill_middle(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        
        try:
            
            for row in self.cart_list:
                #pid,name,price,qty,stock
                
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='InActive'
                if int(row[3])!=int(row[4]):
                    status='Active'
                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+row[3]+"\tRs."+price)
                #########update qty in product table
                cur.execute('Update Product set qty=?,status=? where pid=?',(
                    qty,
                    status,
                    pid,
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)  
    
    def save_bill_to_file(self):
        # Save bill to text file
        fp = open(f'bill/{str(self.invoice)}.txt', 'w')
        fp.write(self.txt_bill_area.get('1.0', END))
        fp.close()
                
    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_inStock.config(text=f"In Stock ")
        self.var_stock.set('')
        
    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.clear_cart()
        self.show()
        self.show_cart()
        self.cartTitle.config(text=f"Cart \t Total Product: [0]")
        self.var_search.set('')

    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config( text=f"Welcome to WAREHOUSE Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)

    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print',"Please wait while printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')

        else:
            messagebox.showerror('Print',"Please generate bill, To print the receipt",parent=self.root)


    def logout(self):
        self.root.destroy()
        os.system("python login.py") 
if __name__ == "__main__":
    root = Tk()
    obj = BillClass(root)
    root.mainloop()
