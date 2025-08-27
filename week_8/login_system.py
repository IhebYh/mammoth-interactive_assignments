import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib

conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT)""")
conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user():
    username = entry_username.get()
    password = entry_password.get()
    if username == "" or password == "":
        messagebox.showerror("Error", "All fields required")
        return
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, hash_password(password)))
        conn.commit()
        messagebox.showinfo("Success", "User registered! Please sign in.")
        switch_to_login()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists")

def login_user():
    username = entry_username.get()
    password = entry_password.get()
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))
    result = c.fetchone()
    if result:
        switch_to_dashboard(username)
    else:
        messagebox.showerror("Error", "Invalid login")

def switch_to_signup():
    label_title.config(text="Sign Up")
    btn_action.config(text="Register", command=register_user)
    btn_switch.config(text="Go to Sign In", command=switch_to_login)

def switch_to_login():
    label_title.config(text="Sign In")
    btn_action.config(text="Login", command=login_user)
    btn_switch.config(text="Go to Sign Up", command=switch_to_signup)

def switch_to_dashboard(username):
    for widget in root.winfo_children():
        widget.destroy()
    tk.Label(root, text=f"Welcome, {username}!", font=("Arial", 16)).pack(pady=20)
    tk.Button(root, text="Logout", command=reset_app).pack()

def reset_app():
    for widget in root.winfo_children():
        widget.destroy()
    build_login_ui()

def build_login_ui():
    global entry_username, entry_password, label_title, btn_action, btn_switch

    label_title = tk.Label(root, text="Sign In", font=("Arial", 16))
    label_title.pack(pady=10)

    tk.Label(root, text="Username").pack()
    entry_username = tk.Entry(root)
    entry_username.pack()

    tk.Label(root, text="Password").pack()
    entry_password = tk.Entry(root, show="*")
    entry_password.pack()

    btn_action = tk.Button(root, text="Login", command=login_user)
    btn_action.pack(pady=5)

    btn_switch = tk.Button(root, text="Go to Sign Up", command=switch_to_signup)
    btn_switch.pack()

# --- Main ---
root = tk.Tk()
root.title("Login System")
root.geometry("300x250")

build_login_ui()

root.mainloop()
