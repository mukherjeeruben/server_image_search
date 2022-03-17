import tensorflow as tf
from interface.query_execution import execute_query


def create_scraped_entries(dataset):
    query_parameters = [tuple(item.values()) for item in dataset]
    query = '''INSERT INTO "DEV".table_image_master(alt_image_text, image_url) values (%s,%s)'''
    result = execute_query(query=query, query_params=query_parameters)
    return result


def get_null_vector_image_data():
    query = '''SELECT embeddings_vector, sequence_key, alt_image_text FROM "DEV".table_image_master WHERE embeddings_vector IS NULL'''
    result = execute_query(query=query)
    return result


def get_all_image_data():
    query = '''SELECT embeddings_vector, image_url FROM "DEV".table_image_master WHERE embeddings_vector IS NOT NULL '''
    result = execute_query(query=query)
    return result


def update_vectorized_data(dataset):
    if len(dataset) > 1:
        dataset = [{k: v for k, v in d.items() if k == 'embeddings_vector' or k =='sequence_key'} for d in dataset]
        query_parameters = [tuple(item.values()) for item in dataset]
        query = '''UPDATE "DEV".table_image_master SET embeddings_vector = (%s) WHERE sequence_key = (%s) '''
        result = execute_query(query=query, query_params=query_parameters)
        return result
    else:
        return 'All images vectorized'


def delete_all_data():
    query = '''DELETE FROM "DEV".table_image_master'''
    result = execute_query(query=query)
    if result > 0:
        query = '''ALTER SEQUENCE "DEV".table_image_master_sequence_key_seq RESTART WITH 1;
                UPDATE "DEV".table_image_master SET sequence_key = nextval('"DEV".table_image_master_sequence_key_seq');'''
        execute_query(query=query)
        response = str(result) + ' recored deleted'
        return response
    else:
        return 'No records to delete'