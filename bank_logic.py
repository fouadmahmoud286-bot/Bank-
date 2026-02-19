import random

class BankAccount:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.account_number = random.randint(1000, 9999)  # رقم حساب عشوائي

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True
        else:
            print("Not enough balance!")
            return False

    def show_balance(self):
        print(f"{self.name} | Account: {self.account_number} | Balance: {self.balance}")


# --- مثال للتجربة ---
# a1 = BankAccount("Ahmed", 100)
# a2 = BankAccount("Sara", 200)

# a1.show_balance()
# a1.deposit(50)
# a1.withdraw(30)
# a1.show_balance()

# a2.show_balance()
# a2.withdraw(250)  # هيديك رسالة "Not enough balance"
