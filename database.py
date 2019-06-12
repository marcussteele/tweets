import tweepy
import os
from functions import create_database, connect_to_database, create_table

def main():
    create_database('tweet')
    cur = connect_to_database('tweet')
    create_table(cur,'beer_tweets')

if __name__ == "__main__":
    main()