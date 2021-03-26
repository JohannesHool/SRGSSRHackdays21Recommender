import pandas as pd
import numpy as np
import json


def get_example_recommendations(articles):
    df_art_info_total = articles
    ids = df_art_info_total['cg10'].sample(10).values
    ratings = np.random.randint(2, size=10)
    return get_recommendations(articles, ids, ratings)


def get_recommendations(articles, ids, ratings):
    # load all cleaned Articles
    df_art_info_total = articles

    # load the selected articles in from the choice-screen
    df_input = pd.DataFrame({'id': ids, 'rating': ratings})

    # compute 10 best matches from authors (based also on visits and recency)
    author_result = df_art_info_total[df_art_info_total['author'].isin(df_art_info_total[df_art_info_total['cg10'].isin(df_input[df_input['rating']==1].id.to_list())]['author'].tolist())].sort_values(by='sort_score',ascending=False).head(10)
    # describe what the output contains
    explain_string_author = 'Aufgrund Ihrer Angaben, Popularität und Aktualität werden Ihnen die Artikel von [Platzhalter siehe Reason unten] angezeigt.'

    # create a results-dictionary
    dicto = author_result[['cg10', 'sort_score', 'author']].reset_index(drop=True).rename(columns={'cg10': 'id', 'sort_score': 'certainty', 'author': 'reason'}).to_dict(orient='records')

    payload_author={'name': 'author_recom',
    'reason':explain_string_author,
    'certainty':1,
    'articles':dicto}

    return payload_author