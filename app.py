import streamlit as st
from bank_system import BankSystem

# Initialize BankSystem in session state
if 'bank' not in st.session_state:
    st.session_state.bank = BankSystem()

bank = st.session_state.bank

st.title("Bank Account Management System")

# Sidebar with all options visible
st.sidebar.title("Menu")
if st.sidebar.button("Create Account", key="sidebar_create_account"):
    st.session_state.menu = "Create Account"
if st.sidebar.button("Deposit", key="sidebar_deposit"):
    st.session_state.menu = "Deposit"
if st.sidebar.button("Withdraw", key="sidebar_withdraw"):
    st.session_state.menu = "Withdraw"
if st.sidebar.button("Check Balance", key="sidebar_check_balance"):
    st.session_state.menu = "Check Balance"
if st.sidebar.button("View Account", key="sidebar_view_account"):
    st.session_state.menu = "View Account"
if st.sidebar.button("Transaction History", key="sidebar_transaction_history"):
    st.session_state.menu = "Transaction History"

# Initialize menu state if not set
if 'menu' not in st.session_state:
    st.session_state.menu = "Create Account"

def handle_account_creation():
    st.subheader("Create New Account")
    account_id = st.text_input("Account ID", key="create_account_id").strip()
    holder_name = st.text_input("Holder Name", key="create_holder_name").strip()
    initial_balance = st.number_input("Initial Balance", min_value=0.0, value=0.0, key="create_initial_balance")
    if st.button("Create Account", key="create_account_button"):
        if account_id and holder_name:
            result = bank.create_account(account_id, holder_name, initial_balance)
            st.success(result)
        else:
            st.error("Please provide both Account ID and Holder Name.")

def handle_deposit():
    st.subheader("Deposit Money")
    account_id = st.text_input("Account ID", key="deposit_account_id").strip()
    amount = st.number_input("Amount", min_value=0.0, key="deposit_amount")
    if st.button("Deposit", key="deposit_button"):
        if account_id:
            result = bank.deposit(account_id, amount)
            st.success(result)
        else:
            st.error("Please provide an Account ID.")

def handle_withdrawal():
    st.subheader("Withdraw Money")
    account_id = st.text_input("Account ID", key="withdraw_account_id").strip()
    amount = st.number_input("Amount", min_value=0.0, key="withdraw_amount")
    if st.button("Withdraw", key="withdraw_button"):
        if account_id:
            result = bank.withdraw(account_id, amount)
            st.success(result)
        else:
            st.error("Please provide an Account ID.")

def handle_balance_check():
    st.subheader("Check Account Balance")
    account_id = st.text_input("Account ID", key="balance_account_id").strip()
    if st.button("Check Balance", key="check_balance_button"):
        if account_id:
            balance = bank.get_balance(account_id)
            st.write(f"Current Balance: ${balance:.2f}")
        else:
            st.error("Please provide an Account ID.")

def handle_account_view():
    st.subheader("View Account Details")
    account_id = st.text_input("Account ID", key="view_account_id").strip()
    if st.button("View Details", key="view_details_button"):
        if account_id:
            info = bank.get_account_info(account_id)
            st.write(info)
        else:
            st.error("Please provide an Account ID.")

def handle_transaction_history():
    st.subheader("View Transaction History")
    account_id = st.text_input("Account ID", key="history_account_id").strip()
    if st.button("View History", key="view_history_button"):
        if account_id:
            transactions = bank.get_transaction_history(account_id)
            if isinstance(transactions, list):
                for transaction in transactions:
                    st.write(f"{transaction['type']}: ${transaction['amount']:.2f} - Balance: ${transaction['balance']:.2f}")
            else:
                st.error(transactions)  # In case of an error message
        else:
            st.error("Please provide an Account ID.")

# Display content based on selected menu item
if st.session_state.menu == "Create Account":
    handle_account_creation()
elif st.session_state.menu == "Deposit":
    handle_deposit()
elif st.session_state.menu == "Withdraw":
    handle_withdrawal()
elif st.session_state.menu == "Check Balance":
    handle_balance_check()
elif st.session_state.menu == "View Account":
    handle_account_view()
elif st.session_state.menu == "Transaction History":
    handle_transaction_history()