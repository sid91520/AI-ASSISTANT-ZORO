# import sqlite3

# conn = sqlite3.connect('feedback')
# cursor = conn.cursor()
# cursor.execute('SELECT * FROM feedback ')
# rows = cursor.fetchall()
# for row in rows:
#     print(row)

# cursor.close()
# conn.close()
import tkinter as tk
from tkinter import ttk
import sqlite3

def display_feedback():
    conn = sqlite3.connect('feedback')  # Assuming the database file is named 'feedback.db'
    cursor = conn.cursor()
    cursor.execute('DELETE FROM  feedback WHERE Name =123;')
   
    cursor.execute('SELECT * FROM feedback')
    # cursor.execute('DELETE FROM  feedback WHERE Name = ;')
    
    rows = cursor.fetchall()

    # Create a new window for displaying feedback
    feedback_window = tk.Toplevel(root)
    feedback_window.title("Feedback")
    feedback_window.configure(bg="black")

    # Create a treeview widget to display rows and columns
    tree = ttk.Treeview(feedback_window, style="Custom.Treeview")
    tree["columns"] = ("Email", "Name", "Feedback")
    tree.heading("#0", text="ID")
    tree.heading("Email", text="Email")
    tree.heading("Name", text="Name")
    tree.heading("Feedback", text="Feedback")
    
    tree.column("#0", width=100)
    tree.column("Email", width=150)
    tree.column("Name", width=150)
    tree.column("Feedback", width=400)

    for i, row in enumerate(rows):
        tree.insert("", "end", text=str(i+1), values=row)
    tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    cursor.close()
    conn.close()

# Create the main window
root = tk.Tk()
root.title("Feedback Viewer")

# Button to display feedback
view_feedback_button = tk.Button(root, text="View Feedback", command=display_feedback)
view_feedback_button.pack(pady=10)

# Define custom style for the treeview
style = ttk.Style()
style.configure("Custom.Treeview", background="black", foreground="white", fieldbackground="black", bordercolor="blue")

root.mainloop()



