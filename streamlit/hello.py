import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to weather & traffic dashboards 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Hello, Welcome to weather & traffic dashboard
    weather dashboard provides daily analysis for the weather of a city
    traffic dashboard provides analysis for route based on weather
"""
)
