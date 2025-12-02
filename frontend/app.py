import streamlit as st
from analytics_ui import analytics_tab
from add_update_ui import add_update_tab
from analytics_month_ui import analytics_months_tab


st.set_page_config(
    page_title="Expense Tracking System",
    page_icon="📠",
    layout="centered"
)

st.title("📠 Expense Tracking System")


tab1, tab2, tab3 = st.tabs(["add/update", "analytics", "month_analytics"])



with tab1:
    add_update_tab()

    
with tab2:

    analytics_tab()

with tab3:

    analytics_months_tab()

    