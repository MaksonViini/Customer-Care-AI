import spacy

nlp = spacy.load("pt_core_news_sm")


def remove_stopwords(text):
    doc = nlp(text)
    filtered_words = [token.text for token in doc if not token.is_stop]
    return " ".join(filtered_words)
