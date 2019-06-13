import tweepy
import os
from functions import create_database, connect_to_database, create_table

def main(database,table):
    create_database(database)
    cur = connect_to_database(database)
    create_table(cur,table)



if __name__ == "__main__":
    db = input('Please enter a name for the database that will be created: ')
    tbl = input('Please enter a name for the table that will be created: ')
    main(database=db,table=tbl)