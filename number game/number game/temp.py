import tkinter as tk
from tkinter import messagebox

# Predefined username and password
USERNAME = "user"
PASSWORD = "password"

# Function to check login credentials
def check_login():
    username = entry_username.get()
    password = entry_password.get()

    if username == USERNAME and password == PASSWORD:
        messagebox.showinfo("Login Success", "Welcome!")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Set up the main window
root = tk.Tk()
root.title("Login Form")

# Set window size
root.geometry("300x200")

# Create labels and entry fields for username and password
label_username = tk.Label(root, text="Username:")
label_username.pack(pady=10)

entry_username = tk.Entry(root, width=30)
entry_username.pack(pady=5)

label_password = tk.Label(root, text="Password:")
label_password.pack(pady=10)

entry_password = tk.Entry(root, width=30, show="*")
entry_password.pack(pady=5)

# Create login button
login_button = tk.Button(root, text="Login", command=check_login)
login_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()