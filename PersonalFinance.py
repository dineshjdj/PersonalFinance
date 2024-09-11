import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.markdown("""
    <style>
        Set background color 
        body {
            background-color: white;
        }
        Style headings 
        h1, h2, h3 {
            color: #1E90FF;  /* Dodger Blue */
        }
        Style other text 
        .stMarkdown p, .stMarkdown span {
            color: black;
        }
        Add custom logo 
        .logo-img {
            width: 150px;
        }
    </style>
""", unsafe_allow_html=True)

def time_remaining(event_date):
    today = datetime.now()
    remaining = event_date - today
    return remaining.days

if 'events' not in st.session_state:
    st.session_state['events'] = []
if 'salary' not in st.session_state:
    st.session_state['salary'] = 0
if 'expenses' not in st.session_state:
    st.session_state['expenses'] = []

st.title("Personal Finance Event Handler")

if st.session_state['salary'] == 0:
    st.subheader("Enter Your Monthly Salary")
    salary = st.number_input("Salary", min_value=0, step=100)
    if st.button("Submit Salary"):
        st.session_state['salary'] = salary
        st.success("Salary submitted!")
else:
    st.write(f"Your monthly salary is: ${st.session_state['salary']}")

st.sidebar.title("Manage Your Finances")

event_type = st.sidebar.selectbox("Add Financial Event", ['Bill Payment', 'Investment', 'Savings Goal', 'Expense Tracking'])

st.sidebar.markdown("## Add Event Details")

event_name = "" 

if event_type == 'Bill Payment':
 
    bill_option = st.sidebar.selectbox("Select Bill", ['Current Bill', 'Water Bill', 'Internet Bill'])
    event_name = bill_option 

    amount_due = st.sidebar.number_input("Amount Due", min_value=0.0, step=0.01)

    event_date = st.sidebar.date_input("Event Date", min_value=datetime.now().date())
    event_date = datetime.combine(event_date, datetime.min.time())  

    recurring = st.sidebar.checkbox("Recurring?")
    if recurring:
        frequency = st.sidebar.selectbox("Recurring Frequency", ['Weekly', 'Monthly', 'Yearly'])
    else:
        frequency = None

elif event_type == 'Investment':
 
    investment_option = st.sidebar.selectbox("Select Investment", ['Stocks', 'Mutual Funds', 'Fixed Deposit'])
    event_name = investment_option  

    amount = st.sidebar.number_input("Investment Amount", min_value=0.0, step=0.01)

    event_date = st.sidebar.date_input("Event Date", min_value=datetime.now().date())
    event_date = datetime.combine(event_date, datetime.min.time())  

elif event_type == 'Savings Goal':
    event_name = st.sidebar.text_input("Savings Goal Name")
    target_amount = st.sidebar.number_input("Target Amount", min_value=0.0, step=0.01)
    current_savings = st.sidebar.number_input("Current Savings", min_value=0.0, step=0.01)

    event_date = None

elif event_type == 'Expense Tracking':
    expense_category = st.sidebar.selectbox("Expense Category", ['Food', 'Transport', 'Entertainment', 'Miscellaneous'])
    expense_amount = st.sidebar.number_input("Expense Amount", min_value=0.0, step=0.01)
    st.session_state['expenses'].append({'Category': expense_category, 'Amount': expense_amount})
    st.sidebar.success(f"Expense of ${expense_amount} added to {expense_category} category.")

    event_date = None

if st.sidebar.button("Add Event"):
    event = {
        "Event Name": event_name,
        "Event Type": event_type,
        "Event Date": event_date, 
        "Amount Due": amount_due if event_type == 'Bill Payment' else 0.0,
        "Investment Amount": amount if event_type == 'Investment' else 0.0,
        "Target Amount": target_amount if event_type == 'Savings Goal' else 0.0,
        "Current Savings": current_savings if event_type == 'Savings Goal' else 0.0,
        "Recurring": recurring if event_type == 'Bill Payment' else False,
        "Frequency": frequency if event_type == 'Bill Payment' else None
    }
    st.session_state['events'].append(event)
    st.sidebar.success(f"{event_type} event added!")

st.subheader("Your Financial Events")

if len(st.session_state['events']) > 0:
    event_df = pd.DataFrame(st.session_state['events'])

    event_df['Days Remaining'] = event_df['Event Date'].apply(lambda x: time_remaining(x) if pd.notnull(x) else None)

    st.dataframe(event_df[['Event Name', 'Event Type', 'Event Date', 'Days Remaining', 'Amount Due', 'Investment Amount']])

else:
    st.write("No events added yet. Use the sidebar to add your first event.")

st.subheader("Expense Tracking")
if len(st.session_state['expenses']) > 0:
    expense_df = pd.DataFrame(st.session_state['expenses'])
    st.table(expense_df)
    total_expense = expense_df['Amount'].sum()
    st.write(f"Total Expenses: ${total_expense}")

    total_bills = event_df['Amount Due'].sum() if 'Amount Due' in event_df else 0.0
    total_investments = event_df['Investment Amount'].sum() if 'Investment Amount' in event_df else 0.0
    
    total_spent = total_expense + total_bills + total_investments
    remaining_salary = st.session_state['salary'] - total_spent

    st.write(f"Total Bills: ${total_bills}")
    st.write(f"Total Investments: ${total_investments}")
    st.write(f"Remaining Salary: ${remaining_salary}")

    if total_spent > st.session_state['salary']:
        st.warning("Your total expenses, bills, and investments exceed your salary!")
    else:
        st.success(f"You have ${remaining_salary} remaining from your salary.")
else:
    st.write("No expenses recorded yet.")
