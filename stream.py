import tweepy
from functions import connect_to_tweepy, connect_to_database,streamer

def main(database,table,keywords):
    api = connect_to_tweepy( )
    cursor = connect_to_database(database)
    streamer(api,table,keywords)

if __name__ == "__main__":
    db = input('Please enter a database to connect to: ')
    tbl = input('Please enter a table name to save tweets in: ')
    kywrds = input('Please enter a list of keywords to filter tweets by: ')
    main(db,tbl,kywrds)
