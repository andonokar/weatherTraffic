import streamlit as st

from config.loader import config

st.title("Route Map")


if 'city_selection' not in st.session_state:
    st.session_state.city_selection = set()


inp = st.text_input("type the number of the cities you want to search for")
if inp:
    number = int(inp)

    for i in range(number):
        a = st.selectbox(f"Select city {i + 1}", config["cities"].keys(), index=None, key=f"city_{i}")
        if a:
            st.session_state.city_selection.add(a)

    if st.button("Search"):
        selected_cities = st.session_state.city_selection
        coordinates
