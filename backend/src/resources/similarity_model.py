import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from ..database import description_colletion

nlp = spacy.load("pt_core_news_sm")


# Custom exception classes for better error handling
class DataLoadingError(Exception):
    pass


class DataProcessingError(Exception):
    pass


class SimilarityModelError(Exception):
    pass


def load_data():
    try:
        result = description_colletion.find_one({})

        data = pd.DataFrame(result["descriptions"]).reset_index(drop=True)
        data["description"] = data["description"].apply(lambda x: x.lower())
        data["description"] = data["description"].apply(remove_stopwords)
        return data

    except Exception as e:
        raise DataLoadingError(f"Error loading or processing data: {e}") from e


def instantiate_vectorizer(data):
    try:
        # Instantiate the TF-IDF vectorizer and fit on the entire dataset
        vectorizer = TfidfVectorizer(lowercase=True, strip_accents="unicode")
        tfidf_matrix = vectorizer.fit_transform(data["description"])
        return vectorizer, tfidf_matrix

    except Exception as e:
        raise DataProcessingError(f"Error in vectorizer instantiation: {e}") from e


def remove_stopwords(text):
    doc = nlp(text)
    filtered_words = [token.text for token in doc if not token.is_stop]
    return " ".join(filtered_words)


def similarity_model(user_input):
    try:
        vectorizer, tfidf_matrix = instantiate_vectorizer(load_data())

        user_input = remove_stopwords(user_input)

        # Vetorização do input do usuário
        input_vector = vectorizer.transform([user_input])

        # Cálculo da similaridade de cosseno entre o input do usuário e cada descrição
        similarity_scores = cosine_similarity(input_vector, tfidf_matrix)

        most_similar_index = similarity_scores.argmax()

        return int(most_similar_index)

    except Exception as e:
        raise SimilarityModelError(f"Error in similarity model: {e}") from e
