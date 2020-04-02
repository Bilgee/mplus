from flask import Flask, jsonify, abort, request, json
from flask_restful import Resource
from flask_restful import reqparse
from log import logger
import numpy as np
import time
from wplusner import ner_words, tokens_by_page


class TopicModelAPI(Resource):
    """NFIS api implementation
    """

    def __init__(self, **kwargs):
        super(TopicModelAPI, self).__init__()
        self.topic_model = kwargs['topic_model']
        self.text = kwargs['clean_text']
        self.data=self.topic_model.predict(self.text)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'data', type=str, location='json', required=True)

    def get(self):
        return self.data

    def post(self):
        try:
            args = self.parser.parse_args()
            data = args["data"]
            if data is not None:
                print(data)
                text = tokens_by_page(data)
                self.data = self.topic_model.predict(self.text)
#                 self.data['response']['code'] = 0
#                 self.data['response']['text'] = data
            return self.data
        except:
            logger.exception('ERROR')
            return self.data
