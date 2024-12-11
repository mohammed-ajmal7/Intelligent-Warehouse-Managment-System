import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Database connection details
db_host = 'localhost'
db_user = 'root'
db_password = 'root'
db_name = 'warehouse'

# Function to establish connection to MySQL database
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

# Function to fetch all records from the database
def fetch_records():
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tracking ORDER BY timestamp DESC")
        records = cursor.fetchall()
        conn.close()

        # Clear the current data in the treeview
        for row in tree.get_children():
            tree.delete(row)

        # Insert data into the treeview
        for record in records:
            tree.insert("", "end", values=(record[1], record[2], record[3], record[4]))

# Function to add a new record to the database
def add_record():
    uid = entry_uid.get()
    location = entry_location.get()
    entry_type = entry_type_var.get()

    if not uid or not location or not entry_type:
        messagebox.showwarning("Input Error", "Please fill all the fields.")
        return

    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tracking (uid, location, entry_type) VALUES (%s, %s, %s)", (uid, location, entry_type))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Record added successfully!")
        fetch_records()

# Function to edit an existing record
def edit_record():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a record to edit.")
        return

    # Get the selected record
    record = tree.item(selected_item, "values")
    uid = record[0]
    location = record[1]
    entry_type = record[2]

    # Show the record in the entry fields
    entry_uid.delete(0, tk.END)
    entry_uid.insert(0, uid)
    entry_location.delete(0, tk.END)
    entry_location.insert(0, location)
    entry_type_var.set(entry_type)

    # After editing, update the record
    def update_record():
        new_uid = entry_uid.get()
        new_location = entry_location.get()
        new_entry_type = entry_type_var.get()

        if not new_uid or not new_location or not new_entry_type:
            messagebox.showwarning("Input Error", "Please fill all the fields.")
            return

        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("UPDATE tracking SET uid = %s, location = %s, entry_type = %s WHERE uid = %s", 
                           (new_uid, new_location, new_entry_type, uid))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Record updated successfully!")
            fetch_records()

    # Open a new window to confirm the update
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Record")
    edit_button = tk.Button(edit_window, text="Update", command=update_record)
    edit_button.pack()

# Function to delete a selected record
def delete_record():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a record to delete.")
        return

    # Get the selected record
    record = tree.item(selected_item, "values")
    uid = record[0]

    confirm = messagebox.askyesno("Delete Record", f"Are you sure you want to delete the record for UID: {uid}?")
    if confirm:
        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tracking WHERE uid = %s", (uid,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Record deleted successfully!")
            fetch_records()

# Create the main window
root = tk.Tk()
root.title("RFID Tracking Database")

# Frame for the input fields
frame_input = tk.Frame(root)
frame_input.pack(padx=10, pady=10)

tk.Label(frame_input, text="UID:").grid(row=0, column=0)
entry_uid = tk.Entry(frame_input)
entry_uid.grid(row=0, column=1)

tk.Label(frame_input, text="Location:").grid(row=1, column=0)
entry_location = tk.Entry(frame_input)
entry_location.grid(row=1, column=1)

tk.Label(frame_input, text="Entry Type:").grid(row=2, column=0)
entry_type_var = tk.StringVar()
entry_type_menu = ttk.Combobox(frame_input, textvariable=entry_type_var, values=["Entry", "Exit"])
entry_type_menu.grid(row=2, column=1)
entry_type_menu.set("Entry")

# Buttons to add, edit, delete records
button_add = tk.Button(frame_input, text="Add Record", command=add_record)
button_add.grid(row=3, column=0, columnspan=2, pady=5)

# Treeview to display the records
tree = ttk.Treeview(root, columns=("UID", "Location", "Entry Type", "Timestamp"), show="headings")
tree.heading("UID", text="UID")
tree.heading("Location", text="Location")
tree.heading("Entry Type", text="Entry Type")
tree.heading("Timestamp", text="Timestamp")
tree.pack(padx=10, pady=10)

# Buttons to edit and delete records
button_edit = tk.Button(root, text="Edit Record", command=edit_record)
button_edit.pack(padx=10, pady=5)

button_delete = tk.Button(root, text="Delete Record", command=delete_record)
button_delete.pack(padx=10, pady=5)

# Fetch and display records when the program starts
fetch_records()

# Run the Tkinter event loop
root.mainloop()
