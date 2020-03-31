import yaml
import os

abspath = os.path.dirname(os.path.abspath(__file__))
print(abspath)

with open("config/config.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

ENV = cfg['ENV']  # PROD or DEV
LOG = cfg[ENV]['LOG']

HTTP_HOST = cfg[ENV]['HTTP_HOST']
HTTP_PORT = cfg[ENV]['HTTP_PORT']


with open(os.path.join(abspath, 'model.yml'), 'r') as conf_file:
    MODEL_CONF = yaml.safe_load(conf_file)
