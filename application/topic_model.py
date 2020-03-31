import json
from log import logger


class TopicModel:
    def __init__(self, model):
        """init class object

        Arguments:
            model_path {string} -- [a path to read a trained model]
            features {list} -- [list of features as a string]
        """
        self.model = model

    def predict(self):
        return 'response'
