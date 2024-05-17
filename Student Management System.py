import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Global variables for Tkinter widgets and SQLite
nameEntry = None
highschoolEntry = None
phoneEntry = None
addressEntry = None
gradeLevelDropdown = None
strandDropdown = None
root = None
connection = None
TABLE_NAME = "management_table"
STUDENT_ID = "student_id"
STUDENT_NAME = "student_name"
STUDENT_HIGHSCHOOL = "student_highschool"
STUDENT_ADDRESS = "student_address"
STUDENT_PHONE = "student_phone"
STUDENT_GRADE_LEVEL = "student_grade_level"
STUDENT_STRAND = "student_strand"

def create_main_window():
    global nameEntry, highschoolEntry, phoneEntry, addressEntry, gradeLevelDropdown, strandDropdown, root, connection

    root = tk.Tk()
    root.title("Management")

    # Label widgets for input fields
    appLabel = tk.Label(root, text="RTPM - DSHS SHS Enrollment System", fg="#c08081", width=40)
    appLabel.config(font=("Bebas Neue ", 35))
    appLabel.grid(row=0, columnspan=2, padx=(15, 15), pady=(30, 0))

    nameLabel = tk.Label(root, text="Enter your Name", width=40, anchor='w', font=("Barlow", 12))
    nameLabel.grid(row=1, column=0, padx=(10, 0), pady=(30, 0))
    highschoolLabel = tk.Label(root, text="Enter your Previous School", width=40, anchor='w', font=("Barlow", 12))
    highschoolLabel.grid(row=2, column=0, padx=(10, 0))
    phoneLabel = tk.Label(root, text="Enter your Phone Number", width=40, anchor='w', font=("Barlow", 12))
    phoneLabel.grid(row=3, column=0, padx=(10, 0))
    addressLabel = tk.Label(root, text="Enter your Address", width=40, anchor='w', font=("Barlow", 12))
    addressLabel.grid(row=4, column=0, padx=(10, 0))
    gradeLevelLabel = tk.Label(root, text="Select Grade Level", width=40, anchor='w', font=("Barlow", 12))
    gradeLevelLabel.grid(row=5, column=0, padx=(10, 0))
    strandLabel = tk.Label(root, text="Select Strand", width=40, anchor='w', font=("Barlow", 12))
    strandLabel.grid(row=6, column=0, padx=(10, 0))

    # Entry widgets for user input
    nameEntry = tk.Entry(root, width=30)
    highschoolEntry = tk.Entry(root, width=30)
    phoneEntry = tk.Entry(root, width=30)
    addressEntry = tk.Entry(root, width=30)

    nameEntry.grid(row=1, column=1, padx=(0, 10), pady=(30, 20))
    highschoolEntry.grid(row=2, column=1, padx=(0, 10), pady=20)
    phoneEntry.grid(row=3, column=1, padx=(0, 10), pady=20)
    addressEntry.grid(row=4, column=1, padx=(0, 10), pady=20)

    # Dropdowns for grade level and strand selection
    gradeLevelValues = ["11", "12"]
    gradeLevelDropdown = ttk.Combobox(root, values=gradeLevelValues, width=27)
    gradeLevelDropdown.grid(row=5, column=1, padx=(0, 10), pady=20)

    strandValues = ["ABM", "STEM"]
    strandDropdown = ttk.Combobox(root, values=strandValues, width=27)
    strandDropdown.grid(row=6, column=1, padx=(0, 10), pady=20)

    # Buttons for actions
    button = tk.Button(root, text="Take Input", command=takeNameInput)
    button.grid(row=7, column=0, pady=30)

    displayButton = tk.Button(root, text="Display Result", command=destroyRootWindow)
    displayButton.grid(row=7, column=1)

    root.mainloop()

def takeNameInput():
    global nameEntry, highschoolEntry, phoneEntry, addressEntry, gradeLevelDropdown, strandDropdown, connection

    username = nameEntry.get()
    highschoolName = highschoolEntry.get()
    phone = phoneEntry.get()
    address = addressEntry.get()
    grade_level = gradeLevelDropdown.get()
    strand = strandDropdown.get()

    try:
        phone = int(phone)  # Convert phone to integer
    except ValueError:
        messagebox.showerror("Error", "Phone Number must be numeric.")
        return

    # Insert data into SQLite database
    try:
        connection.execute("INSERT INTO " + TABLE_NAME + " ( " + STUDENT_NAME + ", " +
                           STUDENT_HIGHSCHOOL + ", " + STUDENT_ADDRESS + ", " +
                           STUDENT_PHONE + ", " + STUDENT_GRADE_LEVEL + ", " +
                           STUDENT_STRAND + " ) VALUES ( ?, ?, ?, ?, ?, ? )",
                           (username, highschoolName, address, phone, grade_level, strand))
        connection.commit()
        messagebox.showinfo("Success", "Data Saved Successfully.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", "Error occurred: " + str(e))

    # Clear entry fields after insertion
    nameEntry.delete(0, tk.END)
    highschoolEntry.delete(0, tk.END)
    phoneEntry.delete(0, tk.END)
    addressEntry.delete(0, tk.END)

def destroyRootWindow():
    global root
    root.destroy()
    create_results_window()

def create_results_window():
    global tree, connection

    secondWindow = tk.Tk()
    secondWindow.title("Display results")

    appLabel = tk.Label(secondWindow, text="Student Management System", fg="#c08081", width=40)
    appLabel.config(font=("Bebas Neue", 30))
    appLabel.pack()

    tree = ttk.Treeview(secondWindow, selectmode='browse')
    tree["columns"] = ("one", "two", "three", "four", "five", "six")

    tree.heading("one", text="Student Name")
    tree.heading("two", text="High School Name")
    tree.heading("three", text="Address")
    tree.heading("four", text="Phone Number")
    tree.heading("five", text="Grade Level")
    tree.heading("six", text="Strand")

    try:
        cursor = connection.execute("SELECT * FROM " + TABLE_NAME)
        for row in cursor:
            tree.insert('', tk.END, text="Student " + str(row[0]), values=(row[1], row[2], row[3], row[4], row[5], row[6]))
    except sqlite3.Error as e:
        messagebox.showerror("Error", "Error occurred: " + str(e))

    tree.pack()

    deleteButton = tk.Button(secondWindow, text="Delete", command=delete_selected_student)
    deleteButton.pack(pady=20)

    backButton = tk.Button(secondWindow, text="Back", command=secondWindow.destroy)
    backButton.pack(pady=20)

    secondWindow.mainloop()

def delete_selected_student():
    global tree, connection

    try:
        selected_item = tree.selection()[0]
        student_id = tree.item(selected_item)['text'].split(" ")[1]

        connection.execute("DELETE FROM " + TABLE_NAME + " WHERE " + STUDENT_ID + " = ?", (student_id,))
        connection.commit()
        tree.delete(selected_item)
        messagebox.showinfo("Success", "Student information deleted successfully.")
    except IndexError:
        messagebox.showerror("Error", "Please select a student to delete.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", "Error occurred: " + str(e))

def main():
    global connection

    # Establish SQLite connection and create table if not exists
    try:
        connection = sqlite3.connect('management.db')
        connection.execute("CREATE TABLE IF NOT EXISTS " + TABLE_NAME + " ( " + STUDENT_ID +
                           " INTEGER PRIMARY KEY AUTOINCREMENT, " +
                           STUDENT_NAME + " TEXT, " + STUDENT_HIGHSCHOOL + " TEXT, " +
                           STUDENT_ADDRESS + " TEXT, " + STUDENT_PHONE + " INTEGER, " +
                           STUDENT_GRADE_LEVEL + " INTEGER, " +
                           STUDENT_STRAND + " TEXT);")
    except sqlite3.Error as e:
        print("SQLite error:", e)

    create_main_window()

    # Close connection after main window is closed
    if connection:
        connection.close()

if __name__ == "__main__":
    main()
