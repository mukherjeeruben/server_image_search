from flask_restx import Resource
from models.scraper_model import api, scrape_selection_fields, search_fields
from bl.scraper import scraper
from bl.cnn_classifier import predict_image
from bl.bert_vectorizer import sentence_text_vectorizer, get_similarity, set_cache
import config
from dal.scraped_db_data import create_scraped_entries, delete_all_data


@api.route('/scrape_data')
class DataScraper(Resource):
    @api.expect(scrape_selection_fields)
    def post(self):
        ''' Scrape data from google images'''
        payload = api.payload
        dataset = scraper(selection_criterias=payload['SearchKeyList'])
        if config.CNNFILTER:
            dataset = predict_image(dataset)
        success = create_scraped_entries(dataset)
        if success > 0:
            response = 'Scraped for ' + str(','.join(payload['SearchKeyList']))
            return response
        else:
            return 'Failed to scrape'


@api.route('/vectorize_data')
class DataVectorizer(Resource):
    def get(self):
        ''' Vectorize Scraped data'''
        response = sentence_text_vectorizer()
        set_cache()
        return response


@api.route('/similarity')
class SimilarityScore(Resource):
    @api.expect(search_fields)
    def post(self):
        ''' get smilarity scores with respect to query'''
        payload = api.payload
        matchs = get_similarity(search_query=payload['SearchKey'])
        return matchs


@api.route('/deletealldata')
class Deletealldata(Resource):
    def get(self):
        ''' delete all data'''
        return delete_all_data()

