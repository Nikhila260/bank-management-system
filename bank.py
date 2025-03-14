import json
import hashlib
import getpass
import os

DATA_FILE = "bank_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_account():
    data = load_data()
    username = input("Enter a username: ")
    if username in data:
        print("Username already exists!")
        return
    password = input("Enter a password: ")
    hashed_password = hash_password(password)
    data[username] = {"password": hashed_password, "balance": 0, "transactions": []}
    save_data(data)
    print("Account created successfully!")

def login():
    data = load_data()
    username = input("Enter username: ")
    if username not in data:
        print("Account does not exist!")
        return None
    password = input("Enter password: ")
    if hash_password(password) != data[username]["password"]:
        print("Invalid password!")
        return None
    print("Login successful!")
    return username

def deposit(username):
    data = load_data()
    amount = float(input("Enter deposit amount: "))
    if amount <= 0:
        print("Invalid amount!")
        return
    data[username]["balance"] += amount
    data[username]["transactions"].append(f"Deposited ${amount}")
    save_data(data)
    print(f"Deposited ${amount} successfully!")

def withdraw(username):
    data = load_data()
    amount = float(input("Enter withdrawal amount: "))
    if amount <= 0 or amount > data[username]["balance"]:
        print("Invalid amount or insufficient funds!")
        return
    data[username]["balance"] -= amount
    data[username]["transactions"].append(f"Withdrew ${amount}")
    save_data(data)
    print(f"Withdrew ${amount} successfully!")

def transfer(username):
    data = load_data()
    recipient = input("Enter recipient username: ")
    if recipient not in data:
        print("Recipient does not exist!")
        return
    amount = float(input("Enter transfer amount: "))
    if amount <= 0 or amount > data[username]["balance"]:
        print("Invalid amount or insufficient funds!")
        return
    data[username]["balance"] -= amount
    data[recipient]["balance"] += amount
    data[username]["transactions"].append(f"Transferred ${amount} to {recipient}")
    data[recipient]["transactions"].append(f"Received ${amount} from {username}")
    save_data(data)
    print(f"Transferred ${amount} to {recipient} successfully!")

def check_balance(username):
    data = load_data()
    print(f"Your balance is: ${data[username]['balance']}")

def transaction_history(username):
    data = load_data()
    print("Transaction History:")
    for transaction in data[username]["transactions"]:
        print(transaction)

def main():
    while True:
        print("\n1. Create Account\n2. Login\n3. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            create_account()
        elif choice == "2":
            user = login()
            if user:
                while True:
                    print("\n1. Deposit\n2. Withdraw\n3. Transfer\n4. Check Balance\n5. Transaction History\n6. Logout")
                    action = input("Choose an option: ")
                    if action == "1":
                        deposit(user)
                    elif action == "2":
                        withdraw(user)
                    elif action == "3":
                        transfer(user)
                    elif action == "4":
                        check_balance(user)
                    elif action == "5":
                        transaction_history(user)
                    elif action == "6":
                        print("Logged out successfully!")
                        break
                    else:
                        print("Invalid choice!")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
