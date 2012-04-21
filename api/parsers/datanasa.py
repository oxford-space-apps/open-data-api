import json
from flaskext.mongoalchemy import MongoAlchemy
import requests

from api import app
from api import db


ENDPOINT = 'http://data.nasa.gov/api/'

class Dataset(db.Document):
    """ Represents a dataset,
    we could split this out to hold all the actual data,
    slug, url, title, etc
    """
    remote_id = db.IntField()
    data = db.StringField()

def get_dataset(id):
    response = requests.get(ENDPOINT + 'get_dataset?id=%s' % id)
    dataset_data = json.loads(response.text)
    dataset = Dataset(remote_id = id, data=response.text)
    dataset.save()
