import sqlite3
import tkinter as tk
from tkinter import messagebox
import hashlib

# Set the admin username directly in the code
admin_username = 'GBS2024'

# Create and initialize the database
def init_db():
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS balances (
            username TEXT PRIMARY KEY,
            balance REAL NOT NULL,
            FOREIGN KEY (username) REFERENCES users (username)
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_login(username, password):
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    result = c.fetchone()
    conn.close()
    return result is not None

def save_user(username, password):
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
    c.execute("INSERT INTO balances (username, balance) VALUES (?, ?)", (username, 0.0))
    conn.commit()
    conn.close()

def save_balance(username, balance):
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute("UPDATE balances SET balance = ? WHERE username = ?", (balance, username))
    conn.commit()
    conn.close()

def load_balance(username):
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM balances WHERE username = ?", (username,))
    balance = c.fetchone()[0]
    conn.close()
    return balance

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

    # Only show the View Data button if the user is the admin
    if username == admin_username:
        view_data_button = tk.Button(root, text="View Data", command=view_data_screen)
        view_data_button.pack(pady=5)

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

def view_data_screen():
    view_window = tk.Tk()
    view_window.title("View Database")

    users_label = tk.Label(view_window, text="Users Table:")
    users_label.pack(pady=5)

    users_text = tk.Text(view_window, height=10, width=50)
    users_text.pack(pady=5)

    balances_label = tk.Label(view_window, text="Balances Table:")
    balances_label.pack(pady=5)

    balances_text = tk.Text(view_window, height=10, width=50)
    balances_text.pack(pady=5)

    conn = sqlite3.connect('bank.db')
    c = conn.cursor()

    users_text.insert(tk.END, "Username\tPassword\n")
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    for user in users:
        users_text.insert(tk.END, f"{user[0]}\t{user[1]}\n")

    balances_text.insert(tk.END, "Username\tBalance\n")
    c.execute("SELECT * FROM balances")
    balances = c.fetchall()
    for balance in balances:
        balances_text.insert(tk.END, f"{balance[0]}\t{balance[1]:.2f}\n")

    conn.close()

    view_window.mainloop()

if __name__ == '__main__':
    init_db()
    login_screen()
