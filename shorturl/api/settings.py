from json import load

with open('config.json', 'r') as config_file:
    config_json = load(config_file)
    
# * MongoDB connection details
MONGO_HOST =  config_json['MONGO_HOST']
MONGO_PORT = config_json['MONGO_PORT']
MONGO_DBNAME = config_json['MONGO_DBNAME']
MONGO_USERNAME = config_json['MONGO_USERNAME']
MONGO_PASSWORD = config_json['MONGO_PASSWORD']

# * The route through which we can access our API
URL_PREFIX = 'api'

# * We limit which methods can be used on our resources/items
RESOURCE_METHODS = ['GET', 'POST']
ITEM_METHODS = ['GET']

# * We need to specify this, because we will upload datetime objects
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

# * Schema, we are going to store a 8 character token for the short url,
# * and we also store the original long url, hashed
DOMAIN = {
    'storage': {
        'schema': {
            'slug': {'type': 'string', 'required': True, 'unique': True},
            'url': {'type': 'string', 'required': True, 'unique': True},
            'expireAt': {'type': 'datetime', 'required': True}
        }
    }
}

# * X_DOMAINS setting specify which domains are allowed to make CORS requests
""" X_DOMAINS = '*' """
# * disables HATEOAS and PAGINATION
# * HATEOAS refers to the links, which can be used to navigate through the api without knowing its structure
# * Disabling PAGINATION results in getting all the information in one request
HATEOAS = False
PAGINATION = False