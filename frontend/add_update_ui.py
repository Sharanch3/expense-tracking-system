import streamlit as st
import requests
from datetime import date


API_URL = "http://127.0.0.1:8000"

OPTIONS = ["Rent", "Food", "Shopping", "Entertainment", "Other"]


def add_update_tab():

    selected_date = st.date_input(label= "Date", value= date(2024,1,1), label_visibility= "collapsed")

    response = requests.get(f"{API_URL}/expenses/{selected_date}")

    if response.status_code == 200:
        existing_expenses = response.json()

    else:
        st.info("No expenses for the current date")
        existing_expenses = []


    #FORM
    with st.form("expense"):

        col1, col2, col3 = st.columns(3)

        col1.text("Amount")
        col2.text("Category")
        col3.text("Note")
        
        expenses = []
        
        for i in range(5):

            exp = existing_expenses[i] if i < len(existing_expenses) else {'amount': 0.0, 'category':"Shopping", 'notes':''}
            
            amount_input = col1.number_input(label="Amount", min_value=0.0, step=1.0, value= exp['amount'], label_visibility="collapsed", key=f"amt_{selected_date}_{i}")

            category_input = col2.selectbox(label="Category", options= OPTIONS, index= OPTIONS.index(exp['category']), key=f"cat_{selected_date}_{i}", label_visibility="collapsed")
                
            notes_input = col3.text_input(label="Notes", max_chars= 30, value=exp['notes'], key=f"note_{selected_date}_{i}", label_visibility="collapsed")
        
            expenses.append({'amount': amount_input, 'category': category_input, 'notes': notes_input})


        

        if st.form_submit_button():

            filetered_expenses = [e for e in expenses if e['amount'] > 0]
            response = requests.post(f"{API_URL}/expenses/{selected_date}", json= filetered_expenses)
            
            if response.status_code == 200:
                st.success("Expenses updated successfully!")
            
            else:
                st.error("Failed to update expenses.")