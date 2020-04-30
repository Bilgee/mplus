from flask_restful import Resource
from flask_restful import reqparse
from log import logger


class AdAPI(Resource):
    def __init__(self, **kwargs):
        super(AdAPI, self).__init__()
        self.ad_mag = kwargs['ad_mag_predict']
        self.data = {
            u"response": {
                u"code": 1,
                u"text": {"message": "error occured"}
            }
        }
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'data', type=dict, location='json', required=True)

    def get(self):
        return "Send json with POST request to get it analyzed"

    def post(self):
        try:
            args = self.parser.parse_args()
            data = args["data"]
            if data is not None:
                self.data['response']['code'] = 0
                self.data['response']['text'] = self.ad_mag.predict(data)
            return self.data
        except:
            logger.exception('ERROR')
            return self.data
