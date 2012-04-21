import requests

from flask import Flask

ENDPOINT = 'http://data.nasa.gov/api/'

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():

    response = requests.get(ENDPOINT + 'get_dataset?id=354')
    print(response.text)

if __name__ == '__main__':
    app.debug = True
    app.port = 8000
    app.run()
