from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from dal.scraped_db_data import get_null_vector_image_data, update_vectorized_data
import numpy as np
from dal.scraped_db_data import get_all_image_data
dataset = None
bert_model = None


def sentence_text_vectorizer():
    dataset = get_null_vector_image_data()
    for item in dataset:
        item['embeddings_vector'] = bert_model.encode(item['alt_image_text']).tolist()
    success = update_vectorized_data(dataset)
    return success


def get_similarity(search_query):
    matches = list()
    for x in dataset:
        x['embeddings_vector'] = np.array(x['embeddings_vector'])
    search_embeddings = bert_model.encode(search_query.lower())
    for image_set in dataset:
        similarity_score = cosine_similarity([image_set['embeddings_vector']], [search_embeddings])
        if similarity_score[0][0] > 0.5:
            matches.append({'url': image_set['image_url'], 'score': similarity_score[0][0]})
    matches = sorted(matches, key=lambda item: item['score'], reverse=True)
    return matches


def set_cache():
    global dataset
    global bert_model
    dataset = get_all_image_data()
    bert_model = SentenceTransformer('all-mpnet-base-v2')
    return None