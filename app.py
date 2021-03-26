from flask import Flask
from flask import request
from flask import jsonify
import json
import pandas as pd
import authorRecommender
import rubricRecommender

app = Flask(__name__)
articles = pd.read_csv('data/articles.csv', error_bad_lines=False, converters={'art': eval, 'meta': eval})


def get_rubric(x):
    try:
        return x['rubrics'][0]['name']
    except:
        return 'None'


articles['rub'] = articles['art'].apply(get_rubric)


@app.route('/')
def hello_world():
    return 'This is the index page... nothing going on...'


@app.route('/initial', methods=['GET'])
def get_initial():

    # Get some rancom recommendations from author recommender
    author_recommendations = authorRecommender.get_example_recommendations(articles)

    # Store recommendations in a list with a name indicating the recommender as initial recommendations
    recommendations = []
    recommendations.append(
        {'name': 'initial', 'recommendations': author_recommendations['articles'], 'reason': author_recommendations['reason'], 'certainty': author_recommendations['certainty']})

    return jsonify(results=recommendations)


@app.route('/recommend', methods=['GET', 'POST'])
def get_recommendations_from_json():

    # Get data from request params
    content = request.get_json(force=True)
    ids = []
    ratings = []

    for rating in content['ratings']:
        ids.append(int(rating['id']))
        ratings.append(int(rating['rating']))

    # Store all recommendations in a list
    recommendations = []
    author_recommendations = authorRecommender.get_recommendations(articles, ids, ratings)
    recommendations.append({'name': author_recommendations['name'], 'recommendations': author_recommendations['articles'],
                            'reason': author_recommendations['reason'], 'certainty': author_recommendations['certainty']})

    rubric_recommendations = rubricRecommender.get_recommendations(articles, ids, ratings)
    recommendations.append(
        {'name': rubric_recommendations['name'], 'recommendations': rubric_recommendations['articles'],
         'reason': rubric_recommendations['reason'], 'certainty': rubric_recommendations['certainty']})

    return jsonify(results=recommendations)


@app.route('/recommendwojson', methods=['GET'])
def get_recommendations():

    recommendations = []
    ids = [int(id) for id in request.args.get('ids').split(',')]
    ratings = [int(rating) for rating in request.args.get('ratings').split(',')]

    author_recommendations = authorRecommender.get_recommendations(articles, ids, ratings)

    recommendations.append({'name': author_recommendations['name'], 'recommendations': author_recommendations['articles'], 'reason': author_recommendations['reason'], 'certainty': author_recommendations['certainty']})

    rubric_recommendations = rubricRecommender.get_recommendations(articles, ids, ratings)
    recommendations.append(
        {'name': rubric_recommendations['name'], 'recommendations': rubric_recommendations['articles'],
         'reason': rubric_recommendations['reason'], 'certainty': rubric_recommendations['certainty']})
    print(recommendations)
    return jsonify(results=recommendations)


if __name__ == '__main__':
    app.run()