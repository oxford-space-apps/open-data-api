import requests

from flask import Flask
from flaskext.mongoalchemy import MongoAlchemy

ENDPOINT = 'http://data.nasa.gov/api/'

app = Flask(__name__)
app.config['MONGOALCHEMY_DATABASE'] = 'nasadata'
db = MongoAlchemy(app)

class Dataset(db.Document):
    remote_id = db.IntField()
    data = db.StringField()

@app.route('/', methods=['GET'])
def index():

    response = requests.get(ENDPOINT + 'get_dataset?id=354')
    response_text = response.text
    dataset = Dataset(remote_id = response.text.id, data=response.text)
    dataset.save()
    
    

if __name__ == '__main__':
    app.debug = True
    app.port = 8000
    app.run()
