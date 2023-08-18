import os
import random
import string
import tkinter as tk
from tkinter import messagebox


# Define the file paths for the bank data and transaction log
BANK_DATA_FILE = "Bank Data.txt"
TRANSACTION_LOG_FILE = "Transaction Log.txt"

# Check if the bank data file exists; if not, create it with an initial balance of R0
if not os.path.exists(BANK_DATA_FILE):
    with open(BANK_DATA_FILE, "w") as f:
        f.write("0")

# Check if the transaction log file exists; if not, create it
if not os.path.exists(TRANSACTION_LOG_FILE):
    with open(TRANSACTION_LOG_FILE, "w") as f:
        f.write("")


# Load the current balance from the bank data file
def load_balance():
    with open(BANK_DATA_FILE, "r") as f:
        return float(f.read())


# Update the current balance in the bank data file
def update_balance(balance):
    with open(BANK_DATA_FILE, "w") as f:
        f.write(str(balance))


# Log a transaction in the transaction log file
def log_transaction(transaction):
    with open(TRANSACTION_LOG_FILE, "a") as f:
        f.write(transaction)


# Function to handle deposits
def deposit():
    amount = deposit_entry.get()
    if not amount:
        messagebox.showerror("Invalid Amount", "Please enter a deposit amount.")
        return
    try:
        amount = float(amount)
        if amount < 10:
            messagebox.showerror("Invalid Amount", "Deposit amount must be more than R10.")
            return
    except ValueError:
        messagebox.showerror("Invalid Amount", "Deposit amount must be a valid number.")
        return

    balance = load_balance()
    balance += amount
    update_balance(balance)
    log_transaction(f"Deposit: R{amount}\n")
    messagebox.showinfo("Deposit Successful", f"Deposit of R{amount} successful.\nCurrent balance: R{balance}\nThank you for banking with EverTrust.")

    # Ask if the user wants to see the total balance
    if messagebox.askyesno("Total Balance", "Do you want to see the total balance?"):
        show_total_balance()

    # Ask if the user wants to leave or close the account
    if messagebox.askyesno("Account", "Do you want to leave or close the account?"):
        leave_or_close_account()

    reload_fields()


# Function to handle withdrawals
def withdraw():
    amount = withdraw_entry.get()
    if not amount:
        messagebox.showerror("Invalid Amount", "Please enter a withdrawal amount.")
        return
    try:
        amount = float(amount)
        if amount < 10:
            messagebox.showerror("Invalid Amount", "Withdrawal amount must be more than R10.")
            return
    except ValueError:
        messagebox.showerror("Invalid Amount", "Withdrawal amount must be a valid number.")
        return

    balance = load_balance()
    if balance >= amount:
        balance -= amount
        update_balance(balance)
        log_transaction(f"Withdrawal: R{amount}\n")
        messagebox.showinfo("Withdrawal Successful", f"Withdrawal of R{amount} successful.\nCurrent balance: R{balance}\nThank you for banking with EverTrust.")

        # Ask if the user wants to see the total balance
        if messagebox.askyesno("Total Balance", "Do you want to see the total balance?"):
            show_total_balance()

        # Ask if the user wants to leave or close the account
        if messagebox.askyesno("Account", "Do you want to leave or close the account?"):
            leave_or_close_account()

        reload_fields()
    else:
        messagebox.showerror("Insufficient Funds", f"Sorry, you do not have sufficient funds.\nCurrent balance: R{balance}")


# Function to display the total balance
def show_total_balance():
    balance = load_balance()
    messagebox.showinfo("Total Balance", f"Your current balance is: R{balance}")


# Function to display the current balance
def show_current_balance():
    balance = load_balance()
    messagebox.showinfo("Current Balance", f"Your current balance is: R{balance}")


# Function to leave or close the account
def leave_or_close_account():
    messagebox.showinfo("Account", "Thank you for banking with EverTrust. Goodbye!")
    window.destroy()


# Function to reload fields
def reload_fields():
    deposit_entry.delete(0, tk.END)
    withdraw_entry.delete(0, tk.END)

    # Clear the current balance
    balance_button.config(text="Show Current Balance")

    # Reload transaction history
    with open(TRANSACTION_LOG_FILE, "r") as f:
        transaction_history = f.read()
    transaction_text.delete(1.0, tk.END)
    transaction_text.insert(tk.END, transaction_history)

    # Enable buttons when corresponding fields are filled
    if deposit_entry.get():
        deposit_button.config(state=tk.NORMAL)
    if withdraw_entry.get():
        withdraw_button.config(state=tk.NORMAL)


# Function to clear the transaction history
def clear_transaction_history():
    with open(TRANSACTION_LOG_FILE, "w") as f:
        f.write("")
    transaction_text.delete(1.0, tk.END)


# Function to generate a random password
def generate_random_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(12))
    return password


# Function for user registration with validation
def register_user():
    def validate_date(date_text):
        try:
            day, month, year = map(int, date_text.split("-"))
            if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 9999):
                return False
        except ValueError:
            return False
        return True

    def validate_password(password_text):
        if len(password_text) < 8:
            return False
        return True

    username = username_entry.get()
    date_of_birth = dob_entry.get()
    password = password_entry.get()

    if not username:
        messagebox.showerror("Invalid Input", "Please enter a username.")
        return
    if not date_of_birth or not validate_date(date_of_birth):
        messagebox.showerror("Invalid Input", "Please enter a valid date of birth in dd-mm-yyyy format.")
        return
    if not password or not validate_password(password):
        messagebox.showerror("Invalid Input", "Password must be at least 8 characters long.")
        return

    with open("user_credentials.txt", "a") as f:
        f.write(f"{username},{date_of_birth},{password}\n")
    messagebox.showinfo("Registration Successful", "Registration successful!")


# Function for user login with validation
def login_user():
    username = username_entry.get()
    password = password_entry.get()

    if not username:
        messagebox.showerror("Invalid Input", "Please enter a username.")
        return
    if not password:
        messagebox.showerror("Invalid Input", "Please enter a password.")
        return

    with open("user_credentials.txt", "r") as f:
        for line in f:
            stored_username, stored_dob, stored_password = line.strip().split(",")
            if username == stored_username and password == stored_password:
                messagebox.showinfo("Login Successful", "Login successful!")
                cover_page_frame.pack_forget()
                bank_transaction_frame.pack()
                return
    messagebox.showerror("Login Failed", "Invalid username or password.")


# Function to open the registration form
def open_registration_form():
    register_window = tk.Toplevel(window)
    register_window.title("Registration Form")
    register_window.geometry("300x200")

    # Create labels and entry widgets for registration form
    username_label = tk.Label(register_window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(register_window)
    username_entry.pack()

    dob_label = tk.Label(register_window, text="Date of Birth (dd-mm-yyyy):")
    dob_label.pack()
    dob_entry = tk.Entry(register_window)
    dob_entry.pack()

    password_label = tk.Label(register_window, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(register_window, show="*")
    password_entry.pack()

    def register_and_close():
        username = username_entry.get()
        date_of_birth = dob_entry.get()
        password = password_entry.get()
        with open("user_credentials.txt", "a") as f:
            f.write(f"{username},{date_of_birth},{password}\n")
        register_window.destroy()
        messagebox.showinfo("Registration Successful", "Registration successful!")

    register_button = tk.Button(register_window, text="Register", command=register_and_close)
    register_button.pack()


# Function to open the login form
def open_login_form():
    login_window = tk.Toplevel(window)
    login_window.title("Login Form")
    login_window.geometry("300x150")

    # Create labels and entry widgets for login form
    username_label = tk.Label(login_window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    password_label = tk.Label(login_window, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    def login_and_close():
        username = username_entry.get()
        password = password_entry.get()
        with open("user_credentials.txt", "r") as f:
            for line in f:
                stored_username, _, stored_password = line.strip().split(",")
                if username == stored_username and password == stored_password:
                    login_window.destroy()
                    messagebox.showinfo("Login Successful", "Login successful!")
                    cover_page_frame.pack_forget()
                    bank_transaction_frame.pack()
                    return
        messagebox.showerror("Login Failed", "Invalid username or password.")

    login_button = tk.Button(login_window, text="Login", command=login_and_close)
    login_button.pack()

# Create the main window
window = tk.Tk()
window.title("EverTrust Bank")
window.geometry("400x500")  # Increased window size

# Customizing fonts and colors
font = ("Arial", 12)
bg_color = "#b4e3f1"  # Light blue color
button_color = "#b4e391"  # Light green color

window.config(bg=bg_color)

# Create a frame for the bank transaction section
bank_transaction_frame = tk.Frame(window, bg=bg_color)

# Create a frame for the deposit section
deposit_frame = tk.Frame(bank_transaction_frame, bg=bg_color)
deposit_frame.pack(pady=10)

# Create labels and entry widgets for deposit
deposit_label = tk.Label(deposit_frame, text="Deposit Amount:", font=font, bg=bg_color)
deposit_label.pack()
deposit_entry = tk.Entry(deposit_frame, font=font)
deposit_entry.pack()

# Create a deposit button
deposit_button = tk.Button(deposit_frame, text="Deposit", font=font, bg=button_color, command=deposit)
deposit_button.pack()

# Create a frame for the withdrawal section
withdraw_frame = tk.Frame(bank_transaction_frame, bg=bg_color)
withdraw_frame.pack(pady=10)

# Create labels and entry widgets for withdrawal
withdraw_label = tk.Label(withdraw_frame, text="Withdrawal Amount:", font=font, bg=bg_color)
withdraw_label.pack()
withdraw_entry = tk.Entry(withdraw_frame, font=font)
withdraw_entry.pack()

# Create a withdrawal button
withdraw_button = tk.Button(withdraw_frame, text="Withdraw", font=font, bg=button_color, command=withdraw)
withdraw_button.pack()

# Create a frame for the action buttons section
action_frame = tk.Frame(bank_transaction_frame, bg=bg_color)
action_frame.pack(pady=10)

# Create a reload button
reload_button = tk.Button(action_frame, text="Reload", font=font, bg=button_color, command=reload_fields)
reload_button.pack(side=tk.LEFT, padx=5)

# Create a button to display the current balance
balance_button = tk.Button(action_frame, text="Show Current Balance", font=font, bg=button_color, command=show_current_balance)
balance_button.pack(side=tk.LEFT, padx=5)

# Create a frame for the transaction history section
transaction_frame = tk.Frame(bank_transaction_frame, bg=bg_color)
transaction_frame.pack(pady=10)

# Create a label for the transaction history
transaction_label = tk.Label(transaction_frame, text="Transaction History:", font=font, bg=bg_color)
transaction_label.pack()

# Create a text widget for the transaction history
transaction_text = tk.Text(transaction_frame, height=8, width=30, font=font)
transaction_text.pack()

# Create a frame for the clear transaction history button
clear_button_frame = tk.Frame(bank_transaction_frame, bg=bg_color)
clear_button_frame.pack(pady=10)

# Create a clear button for the transaction history
clear_button = tk.Button(clear_button_frame, text="Clear Transaction History", font=font, bg=button_color, command=clear_transaction_history)
clear_button.pack()

# Pack the clear button frame
clear_button_frame.pack()

# Pack the bank transaction frame
# Note: We'll initially show the cover page frame and hide the bank transaction frame
bank_transaction_frame.pack_forget()

# Create a separate frame for the cover page (registration and login)
cover_page_frame = tk.Frame(window, bg=bg_color)

# Create labels and buttons for the cover page
cover_label = tk.Label(cover_page_frame, text="Welcome to EverTrust Bank", font=font, bg=bg_color)
cover_label.pack(pady=20)

register_button = tk.Button(cover_page_frame, text="Register", font=font, command=open_registration_form)
register_button.pack(pady=10)

login_button = tk.Button(cover_page_frame, text="Login", font=font, command=open_login_form)
login_button.pack(pady=10)

# Pack the cover page frame
cover_page_frame.pack()

# Run the GUI main loop
window.mainloop()
