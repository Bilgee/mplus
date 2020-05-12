from flask_restful import Resource
from flask_restful import reqparse
from log import logger


class TopicModelAPI(Resource):
    """NFIS api implementation
    """

    def __init__(self, **kwargs):
        super(TopicModelAPI, self).__init__()
        self.topic_model = kwargs['topic_model']
        self.ner_model = kwargs['ner_model']
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
                tokens, ner, page_numbers = self.ner_model.get_tokens_and_ner(data)
                self.data['response']['text'] = self.topic_model.predict(tokens, ner, page_numbers)
        except Exception as e:
            logger.exception('ERROR', exc_info=e)
        finally:
            return self.data