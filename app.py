import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page

page = st.sidebar.selectbox("Explore Or Predict", ("Predict", "Explore")) #Page en sidebar

if page == "Predict":
    show_predict_page()
else:
    show_predict_page()
