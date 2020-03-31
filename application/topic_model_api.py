from flask import Flask, jsonify, abort, request, json
from flask_restful import Resource
from flask_restful import reqparse
from log import logger
import numpy as np
import time


class TopicModelAPI(Resource):
    """NFIS api implementation
    """

    def __init__(self, **kwargs):
        super(TopicModelAPI, self).__init__()
        self.topic_model = kwargs['topic_model']
        self.data = {
            u"response": {
                u"code": 1,
                u"text": {"message": "error occured"}
            }
        }
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'data', type=str, location='json', required=True)

    def get(self):
        return 'OK'

    def post(self):
        try:
            args = self.parser.parse_args()
            data = args["data"]
            if data is not None:
                self.data['response']['code'] = 0
                self.data['response']['text'] = data
            return self.data
        except:
            logger.exception('ERROR')
            return self.data
