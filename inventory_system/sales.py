from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os

class salesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("SMART WAREHOUSE MANAGEMENT | DEVELOPED BY KUSUMANJALI AND SNEHA PRIYA")
        self.root.config(bg="white")
        self.root.focus_force()
        self.bill_list=[]

        # Load and set the background image
        self.bg3_image = Image.open(r"images/bg3.jpeg")  # Replace with your image path
        self.bg3_image = self.bg3_image.resize((1350, 700), Image.Resampling.LANCZOS)  # Resize to match window size
        self.bg3_photo = ImageTk.PhotoImage(self.bg3_image)
        bg_label = Label(self.root, image=self.bg3_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.var_invoice=StringVar()
        #title
        lb1_title = Label(self.root, text="View Customer Bill", font=("goudy old style", 30), bg="black",
                          fg="white", bd=3, relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)
        lb1_invoice=Label(self.root,text="Invoice No.",font=("times new roman",15),bg="white").place(x=50,y=100)

        txt_invoice=Entry(self.root,textvariable=self.var_invoice,font=("times new roman",15),bg="lightyellow").place(x=160,y=100,width=180,height=28)

        btn_search=Button(self.root,text="Search",font=("times new roman",15,"bold"),bg="#2196f3",fg="white",cursor="hand2", command=self.search).place(x=360,y=100,width=120,height=28)
        btn_clear=Button(self.root,text="Clear",font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2", command=self.clear).place(x=490,y=100,width=120,height=28)
        #bill list
        sales_Frame=Frame(self.root,bd=3,relief=RIDGE)
        sales_Frame.place(x=50,y=140,width=200,height=330)

        scrolly=Scrollbar(sales_Frame,orient=VERTICAL)

        self.Sales_List=Listbox(sales_Frame,font=("goudy old style",15),bg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH,expand=1)
        self.Sales_List.bind("<ButtonRelease-1>",self.get_data)

        #bill area
        bill_Frame=Frame(self.root,bd=3,relief=RIDGE)
        bill_Frame.place(x=280,y=140,width=410,height=330)

        lb2_title = Label(bill_Frame, text="Customer Bill Area", font=("goudy old style", 20), bg="orange",
                          fg="white", bd=3, relief=RIDGE).pack(side=TOP,fill=X)
        #lb1_invoice=Label(self.root,text="Invoice No.",font=("times new roman",15),bg="white").place(x=50,y=100)


        scrolly2=Scrollbar(bill_Frame,orient=VERTICAL)
        self.bill_area=Text(bill_Frame,bg="lightyellow",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)

        #image
        self.bill_photo = Image.open("images/category.jpeg")
        self.bill_photo = self.bill_photo.resize((390, 330))  # Provide size as a tuple
        self.bill_photo = ImageTk.PhotoImage(self.bill_photo)

        # Create a Label to display the image
        self.image_label = Label(self.root, image=self.bill_photo,bd=0)
        self.image_label.place(x=700, y=140)

        self.show()
####################################################
    def show(self):
        self.Sales_List.delete(0,END)
        #print(os.listdir('bill'))
        for i in os.listdir('bill'):
            if (i.split('.')[-1])=='txt':
                self.Sales_List.insert(END,i)
                self.bill_list.append(i.split('.')[0])

    
    def get_data(self, ev):
        del self.bill_list[:]
        row = self.Sales_List.curselection()
        if row:  # Check if any item is selected
            index_ = row[0]
            file_name = self.Sales_List.get(index_)
            #print(file_name)
            self.bill_area.delete('1.0',END)
            with open(f'bill/{file_name}', 'r') as fp:
                data = fp.read()
                self.bill_area.delete(1.0, END)  # Clear existing data in the Text widget
                self.bill_area.insert(END, data)
                for i in os.listdir('bill'):
                    self.bill_list.append(i.split('.')[1])

    def search(self):
        if self.var_invoice.get() == "":
            messagebox.showerror("Error", "Invoice no. is required", parent=self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                file_name = f"{self.var_invoice.get()}.txt"  # Properly format file name
                with open(f'bill/{file_name}', 'r') as fp:
                    data = fp.read()
                    self.bill_area.delete('1.0', END)  # Clear existing data in the Text widget
                    self.bill_area.insert(END, data)
            else:
                messagebox.showerror("Error", "Invoice no. is invalid", parent=self.root)


    def clear(self):
        # Add functionality to clear the invoice number and any displayed data
        self.show()
        self.bill_area.delete('1.0',END)





if __name__ == "__main__":
    root = Tk()
    obj = salesClass(root)
    root.mainloop()
