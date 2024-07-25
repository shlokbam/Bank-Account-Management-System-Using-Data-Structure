import csv
import os
import json

class BankAccount:
    def __init__(self, account_id, holder_name, initial_balance=0):
        self.account_id = account_id
        self.holder_name = holder_name
        self.balance = initial_balance
        self.transactions = []

    def add_transaction(self, transaction_type, amount):
        self.transactions.append({
            'type': transaction_type,
            'amount': amount,
            'balance': self.balance
        })

class BankSystem:
    def __init__(self):
        self.filename = 'accounts.csv'
        self.create_csv_if_not_exists()
        self.load_data()

    def create_csv_if_not_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['account_id', 'holder_name', 'balance', 'transactions'])

    def save_data(self):
        with open(self.filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['account_id', 'holder_name', 'balance', 'transactions'])
            for acc_id, acc in self.accounts.items():
                writer.writerow([
                    acc.account_id,
                    acc.holder_name,
                    acc.balance,
                    json.dumps(acc.transactions)
                ])

    def load_data(self):
        self.accounts = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    account = BankAccount(
                        row['account_id'],
                        row['holder_name'],
                        float(row['balance'])
                    )
                    account.transactions = json.loads(row['transactions'])
                    self.accounts[row['account_id']] = account

    def create_account(self, account_id, holder_name, initial_balance=0):
        if account_id in self.accounts:
            return "Account already exists!"
        self.accounts[account_id] = BankAccount(account_id, holder_name, initial_balance)
        if initial_balance > 0:
            self.accounts[account_id].add_transaction("Initial Deposit", initial_balance)
        self.save_data()
        return "Account created successfully!"

    def deposit(self, account_id, amount):
        if account_id not in self.accounts:
            return "Account does not exist!"
        self.accounts[account_id].balance += amount
        self.accounts[account_id].add_transaction("Deposit", amount)
        self.save_data()
        return "Deposit successful!"

    def withdraw(self, account_id, amount):
        if account_id not in self.accounts:
            return "Account does not exist!"
        if self.accounts[account_id].balance < amount:
            return "Insufficient funds!"
        self.accounts[account_id].balance -= amount
        self.accounts[account_id].add_transaction("Withdrawal", -amount)
        self.save_data()
        return "Withdrawal successful!"

    def get_balance(self, account_id):
        if account_id not in self.accounts:
            return "Account does not exist!"
        return self.accounts[account_id].balance

    def get_account_info(self, account_id):
        if account_id not in self.accounts:
            return "Account does not exist!"
        acc = self.accounts[account_id]
        return {
            'account_id': acc.account_id,
            'holder_name': acc.holder_name,
            'balance': acc.balance
        }

    def get_transaction_history(self, account_id):
        if account_id not in self.accounts:
            return "Account does not exist!"
        return self.accounts[account_id].transactions