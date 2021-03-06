import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import random
import numpy as np


# Code Mauro
def request_w2v(x=None, limit=10):
    r = requests.get('https://srf-word2vec-hackday.herokuapp.com/idsearch?article_id='+str(x)+'&limit='+str(limit)+'&date=20200901',auth=HTTPBasicAuth('srghack-2021', 'srghack-2021-pw'))
    df= pd.DataFrame(r.json()["result"])
    df['id']=x
    return df

def get_recommendations_depr(data, ids, ratings):

    new_csv = data.copy()

    ids = ids[:10]
    ratings = ratings[:10]

    # load the selected articles in from the choice-screen
    df_input = pd.DataFrame({'id': ids, 'rating': ratings})

    df_result = pd.DataFrame()

    for x in df_input[df_input['rating']==1]['id'].tolist():
        df_result = df_result.append(request_w2v(x, 10))


    df_result['article_id'] = df_result['article_id'].astype(int)
    df_result = df_result[~(df_result['article_id'].isin(df_input[df_input['rating']==1]['id'].tolist()))].drop_duplicates(subset=['article_id'], keep='first')
    df_result = pd.merge(df_result,new_csv[['cg10','visits_fake_score','date_score', 'sort_score']], how='left',left_on='article_id', right_on='cg10')
    df_result = pd.merge(df_result,new_csv[['cg10','headline']], how='left',left_on='id', right_on='cg10')
    df_sim_payload=df_result[['article_id','sort_score','headline_y']].rename(columns={'article_id':'id','sort_score':'certainty','headline_y':'reason'}).sort_values(by='certainty', ascending=False).head(10)

    explain_string_similarity='Based on the topics of your rated articles, recency and popularity we present you with the following articles.'
    certainty = float(df_sim_payload['certainty'].mean())*10
    dicto_sim=df_sim_payload.reset_index(drop=True).to_dict(orient='records')

    payload_similarity={'name': 'Topics Reccommender',
    'reason':explain_string_similarity,
    'certainty':certainty,
    'articles':dicto_sim}

    return payload_similarity


def get_example_recommendations(articles):
    df_art_info_total = articles
    ids = df_art_info_total['cg10'].sample(50).values
    ratings = np.random.randint(2, size=50)
    return get_recommendations(articles, ids, ratings)


def get_recommendations(articles, ids, ratings):
    # load all cleaned Articles
    df_art_info_total = articles

    # load the selected articles in from the choice-screen
    df_input = pd.DataFrame({'id': ids, 'rating': ratings})

    # compute 10 best matches from authors (based also on visits and recency)
    author_result = df_art_info_total[df_art_info_total['author'].isin(df_art_info_total[df_art_info_total['cg10'].isin(df_input[df_input['rating']==1].id.to_list())]['author'].tolist())].sort_values(by='sort_score',ascending=False).head(10)
    explain_string_author = 'Based on your preferred Authors, popularity and recency we present you with the following articles.'

    # create a results-dictionary
    dicto = author_result[['cg10', 'sort_score', 'author']].reset_index(drop=True).rename(columns={'cg10': 'id', 'sort_score': 'certainty', 'author': 'reason'})

    dicto['reason'] = ['{}% match with one of your favourited articles.'.format(int(random.uniform(0, 100))) for x in range(0, len(dicto))]

    dicto = dicto.to_dict(orient='records')
    payload_author={'name': 'Topics Reccommender',
    'reason': 'Based on the topics of your rated articles, recency and popularity we present you with the following articles.',
    'certainty':0.5,
    'articles':dicto}

    return payload_author

