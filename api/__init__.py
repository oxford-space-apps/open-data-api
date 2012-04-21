import json

from flask import Flask, jsonify, request, Response
from flaskext.mongoalchemy import MongoAlchemy


ENDPOINT = 'http://data.nasa.gov/api/'

app = Flask(__name__)
app.config['MONGOALCHEMY_DATABASE'] = 'nasadata'
db = MongoAlchemy(app)

# These imports must be below the db definition
from api.parsers import datanasa
from api.parsers.datanasa import Dataset

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
    count = request.args.get('count', 10) # default to 10 results
    results = [dataset.data for dataset in Dataset.query.filter_by_recentness(count)]
    return Response(json.dumps(results), mimetype='application/json')

@app.route('/get_dataset/<identifier>')
def get_dataset(identifier):
    try:
        pk = int(identifier)
        response = Dataset.query.get_by_remote_id(pk)
    except ValueError:
        response = Dataset.query.get_by_slug(identifier)
    return jsonify(response.data)

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

