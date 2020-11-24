import streamlit as st


def input_text():
    text = st.sidebar.text_area('Ingrese texto aqui:', height=1)
    return text


def split_text(text):
    p = text.split('\n\n')
    l = len(p)
    threshold = 400
    new_text = []
    i = 0
    while i < l:
        lp = len(p[i])
        if lp > threshold:
            new_text.append(p[i])
        elif (len(p[i]+p[i+1]) > threshold) and (i < l-1):
            new_text.append(p[i] + ' ' + p[i+1])
            i = i+2
        else:
            new_text.append(i)
        i += 1
    return new_text
