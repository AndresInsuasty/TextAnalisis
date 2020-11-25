from nltk.metrics import TrigramAssocMeasures
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import BigramCollocationFinder
import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
plt.style.use('seaborn')

nltk.download('punkt')


def read_text(text):
    text = text.rstrip()
    article = text.split(". ")
    # text=text.rstrip() # Eliminate \n
    # sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    # article = sentence_tokenizer.tokenize(text) #Token by sentence
    sentences = []

    pattern = r'''(?x)                 # set flag to allow verbose regexps
              (?:[A-Z]\.)+         # abbreviations, e.g. U.S.A.
              | \w+(?:-\w+)*       # words with optional internal hyphens
              | \$?\d+(?:\.\d+)?%? # currency and percentages, e.g. $12.40, 82%
              | \.\.\.             # ellipsis
              | [][.,;"'?():-_`]   # these are separate tokens; includes ], ['''

    for sentence in article:
        sentences.append(nltk.regexp_tokenize(sentence, pattern))
        # sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
       # sentences.pop()

    return sentences


def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []

    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]

    all_words = list(set(sent1 + sent2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1

    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1

    return 1 - cosine_distance(vector1, vector2)


def build_similarity_matrix(sentences, stop_words):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:  # ignore if both are same sentences
                continue
            similarity_matrix[idx1][idx2] = sentence_similarity(
                sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix


def generate_summary(file_name, top_n=5):
    nltk.download("stopwords")
    stop_words = stopwords.words('english')
    summarize_text = []

    # Step 1 - Read text anc split it
    sentences = read_text(file_name)

    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(
        ((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    # print("Indexes of top ranked_sentence order are ", ranked_sentence)

    # print("="*200)
    # print(len(ranked_sentence))

    for i in range(top_n):
        summarize_text.append(" ".join(ranked_sentence[i][1]))

    # Step 5 - Offcourse, output the summarize texr
    return "".join(summarize_text)


def freq(text,n):
    pattern = r'''(?x)                 # set flag to allow verbose regexps
              (?:[A-Z]\.)+         # abbreviations, e.g. U.S.A.
              | \w+(?:-\w+)*       # words with optional internal hyphens
              | \$?\d+(?:\.\d+)?%? # currency and percentages, e.g. $12.40, 82%
              | \.\.\.             # ellipsis
              | [][.,;"'?():-_`]   # these are separate tokens; includes ], ['''
    token_text = nltk.regexp_tokenize(text, pattern)
    clean_tokens = token_text[:]
    for token in token_text:
            if token in stopwords.words('english') or token=='.' or token==',' or token=="'":
                clean_tokens.remove(token)
    fdist = nltk.FreqDist(clean_tokens)
    most_common = fdist.most_common(n)
    label=[]
    value=[]
    for element in most_common:
        label.append(element[0])
        value.append(element[1])
    return label, value

def bigrams(text,n):
    pattern = r'''(?x)                 # set flag to allow verbose regexps
              (?:[A-Z]\.)+         # abbreviations, e.g. U.S.A.
              | \w+(?:-\w+)*       # words with optional internal hyphens
              | \$?\d+(?:\.\d+)?%? # currency and percentages, e.g. $12.40, 82%
              | \.\.\.             # ellipsis
              | [][.,;"'?():-_`]   # these are separate tokens; includes ], ['''
    token_text = nltk.regexp_tokenize(text, pattern)
    clean_tokens = token_text[:]
    md_bigrams = list(nltk.bigrams(clean_tokens))
    threshold = 2
    filtered_bigrams = [bigram for bigram in md_bigrams if len(bigram[0])>threshold and len(bigram[1])>threshold]
    fdist = nltk.FreqDist(filtered_bigrams)
    most_common = fdist.most_common(n) 
    label=[]
    value=[]
    for element in most_common:
        label.append(element[0])
        value.append(element[1])
    return label, value

def generate_title(text):
    pattern = r'''(?x)                 # set flag to allow verbose regexps
              (?:[A-Z]\.)+         # abbreviations, e.g. U.S.A.
              | \w+(?:-\w+)*       # words with optional internal hyphens
              | \$?\d+(?:\.\d+)?%? # currency and percentages, e.g. $12.40, 82%
              | \.\.\.             # ellipsis
              | [][.,;"'?():-_`]   # these are separate tokens; includes ], ['''
    token_text = nltk.regexp_tokenize(text, pattern)
    biagram_collocation = BigramCollocationFinder.from_words(token_text) 
    biagram_collocation.nbest(BigramAssocMeasures.likelihood_ratio, 15)
    stopset = set(stopwords.words('english')) 
    filter_stops = lambda w: len(w) < 3 or w in stopset 
    biagram_collocation.apply_word_filter(filter_stops) 
    collocation_bigram = biagram_collocation.nbest(BigramAssocMeasures.likelihood_ratio, 15) 
    return collocation_bigram[0],collocation_bigram[1:]

def word_cloud(text):
    return WordCloud().generate(text)

