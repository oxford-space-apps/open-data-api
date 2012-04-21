import requests
import json 

from flask import Flask, jsonify
from flaskext.mongoalchemy import MongoAlchemy

ENDPOINT = 'http://data.nasa.gov/api/'

app = Flask(__name__)
app.config['MONGOALCHEMY_DATABASE'] = 'nasadata'
db = MongoAlchemy(app)

class Dataset(db.Document):
    """ Represents a dataset,
    we could split this out to hold all the actual data,
    slug, url, title, etc
    """
    remote_id = db.IntField()
    data = db.StringField()

@app.route('/', methods=['GET'])
def index():
    datasets = Dataset.query.all()
    response = []
    for dataset in datasets:
        print "x"
        response.append(dataset.data)
    return jsonify(response)

def get_dataset(id):
    response = requests.get(ENDPOINT + 'get_dataset?id=%s' % id)
    dataset_data = json.loads(response.text)
    dataset = Dataset(remote_id = dataset_data.id, data=response.text)
    dataset.save()
    

if __name__ == '__main__':
    app.debug = True
    app.port = 8000
    app.run()
