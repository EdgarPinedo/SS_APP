import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords

stopwords = stopwords.words('spanish')

def cleanString(text):
    text = "".join([char for char in text if char not in string.punctuation])
    text = text.lower()
    text = " ".join([word for word in text.split() if word not in stopwords])
    return text

def cosineSimVectors(vec1, vec2):
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)

    return cosine_similarity(vec1, vec2)[0][0]

def buscar(strings): 
    cleaned = list(map(cleanString, strings))
    print(cleaned)
    vectorizer = CountVectorizer().fit_transform(cleaned)
    vectors =  vectorizer.toarray()
    csim = cosineSimVectors(vectors[0], vectors[1])
    return csim