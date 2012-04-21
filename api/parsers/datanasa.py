from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
import re

from flaskext.mongoalchemy import BaseQuery
import requests

from api import app
from api import db


ENDPOINT = 'http://data.nasa.gov/api/'


class JSONField(db.StringField):
    def unwrap(self, value, *args, **kwargs):
        """Pass the json field around as a dictionary internally"""
        return json.loads(value)


class DatasetQuery(BaseQuery):
    def filter_by_date(self, date):
        """ Filter datasets by dates
        Acceptable formats:
            * YYYY
            * YYYY-MM
            * YYYY-MM-DD
        Non-numeric characters are stripped making these also valid:
            * YYYYMMDD
            * YYYY/MM/DD
        """
        non_numeric = re.compile(r'[^\d]+').sub('', date)
        formats = {
            'year': ('%Y', relativedelta(years=+1)),
            'month': ('%Y%m', relativedelta(months=+1)),
            'day': ('%Y%m%d', relativedelta(days=+1)),
        }
        for key, info in formats.iteritems():
            try:
                parsed_date = datetime.strptime(non_numeric, info[0])
                diff = parsed_date + formats[key][1]
                break
            except ValueError:
                continue

        return self.filter(Dataset.date_posted >= parsed_date).filter(Dataset.date_posted <= diff)

    def filter_by_recentness(self, count):
        # FIXME: limit doesn't limit here
        return self.descending(self.type.date_posted).limit(count)

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
    date_posted = db.DateTimeField()
    data = JSONField()

    query_class = DatasetQuery


def get_dataset(id):
    response = requests.get(ENDPOINT + 'get_dataset?id=%s' % id)
    data = json.loads(response.text)
    slug = data.get('post').get('slug')
    date = datetime.strptime(data.get('post').get('date'), '%Y-%m-%d %H:%M:%S')
    dataset = Dataset(remote_id = id, slug=slug, date_posted=date, data=response.text)
    dataset.save()

