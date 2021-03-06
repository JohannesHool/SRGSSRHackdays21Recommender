import pandas as pd
import numpy as np
import json

def get_recommendations(articles, ids, ratings):
    idss = []
    for i in range(0, len(ratings)):
        if ratings[i] == 1:
            idss.append(ids[i])

    ids = idss
    arts = articles.copy()

    arts = arts[arts['cg10'].isin(ids)]['rub'].values
    rubs = {}
    for rub in arts:
        if rub not in rubs:
            rubs[rub] = 1
        else:
            rubs[rub] = rubs[rub] + 1

    rubs = sorted(rubs.items(), key=lambda x: x[1], reverse=True)

    df_lim = articles[~articles['cg10'].isin(ids)]

    recs = []
    certainty = 0
    for rub in rubs:
        num = int(rub[1] / len(ids) * 10)
        df_tmp = df_lim[df_lim['rub'] == rub[0]].sort_values('cp32', ascending=False)
        for i in range(0, num):
            certainty = certainty + num/10
            recs.append({"id": int(df_tmp.iloc[i]['cg10']), "certainty": float(num / 10),
                         "reason": "{}% of your preferred articles belong to category {}".format(num * 10, rub[0])})

    payload={'name': 'Categories Recommender',
        'reason': 'Based on your favourite categories and recency we present you with the following articles.',
        'certainty': certainty/10,
        'articles':recs}

    return payload