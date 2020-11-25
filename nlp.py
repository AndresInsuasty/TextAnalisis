# LIBRARIES
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from pptx import Presentation
from pptx.util import Pt


# LOCAL UTILS
from utils.input_text import input_text, split_text
from utils.process_text import generate_summary, freq, bigrams, generate_title, word_cloud
from utils.presentation import get_binary_file_downloader_html, make_presentation

# a little title
st.write("""
# TRASCENDER GLOBAL
""")

# sidebar with space to input text
st.sidebar.header('INPUT TEXT')
text = input_text()  # in this variable we have the raw text

# if we have at least 400 characters we forward to make the analysis and process
if len(text) > 400:

    # split the text with custom function
    text_split = split_text(text)
    st.subheader('DEMO NLP APPLICATIONS:')
    possible_title, bi = generate_title(text)
    st.subheader('Title:')
    title = possible_title[0] + ' ' + possible_title[1]
    st.write(title.upper())
    st.subheader('Possible titles:')
    for id, element in enumerate(bi):
        st.write(id, element[0]+' '+element[1])

    st.subheader('Summary:')
    summary = generate_summary(text, 1)
    st.write(summary)

    st.subheader('Most Frecuents Words')
    label, value = freq(text, 5)
    fig, ax = plt.subplots()
    x = np.arange(len(value))
    ax.bar(x, value)
    plt.xticks(x, label)
    st.pyplot(fig)

    st.subheader('Bigrams')
    label, value = bigrams(text, 5)
    fig, ax = plt.subplots()
    x = np.arange(len(value))
    ax.bar(x, value)
    plt.xticks(x, label)
    st.pyplot(fig)

    st.subheader('WordCloud')
    wordcloud = word_cloud(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud)
    plt.axis("off")
    st.pyplot(fig)

    # Create titles and summaries to slides
    title_split = []
    summary_split = []
    for element in text_split:
        # [('The','title')],bigrams = genera...
        pt, auxiliar = generate_title(element)
        s = generate_summary(element, 1)
        title_split.append(pt[0]+' '+pt[1])
        summary_split.append(s)

    # Create presentation
    make_presentation(title_split, summary_split)

    # Download presentation
    st.markdown(get_binary_file_downloader_html(
        'Output.pptx', 'Presentation'), unsafe_allow_html=True)

else:
    # warning message
    st.write('Please enter a longer text')
