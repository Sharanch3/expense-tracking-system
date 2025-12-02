import streamlit as st
import requests
import pandas as pd


API_URL = "http://localhost:8000"


def analytics_months_tab():
    response = requests.get(f"{API_URL}/monthly_analytics/")
    monthly_summary = response.json()

    
    df = pd.DataFrame(monthly_summary)
    df.rename(columns={
        "Month": "Month Number",
        "Month_name": "Month Name",
        "Total": "Total"
    }, inplace=True)
    df_sorted = df.sort_values(by="Month Number", ascending=False)
    df_sorted.set_index("Month Number", inplace=True)

    
    st.title("Expense Breakdown By Months")
    st.bar_chart(data= df, x="Month Name", y="Total", color="#18B39E")
        
    st.table(df_sorted.sort_index())
    
    

