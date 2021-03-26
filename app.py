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


@app.route('/recommend', methods=['GET'])
def get_recommendations_from_json():

    content = request.json
    ids = []
    ratings = []

    for rating in content['ratings']:
        ids.push(int(rating['id']))
        ratings.push(int(rating['rating']))

    recommendations = []

    author_recommendations = authorRecommender.get_recommendations(articles, ids, ratings)
    recommendations.append({'name': author_recommendations['name'], 'recommendations': author_recommendations['articles'], 'reason': author_recommendations['reason'], 'certainty': author_recommendations['certainty']})

    return jsonify(results=recommendations)


@app.route('/recommendwojson', methods=['GET'])
def get_recommendations():

    recommendations = []
    ids = [int(id) for id in request.args.get('ids').split(',')]
    ratings = [int(rating) for rating in request.args.get('ratings').split(',')]

    author_recommendations = authorRecommender.get_recommendations(articles, ids, ratings)

    recommendations.append({'name': author_recommendations['name'], 'recommendations': author_recommendations['articles'], 'reason': author_recommendations['reason'], 'certainty': author_recommendations['certainty']})

    return jsonify(results=recommendations)


if __name__ == '__main__':
    app.run()