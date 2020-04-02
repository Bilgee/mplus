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
from wplusner import ner_words, tokens_by_page

abspath = os.path.dirname(os.path.abspath(__file__))
print(abspath)

# Flask app exporter
app = Flask(__name__)
api = Api(app)
topic_model_en = TopicModel('application/LDA_Model')
orolt =[{
        "path": "0002/index.html",
        "image": "0002/0/1a.jpg",
        "page_number": 2,
        "title": "Editor's Letter",
        "h1": ["Chapter One"],
        "h2": [],
        "h3": [],
        "h4": [],
        "h5": [],
        "span": [],
        "bold": ["Da Vinci Tower,", "Jakarta Pusat", "Eddy Sofyan /", "Theodore Alexander dari", "Da Vinci Indonesia /", "Joe Russell Harbour"],
        "italic": ["Facade Mafia", "rising architects", "avantgarde,", "social media darling", "Living", "Inside", "CASA Indonesia", "ballroom", "New Beginning,", "Let the journey begin.", "More about us:"],
        "text": ["Editor's LEttEr", "It’s a new-beginning. Awal baru.", "Inilah wajah baru media CASA Indonesia versi cetak edisi pertama di tahun 2020. selama setahun, CASA Indonesia akan terbit sebanyak empat kali, terbagi menjadi Vol. I hingga IV setiap tiga bulan sekali.", ""]
    }, {
        "path": "0003/index.html",
        "image": "0003/0/2.jpg",
        "page_number": 3,
        "title": "MASTHEAD",
        "h1": [],
        "h2": [],
        "h3": [],
        "h4": ["PT MEDIA DINAMIKA SELARAS", "CASA INDONESIAMRA MEDIA", "HOTLINE"],
        "h5": [],
        "span": ["Assistant Managing Editor", "Reporter", "Artistic", "(Group Art)", "(Art Coord.)", "MRA Media", "Photography Department", "(Asst. Coord.)", "Audiovisual Department", "(Coord.)", "Contributors", "Head Of Business Growth", "Advertising Sales", "Marketing Communications", "Public Relations & Business Communications", "Subscription", "Finance & GeneralAdministrationFinance", "Personnel", "General Affairs", "Circulation & Distribution", "Commissioner", "President Director", "Director", "Subscription", "Advertising", "Printer"],
        "bold": [],
        "italic": [],
        "text": ["MASTHEAD", "Managing EditorPrastia H. B. Putra", "", "President CommissionerSoetikno Soedarjo", ""]
    }, {
        "path": "0009/index.html",
        "image": "0009/0/1.jpg",
        "page_number": 9,
        "title": "Dekade Baru",
        "h1": ["DekadeBaru"],
        "h2": [],
        "h3": [],
        "h4": [],
        "h5": [],
        "span": [],
        "bold": [],
        "italic": ["New Beginning.", "ballroom", "tenants", "home and living.", "talkshow,", "See you on Casa Indonesia 2020!"],
        "text": ["UPCOMING", "Teks oleh Desy RufaidaFoto: Dok. CASA Indonesia", "T ahun berganti tahun, beragam pameran desain turut hadir meramaikan ajang ekspresi seni di Indonesia. Telah melewati satu dekade, di tahun ke-11 ini Casa Indonesia 2020 kembali menjadi sebuah ekshibisi yang mencuri perhatian berbagai kalangan, tidak hanya untuk para kreator desain tetapi juga para penikmat desain.", ""]
    }]
clean_text=tokens_by_page(orolt)
ner=ner_words(orolt)
api.add_resource(TopicModelAPI, '/v1.0/topicmodel/en',
                 resource_class_kwargs={'topic_model': topic_model_en,'clean_text': clean_text,'ner': ner})
