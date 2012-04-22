from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
import re

from flaskext.mongoalchemy import BaseQuery
import requests

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

    def get_by_category_id(self, category_id, count):
        return self.in_(self.type.categories.id, int(category_id)).limit(count)

    def get_by_category_slug(self, slug, count):
        return self.in_(self.type.categories.slug, slug).limit(count)

    def get_by_tag_id(self, tag_id):
        return self.in_(self.type.tags.remote_id, int(tag_id))

    def get_by_slug_slug(self, slug):
        return self.in_(self.type.tags.slug, slug)


class Category(db.Document):
    id = db.IntField()
    slug = db.StringField()


class Tag(db.Document):
    """Represents a Tag"""
    # post_count: 10,
    description = db.StringField()
    remote_id = db.IntField()
    slug = db.StringField()
    title = db.StringField()


class Dataset(db.Document):
    """ Represents a dataset,
    we could split this out to hold all the actual data,
    slug, url, title, etc
    """
    remote_id = db.IntField()
    slug = db.StringField()
    date_posted = db.DateTimeField()
    categories  = db.SetField(db.DocumentField(Category))
    tags = db.SetField(db.DocumentField(Tag))
    data = JSONField()

    query_class = DatasetQuery


def get_dataset(id):
    response = requests.get(ENDPOINT + 'get_dataset?id=%s' % id)
    data = json.loads(response.text)
    post = data.get('post')
    slug = post.get('slug')
    date = datetime.strptime(post.get('date'), '%Y-%m-%d %H:%M:%S')

    tags = set()
    for tag in post.get('tags'):
        new = Tag(description=tag['description'], remote_id=tag['id'],
                  slug=tag['slug'], title=tag['title'])
        new.save()
        tags.add(new)

    categories = post.get('categories')
    category_objects = set()
    for category in categories:
        cat = Category(id=category['id'], slug=category['slug'])
        cat.save()
        category_objects.add(cat)

    dataset = Dataset(remote_id = id, slug=slug, date_posted=date, data=response.text, categories=category_objects, tags=tags)
    dataset.save()

