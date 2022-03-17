import re as regular_expression
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def preprocess_text(text_data):
    english_stop_words = stopwords.words('english')
    lemmatizer = WordNetLemmatizer()
    text_data = regular_expression.sub('[^a-zA-Z0-9]+', ' ', text_data)
    text_data = regular_expression.findall('[a-z]{2,}', text_data.lower())
    text_data = [word for word in text_data if word not in english_stop_words]
    text_data = ' '.join(set([lemmatizer.lemmatize(word) for word in text_data]))
    return text_data