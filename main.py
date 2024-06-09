import os
import tkinter as tk
from tkinter import messagebox
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_login(username, password):
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as file:
            for line in file:
                stored_username, stored_password = line.strip().split(',')
                if stored_username == username and stored_password == hash_password(password):
                    return True
    return False

def save_user(username, password):
    with open("users.txt", "a") as file:
        file.write(f"{username},{hash_password(password)}\n")
    # Initialize balance for new user
    with open(f"balance_{username}.txt", "w") as file:
        file.write("0.0")

def get_user_balance_filename(username):
    return f"balance_{username}.txt"

def save_balance(username, balance):
    with open(get_user_balance_filename(username), "w") as file:
        file.write(str(balance))

def load_balance(username):
    filename = get_user_balance_filename(username)
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return float(file.read())
    else:
        return 0.0

def show_balance(balance_label, balance):
    balance_label.config(text=f"Your balance is {balance:.2f} CHF")

def deposit(username, balance_label):
    global balance
    amount = amount_entry.get()
    try:
        amount = float(amount)
        if amount < 0:
            messagebox.showerror("Invalid Amount", "That's not a valid amount")
        else:
            balance += amount
            save_balance(username, balance)
            show_balance(balance_label, balance)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number")
    amount_entry.delete(0, tk.END)

def withdraw(username, balance_label):
    global balance
    amount = amount_entry.get()
    try:
        amount = float(amount)
        if amount > balance:
            messagebox.showerror("Insufficient Funds", "Insufficient funds")
        elif amount < 0:
            messagebox.showerror("Invalid Amount", "Amount must be greater than 0")
        else:
            balance -= amount
            save_balance(username, balance)
            show_balance(balance_label, balance)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number")
    amount_entry.delete(0, tk.END)

def main_screen(username):
    global balance
    balance = load_balance(username)
    
    root = tk.Tk()
    root.title("Banking Program")

    balance_label = tk.Label(root, text=f"Your balance is {balance:.2f} CHF")
    balance_label.pack(pady=10)

    global amount_entry
    amount_entry = tk.Entry(root)
    amount_entry.pack(pady=5)

    deposit_button = tk.Button(root, text="Deposit", command=lambda: deposit(username, balance_label))
    deposit_button.pack(pady=5)

    withdraw_button = tk.Button(root, text="Withdraw", command=lambda: withdraw(username, balance_label))
    withdraw_button.pack(pady=5)

    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(pady=5)

    show_balance(balance_label, balance)

    root.mainloop()

def login_screen():
    def login():
        username = username_entry.get()
        password = password_entry.get()
        if validate_login(username, password):
            login_window.destroy()
            main_screen(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def signup():
        username = username_entry.get()
        password = password_entry.get()
        save_user(username, password)
        messagebox.showinfo("Signup Success", "User registered successfully!")

    login_window = tk.Tk()
    login_window.title("Login")

    tk.Label(login_window, text="Username").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    tk.Button(login_window, text="Login", command=login).pack(pady=5)
    tk.Button(login_window, text="Sign Up", command=signup).pack(pady=5)

    login_window.mainloop()

if __name__ == '__main__':
    login_screen()
