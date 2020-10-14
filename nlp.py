import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from utils.input_text import input_text
from utils.process_text import generate_summary, freq, bigrams, title, word_cloud
st.write("""
# TRASCENDER GLOBAL
""")


st.sidebar.header('INPUT TEXT')
text = input_text()

if len(text)>10:
    st.subheader('DEMO NLP APPLICATIONS:')

    possible_title,bi=title(text)
    st.subheader('Title:')
    title=possible_title[0]+ ' ' +possible_title[1]
    st.write(title.upper())
    st.subheader('Possible titles:')
    for id,element in enumerate(bi):
        st.write(id,element[0]+' '+element[1])

    st.subheader('Summary:')
    summary = generate_summary(text,1)
    st.write(summary)

    st.subheader('Most Frecuents Words')
    label,value=freq(text,5)
    fig, ax = plt.subplots()
    x=np.arange(len(value))
    ax.bar(x,value)
    plt.xticks(x,label)
    st.pyplot(fig)

    st.subheader('Bigrams')
    label,value=bigrams(text,5)
    fig, ax = plt.subplots()
    x=np.arange(len(value))
    ax.bar(x,value)
    plt.xticks(x,label)
    st.pyplot(fig)

    st.subheader('WordCloud')
    wordcloud = word_cloud(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud)
    plt.axis("off")
    st.pyplot(fig)


else:
    st.write('Please enter a longer text')