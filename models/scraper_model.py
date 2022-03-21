from flask_restx import Namespace, fields


api = Namespace('ScraperService', description='Scrape and Insert data to master database')


scrape_selection_fields = api.model('Search Key word for Scraping',
                                 {'SearchKeyList': fields.List(fields.String)})

search_fields = api.model('Search Key word',
                                 {'SearchKey': fields.String(attribute='name')})