from flask import Flask


app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return 'Hello World!'

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

