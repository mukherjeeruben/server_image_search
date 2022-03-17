from flask import Flask
from flask_restx import Api
import config
from flask_cors import CORS
from bl.bert_vectorizer import set_cache


##############Import service###############
from services.scraper_service import api as scarper_service
###########################################

flask_app = Flask(__name__)
CORS(flask_app)
API = Api(flask_app)

############Append Namespace##############
API.add_namespace(scarper_service)
###########################################


set_cache()


if __name__ == '__main__':
    flask_app.run(debug=config.DEBUG)