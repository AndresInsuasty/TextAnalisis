import streamlit as st


def input_text():
    text = st.sidebar.text_area('Ingrese texto aqui:',height=1) 
    return text