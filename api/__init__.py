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
from api.parsers import grin
from api.parsers import kepler

# FIXME: Need to call an 'update' function which loops and gets each dataset
datanasa.get_dataset(619)

def hacky_jsonify_list(data_list):
    return Response(json.dumps(data_list), mimetype='application/json')

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
    return hacky_jsonify_list(results)

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
    date = request.args.get('date') # required
    if not date:
        return Exception

    count = request.args.get('count', 10) # default to 10
    query = Dataset.query.filter_by_date(date).limit(count)
    results = [dataset.data for dataset in query]
    return hacky_jsonify_list(results)

@app.route('/get_category_datasets/')
def get_category_datasets():
    count = int(request.args.get('count', 10)) # default to 10 results

    pk = request.args.get('id')
    slugs = request.args.getlist('slug')
    if not (pk or slugs):
        return Exception
    if pk:
        results = Dataset.query.get_by_category_id(pk, count)
    else:
        slug = slugs[0]
        results = Dataset.query.get_by_category_slug(slug, count)

    response = [dataset.data for dataset in results]
    return hacky_jsonify_list(response)

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

@app.route('/grin/add')
def get_grin_data():
    grin.get_pages()
    return 'Grin data added to database.' 

@app.route('/kepler/add')
def get_kepler_data():
    kepler.get_candidates();
    return 'Kepler complete.'
