import pandas as pd
import numpy as np
import psycopg2 as pg2
from functions import connect_to_database, get_tweets, cleaning_tweets
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

def main(database,table):
    cur = connect_to_database(database)
    res = get_tweets(cur,table)

    df = pd.DataFrame(res,columns=['userid','location','tweet','time','full_tweet','retweet_count'])
    df.drop(['retweet_count'],axis=1,inplace=True)

    full_tweets = df[df['full_tweet']!= 'No full text']['full_tweet']
    vec_model = TfidfVectorizer(tokenizer=cleaning_tweets)
    vec_model.fit(full_tweets)
    vocab = np.array(vec_model.get_feature_names())
    tf_idf=vec_model.transform(full_tweets).toarray()

    nmf = NMF(n_components=7, max_iter=100, random_state=12345, alpha=0.0)
    W = nmf.fit_transform(tf_idf)
    H = nmf.components_
    print('reconstruction error:', nmf.reconstruction_err_)
    for i,tweet in enumerate(H):
        top_ten = np.argsort(tweet)[::-1][:20]
        print(vocab[top_ten])

if __name__ == "__main__":
    db = input('Please enter a database to connect to: ')
    tbl = input('Please enter a table to get tweets from: ')
    main(str(db),str(tbl))