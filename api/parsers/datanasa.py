import json
from flaskext.mongoalchemy import BaseQuery
import requests

from api import app
from api import db


ENDPOINT = 'http://data.nasa.gov/api/'


class DatasetQuery(BaseQuery):
    def get_by_remote_id(self, pk):
        return self.filter(self.type.remote_id==pk).first()

    def get_by_slug(self, slug):
        return self.filter(self.type.slug==slug).first()


class Dataset(db.Document):
    """ Represents a dataset,
    we could split this out to hold all the actual data,
    slug, url, title, etc
    """
    remote_id = db.IntField()
    slug = db.StringField()
    data = db.StringField()

    query_class = DatasetQuery


def get_dataset(id):
    response = requests.get(ENDPOINT + 'get_dataset?id=%s' % id)
    slug = json.loads(response.text).get('post').get('slug')
    dataset = Dataset(remote_id = id, slug=slug, data=response.text)
    dataset.save()

