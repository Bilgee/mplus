#!/usr/bin/python
# coding: utf-8
"""
    Importing predictor class & logger function along with flask server packages
"""
import os
from flask import Flask
from flask_restful import Api
from application.topic_model import TopicModel
from application.topic_model_api import TopicModelAPI
from application.ad_magazine_api import AdAPI
from application.ad_magazine_predict import AdMatch
from wplusner import Ner

abspath = os.path.dirname(os.path.abspath(__file__))
print(abspath)

# Flask app exporter
app = Flask(__name__)
api = Api(app)
topic_model = TopicModel()
ad_mag = AdMatch()
ner_model = Ner()

api.add_resource(TopicModelAPI, '/v1.0/topicmodel/en',
                 resource_class_kwargs={'topic_model': topic_model, 'ner_model': ner_model})

api.add_resource(AdAPI, '/v1.0/ad/en',
                 resource_class_kwargs={'ad_mag_predict': ad_mag})
