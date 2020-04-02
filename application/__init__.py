#!/usr/bin/python
# coding: utf-8
"""
    Importing predictor class & logger function along with flask server packages
"""
import os
from flask import Flask, request, json
from flask_restful import Api, Resource
from application.topic_model import TopicModel
from application.topic_model_api import TopicModelAPI


abspath = os.path.dirname(os.path.abspath(__file__))
print(abspath)

# Flask app exporter
app = Flask(__name__)
api = Api(app)
topic_model_en = TopicModel('LDA_Model')

api.add_resource(TopicModelAPI, '/v1.0/topicmodel/en',
                 resource_class_kwargs={'topic_model': topic_model_en , 'clean_text': clean_text})
