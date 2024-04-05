import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
import pandas as pd

def fetch_data():
    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Change password if needed
        database="face_recognizer"
    )

    # Create a cursor to execute the query
    mycursor = mydb.cursor()

    # Execute query to fetch data from the 'face_count_camera' table
    query = f"SELECT * FROM face_count_camera LIMIT 25 OFFSET {(page_number - 1) * 25}"
    mycursor.execute(query)
    rows = mycursor.fetchall()

    # Clear table before inserting new data
    table.delete(*table.get_children())

    # Insert fetched data into the table
    for row in rows:
        table.insert("", "end", values=row)

def search_data():
    keyword = search_entry.get()
    if not keyword:
        messagebox.showerror("Error", "Please enter a keyword to search.")
        return

    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Change password if needed
        database="face_recognizer"
    )

    # Create a cursor to execute the query
    mycursor = mydb.cursor()

    # Execute query to fetch data from the 'face_count_camera' table
    query = f"SELECT * FROM face_count_camera WHERE ID LIKE '%{keyword}%' OR Timestamp LIKE '%{keyword}%' OR Count LIKE '%{keyword}%' OR Image_Path LIKE '%{keyword}%' LIMIT 20"
    mycursor.execute(query)
    rows = mycursor.fetchall()

    # Clear table before inserting new data
    table.delete(*table.get_children())

    # Insert fetched data into the table
    for row in rows:
        table.insert("", "end", values=row)

def export_to_excel():
    # Ask user to select location to save the file
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx")

    if file_path:
        try:
            # Get data from table
            data = [table.item(item)["values"] for item in table.get_children()]

            # Create DataFrame from data
            df = pd.DataFrame(data, columns=["ID", "Timestamp", "Count", "Image Path"])

            # Export DataFrame to Excel
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Export Successful", "Data has been exported to Excel successfully.")
        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred: {str(e)}")

# Create Tkinter GUI
root = tk.Tk()
root.title("Data from Database")

# Set window size and position
root.geometry("1366x720+0+0")

# Không cho phép thay đổi kích thước cửa sổ
root.resizable(False, False)

# Set background color
root.configure(background="blue")

# Create a frame for the table
frame = tk.Frame(root, bg="#E6F3FF")
frame.pack(pady=20, padx=10, fill='both', expand=True)

# Create a search frame
search_frame = tk.Frame(root, bg="#E6F3FF")
search_frame.pack(fill="x", padx=10, pady=(0, 10))

# Create a search entry and button
search_entry = tk.Entry(search_frame, width=50)
search_entry.pack(side="left", padx=5, pady=5, ipady=4)

search_button = tk.Button(search_frame, text="Search", command=search_data, bg="#B3CCFF", fg="black")
search_button.pack(side="left", padx=5)

# Create a button to export data to Excel
export_button = tk.Button(search_frame, text="Export to Excel", command=export_to_excel, bg="#B3CCFF", fg="black")
export_button.pack(side="right", padx=5, pady=5)

# Create a table to display data
table = ttk.Treeview(frame, columns=("ID", "Timestamp", "Count", "Image Path"), show="headings", selectmode="browse")
# Define column headings
table.heading("ID", text="ID")
table.heading("Timestamp", text="Timestamp")
table.heading("Count", text="Count")
table.heading("Image Path", text="Image Path")

# Fetch and display data from database
page_number = 1
fetch_data()

# Style the Treeview widget
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#B3CCFF", fieldbackground="#B3CCFF", foreground="black", borderwidth=1, relief="solid", padding=(10, 5))
style.map("Treeview", background=[("selected", "#347083")])
style.map("Treeview.Heading", background="#E6F3FF")

# Pack the table
table.pack(side="left", fill="both", expand=True)

# Set column width and format
table.column("ID", width=50, anchor="center")
table.column("Timestamp", width=200, anchor="center")
table.column("Count", width=80, anchor="center")  # Giảm độ rộng của cột Count
table.column("Image Path", width=400, anchor="w")  # Giảm độ rộng của cột Image Path

# Căn chỉnh văn bản trong các cột
table.heading("ID", text="ID", anchor="center")
table.heading("Timestamp", text="Timestamp", anchor="center")
table.heading("Count", text="Count", anchor="center")
table.heading("Image Path", text="Image Path", anchor="w")

# Function to navigate to the next page
def next_page():
    global page_number
    page_number += 1
    fetch_data()

# Function to navigate to the previous page
def prev_page():
    global page_number
    if page_number > 1:
        page_number -= 1
        fetch_data()

# Create navigation buttons
prev_button = tk.Button(root, text="Previous", command=prev_page, bg="#B3CCFF", fg="black")
next_button = tk.Button(root, text="Next", command=next_page, bg="#B3CCFF", fg="black")
prev_button.pack(side="left", padx=10)
next_button.pack(side="right", padx=10)

# Run the Tkinter main loop
root.mainloop()
