import psycopg2 as pg2
import tweepy
import os
import re
from nltk.stem import WordNetLemmatizer
import string
from nltk.corpus import stopwords

def create_database(database):
    conn = pg2.connect(dbname='postgres', user='postgres', host='localhost', port='5435')
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute('CREATE DATABASE {};'.format(database))
    conn.close()

def connect_to_database(db_name):
    '''

    '''
    conn = pg2.connect(dbname=db_name, user='postgres', host='localhost',port='5435')
    conn.autocommit = True
    cur = conn.cursor()
    return cur

def create_table(cursor,table_name):
    '''
    Creates a table in postgresql to store tweets. Stores userid, location, tweet, time of tweet, full text of
    tweet if there is one, and number of retweets. 
    INPUTS: Name that you want to call the table.
    '''
    query = '''
    CREATE TABLE {} (
        userid VARCHAR(20),
        location VARCHAR(200),
        tweet VARCHAR(200),
        tweet_time VARCHAR(25),
        full_tweet VARCHAR(5000),
        retweets INTEGER);
    '''.format(table_name)

    cursor.execute(query)

def connect_to_tweepy():
    '''

    '''
    consumer_key = os.environ['TWITTER_KEY']
    consumer_secret = os.environ['TWITTER_SECRET']
    access_token = os.environ['TWITTER_TOKEN']
    access_token_secret = os.environ['TWITTER_SECRET_TOKEN']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api


def streamer(api,table,keywords):
    class MyStreamListener(tweepy.StreamListener):
        def on_status(self,tweet):
            user = tweet.id
            loc = tweet.user.location
            text = tweet.text
            tweet_time = tweet.created_at
            try:
                full_text = tweet.extended_tweet["full_text"]
            except:
                full_text = 'No full text'
            cursor.execute("INSERT INTO %s (userid,location,tweet,tweet_time,full_tweet) VALUES(%s,%s,%s,%s,%s);",(table,user,loc,text,tweet_time,full_text))
        def on_error(self, status_code):
            if status_code == 420:
                #returning False in on_data disconnects the stream
                return False
    myStreamListener = MyStreamListener()
    while True:
        try:
            myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener,tweet_mode='extended')
            myStream.filter(track=[keywords])
        except:
            print('Restarting Stream')
            continue

def get_tweets(cursor,table_name):
    cursor.execute('SELECT * FROM {};'.format(table_name))
    results = list(cursor)
    return results

def cleaning_tweets(tweet):
    '''
    Takes in a single tweet and transforms it. Removes mentions, urls, next
    line symbols, makes every letter in the string lowercase, removes punctuation,
    removes stop words, removes empty strings, and removes any extra characters
    that aren't letters.
    Returns a list a words that have been transformed.
    '''
    lemm = WordNetLemmatizer()
    no_mentions = re.sub(r'@[A-Za-z0-9_.]+','',tweet)
    no_urls = re.sub('https?://[A-Za-z0-9./]+','',no_mentions)
    no_nextline = re.sub(r"\s+", " ", no_urls)
    lowered = no_nextline.lower()
    no_punct = lowered.translate(str.maketrans('', '', string.punctuation))
    stop_words = set(stopwords.words('english'))
    no_stops = [lemm.lemmatize(word) for word in no_punct.split(' ') if word not in stop_words]
    no_empty = [w for w in no_stops if w]
    no_quotes = [''.join(let) for let in no_empty if let.isalpha()]
    return no_quotes