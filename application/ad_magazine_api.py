from flask import Flask, jsonify, abort, request, json
from flask_restful import Resource
from flask_restful import reqparse
from log import logger
from application.topic_model import TopicModel
from application.ad_magazine_predict import Ad_match
import nltk
from nltk.corpus import wordnet

class Ad_API(Resource):
    def __init__(self,**kwargs):
        super(Ad_API, self).__init__()
        self.ad_mag=kwargs['ad_mag_predict']
        self.data = {
            u"response": {
                u"code": 1,
                u"text": {"message": "error occured"}
            }
        }
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'data', type=list, location='json', required=True)

    def get(self):
        return "Send json with POST request to get it analyzed"

    def post(self):
        try:
            args = self.parser.parse_args()
            data = args["data"]
            if data is not None:
                self.data['response']['code'] = 0
                self.data['response']['text'] = self.ad_mag.predict(data[0])
            return self.data
        except:
            logger.exception('ERROR')
            return self.data