import pandas as pd
import numpy as np
import json


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
    dicto['reason'] = 'Written by ' + dicto['reason']

    dicto = dicto.to_dict(orient='records')
    payload_author={'name': 'Author Recommendations',
    'reason':explain_string_author,
    'certainty':0.5,
    'articles':dicto}

    return payload_author