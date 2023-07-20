import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("pt_core_news_sm")


def remove_stopwords(text):
    doc = nlp(text)
    filtered_words = [token.text for token in doc if not token.is_stop]
    return " ".join(filtered_words)


def similarity_model(user_input):
    data = pd.read_json(
        "/home/maksonvinicio/Documents/GitLab-GitHub/Customer-Care-AI/ml_model/data/data.json"
    ).reset_index(drop=True)

    data_script = pd.read_json(
        "/home/maksonvinicio/Documents/GitLab-GitHub/Customer-Care-AI/ml_model/data/data_script.json"
    ).reset_index(drop=True)

    data["description"] = data["description"].apply(lambda x: x.lower())

    data["description"] = data["description"].apply(remove_stopwords)

    # Instantiate the TF-IDF vectorizer
    vectorizer = TfidfVectorizer(lowercase=True, strip_accents="unicode")

    # Apply TF-IDF on the text dataset
    tfidf_matrix = vectorizer.fit_transform(data["description"])

    user_input = remove_stopwords(user_input)

    # Vetorização do input do usuário
    input_vector = vectorizer.transform([user_input])

    # Cálculo da similaridade de cosseno entre o input do usuário e cada descrição
    similarity_scores = cosine_similarity(input_vector, tfidf_matrix)

    most_similar_index = similarity_scores.argmax()

    return most_similar_index
