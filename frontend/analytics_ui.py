import streamlit as st
from datetime import date
import requests
import pandas as pd


API_URL = "http://127.0.0.1:8000"



def analytics_tab():

    col1, col2 = st.columns(2)
    
    start_date = col1.date_input(label= "Start Date", value= date(2024, 8, 1 ))

    end_date = col2.date_input(label="End Date", value= date(2024, 8, 12))


    if st.button("Get Analytics"):

        res = requests.post(f"{API_URL}/analytics/", json= {
        "start_date": "2024-08-01",
        "end_date": "2024-08-12"
        })

        response = res.json()

        data = {
            "Category": [item["category"] for item in response],
            "Total": [item["Total"] for item in response],
            "Percentage": [item["Percentage"] for item in response] 
        }


        df = pd.DataFrame(data)
    

        df_sorted = df.sort_values(by="Total", ascending=False)

        
        st.bar_chart(data= df, x="Category", y="Percentage", color="#18B39E")
        
        st.table(df_sorted)
        

        


    
