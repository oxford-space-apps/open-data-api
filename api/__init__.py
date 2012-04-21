import json
import requests

from flask import Flask, jsonify
from flaskext.mongoalchemy import MongoAlchemy


ENDPOINT = 'http://data.nasa.gov/api/'

app = Flask(__name__)
app.config['MONGOALCHEMY_DATABASE'] = 'nasadata'
db = MongoAlchemy(app)

# These imports must be below the db definition
from api.parsers import datanasa

# FIXME: Need to call an 'update' function which loops and gets each dataset
datanasa.get_dataset(619)

@app.route('/', methods=['GET'])
def index():
    datasets = datanasa.Dataset.query.all()
    response = []
    for dataset in datasets:
        print "x"
        response.append(dataset.data)
    return jsonify(response)


@app.route('/get_recent_datasets')
def get_recent_datasets():
    pass

@app.route('/get_dataset')
def get_dataset():
    pass

@app.route('/get_date_datasets')
def get_date_datasets():
    pass

@app.route('/get_category_datasets')
def get_category_datasets():
    pass

@app.route('/get_tag_datasets')
def get_tag_datasets():
    pass

@app.route('/get_search_results')
def get_search_results():
    pass

@app.route('/get_date_index')
def get_date_index():
    pass

@app.route('/get_category_index')
def get_category_index():
    pass

@app.route('/get_tag_index')
def get_tag_index():
    pass

if __name__ == '__main__':
    app.debug = True
    app.port = 8000
    app.run()

