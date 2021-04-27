from textblob import TextBlob
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from collections import Counter

# df = pd.read_csv('./tweet.csv')

def sentiment(text):
    result = TextBlob(text)
    if result.polarity > 0.0:
        return 'positve'
    elif  result.polarity == 0.0:
        return 'neutral'
    else:
        return 'negative'

def analyzeSentiment(df):
    df['sentiment'] = df['tweet'].apply(sentiment)
    # fig = plt.figure(figsize=(8,5))
    dictt = Counter(df['sentiment'])
    # Counter(df['language'])
    # 

    # df.to_csv('./tweet.csv')
    
    # print(**Counter(df['language']))
    # print(dictt)
    # print(df.columns)
    # print(df['place'].head(100))
    # plt.pie(dictt.values(),labels=dictt.keys())
    # plt.show()
    return df
# analyzeSentiment(df)


def topic(df):
    cv = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    LDA = LatentDirichletAllocation(n_components=5, random_state=42)
    dtm = cv.fit_transform(df['tweet'])
    LDA.fit(dtm)
    res = {index: {'title': None, 'data': None} for index in range(5)}

    for index, topic in enumerate(LDA.components_):
        res[index]['title'] = f'THE TOP 100 WORDS FOR TOPIC #{index + 1}'
        res[index]['data'] = [cv.get_feature_names()[i]
                              for i in topic.argsort()[-100:]]
    topic_results = LDA.transform(dtm)
    df['topic'] = topic_results.argmax(axis=1)
    return df

def cluster(df):
    # df = pd.read_csv('./tweet.csv')
    vectorizer = TfidfVectorizer(analyzer='word', 
                              token_pattern=r'\b[a-zA-Z]{3,}\b',
                              ngram_range=(1, 1) 
                              )  
    data = vectorizer.fit_transform(df['tweet']).toarray()
  
    pca = PCA(n_components=2)
    p = pca.fit_transform(data)
    df['pcax'] = list(map(lambda x:x[0],p))
    df['pcay'] = list(map(lambda x:x[1],p))
    kmeans = KMeans(n_clusters=5).fit(data)
    df['kmeans'] = list(kmeans.labels_)
    # df.to_csv('./tweet.csv')
    return df

    # print('-----\n\n\n', kmeans.labels_,p)  






def test(df):
    keys = list(set(df['language']))
    positive, negative, neutral = {} , {} ,{}
    for key in keys:
        positive[key]=0
        negative[key]=0
        neutral[key]=0
    for l, s in zip(df['language'], df['sentiment']):
        if s == 'positve':
            positive[l] += 1
        elif s == 'negative':
            negative[l] +=1
        else:
            neutral[l]+=1
    res = {}
    res['keys'] = keys
    res['positive'] = list(positive.values())
    res['negative'] = list(negative.values())
    res['neutral'] = list(neutral.values())
    print(res )
    

    print(positive, negative , neutral, sep='\n----\n')


# test(df)

