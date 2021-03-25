from flask import Flask
from flask import request
from flask import jsonify
import pandas as pd
import authorRecommender

app = Flask(__name__)
articles = pd.read_csv('data/articles.csv')

@app.route('/')

def hello_world():
    return 'This is the index page... nothing going on...'


@app.route('/initial', methods=['GET'])
def get_initial():
    try:
        return authorRecommender.get_example_recommendations(articles)
    except Exception as e:
        return str(e)


@app.route('/author', methods=['GET'])
def get_author_recommendations():
    try:
        ids = [int(id) for id in request.args.get('ids').split(',')]
        ratings = [int(rating) for rating in request.args.get('ratings').split(',')]
        return authorRecommender.get_recommendations(articles, ids, ratings)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run()