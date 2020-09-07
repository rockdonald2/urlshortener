from flask import Flask
from flask_caching import Cache
from json import load

with open('shorturl/config.json', 'r') as config_file:
    config_json = load(config_file)

    SECRET_KEY = config_json['SECRET_KEY']
    API_URL = config_json['API_URL']
    WEBSITE_DOMAIN = config_json['WEBSITE_DOMAIN']

# * Starting Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
cache = Cache(app)

from shorturl import routes