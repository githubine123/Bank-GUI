import os
import tkinter as tk
from tkinter import messagebox

def show_balance(balance_label, balance):
    balance_label.config(text=f"Your balance is {balance:.2f} CHF")

def deposit(balance, balance_label):
    amount = amount_entry.get()
    try:
        amount = float(amount)
        if amount < 0:
            messagebox.showerror("Invalid Amount", "That's not a valid amount")
        else:
            balance += amount
            save_balance(balance)
            show_balance(balance_label, balance)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number")
    amount_entry.delete(0, tk.END)

def withdraw(balance, balance_label):
    amount = amount_entry.get()
    try:
        amount = float(amount)
        if amount > balance:
            messagebox.showerror("Insufficient Funds", "Insufficient funds")
        elif amount < 0:
            messagebox.showerror("Invalid Amount", "Amount must be greater than 0")
        else:
            balance -= amount
            save_balance(balance)
            show_balance(balance_label, balance)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number")
    amount_entry.delete(0, tk.END)

def save_balance(balance):
    with open("balance.txt", "w") as file:
        file.write(str(balance))

def load_balance():
    if os.path.exists("balance.txt"):
        with open("balance.txt", "r") as file:
            return float(file.read())
    else:
        return 0.0

def main():
    balance = load_balance()
    
    # Create main window
    root = tk.Tk()
    root.title("Banking Program")

    # Create and place widgets
    balance_label = tk.Label(root, text=f"Your balance is {balance:.2f} CHF")
    balance_label.pack(pady=10)

    global amount_entry
    amount_entry = tk.Entry(root)
    amount_entry.pack(pady=5)

    deposit_button = tk.Button(root, text="Deposit", command=lambda: deposit(balance, balance_label))
    deposit_button.pack(pady=5)

    withdraw_button = tk.Button(root, text="Withdraw", command=lambda: withdraw(balance, balance_label))
    withdraw_button.pack(pady=5)

    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(pady=5)

    # Show initial balance
    show_balance(balance_label, balance)

    # Start the GUI event loop
    root.mainloop()

if __name__ == '__main__':
    main()

# Save this into a python file
