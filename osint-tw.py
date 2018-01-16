
import logging
import argparse
import time
import json
import re
from dateutil import parser
import pymysql.cursors

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from urllib.parse import urlparse
import database_osint as db


def get_twitter_authen():
    """
        Get your application keys: https://apps.twitter.com/
        Provide your Twitter API credentials HERE:
    """

    try:
        consumer_key = 'xxxxxxxxxxxxxxxxxxxxxxxx'
        consumer_secret = 'xxxxxxxxxxxxxxxxxxxxxxxx'
        access_token = 'xxxxxxxxxxxxxxxxxxxxxxxx'
        access_secret = 'xxxxxxxxxxxxxxxxxxxxxxxx'
    except KeyError:
        logging.info("osint-tw - Twitter variables not set\n")
    authen = OAuthHandler(consumer_key, consumer_secret)
    authen.set_access_token(access_token, access_secret)
    return authen


def db_conection():
    """
    SETUP your DATABASE parameters here
    """
    config = {'user': 'osintuser', 'password': 'password', 'host': 'localhost', 'port': 3306, 'database': 'osint', 'charset': 'utf8mb4'}
    cnx = 0
    try:
        cnx = pymysql.connect(**config)
    except pymysql.Error as err:
        logging.info("osint-tw - ", err)
        cnx.close()
    return cnx


def store_tweet(tweet_id, text, created_at, screen_name, lang):
    """
    Store a phishing tweet into the DB. It doesn't store RT.
    """
    dab = db.db_conection()
    cursor = dab.cursor()
    try:
        cursor = dab.cursor()
        insert_query = "INSERT INTO `tweets` (`tweet_id`, `tweet_text`, `created_at`, `screen_name`, `lang`) VALUES (%s, " \
                       "%s, %s, %s, %s) "
        
        cursor.execute(insert_query, (tweet_id, text, created_at, screen_name, lang))
        dab.commit()
        cursor.close()
        dab.close()
    except pymysql.Error as mysql_err:
        logging.info("osint-tw - ", mysql_err)
        dab.close()
    return


def store_tweet_tag(tweet_id, hashtag):
    """
       Store HASHTAGS tweet into the DB
    """
    dab = db.db_conection()
    cursor = dab.cursor()
    try:
        cursor = dab.cursor()
        insert_query = "INSERT INTO `tweet_tags` (`tweet_id`, `tag`) VALUES (%s, %s)"
        cursor.execute(insert_query, (tweet_id, str(hashtag)))
        dab.commit()
        cursor.close()
        dab.close()
    except pymysql.Error as mysql_err:
        logging.info("osint-tw - ", mysql_err)
        dab.close()
    return


def store_tweet_url(tweet_id, url):
    """
          Store URLS tweet into the DB
    """
    dab = db.db_conection()
    cursor = dab.cursor()
    try:
        cursor = dab.cursor()
        insert_query = "INSERT INTO `tweet_urls` (`tweet_id`, `url`) VALUES (%s, %s)"
        cursor.execute(insert_query, (tweet_id, url))
        dab.commit()
        cursor.close()
        dab.close()
    except pymysql.Error as mysql_err:
        logging.info("osint-tw - ", mysql_err)
        dab.close()
    return


def store_tweet_media_url(tweet_id, media_url):
    """
        Store MEDIA URLS tweet into the DB
    """
    dab = db.db_conection()
    cursor = dab.cursor()
    try:
        cursor = dab.cursor()
        insert_query = "INSERT INTO `tweet_media_urls` (`tweet_id`, `media_url`) VALUES (%s, %s)"
        cursor.execute(insert_query, (tweet_id, media_url))
        dab.commit()
        cursor.close()
        dab.close()
    except pymysql.Error as mysql_err:
        logging.info("osint-tw - ", mysql_err)
        dab.close()

    return


class CustomListener(StreamListener):
    """
           listening tweets related to phishing.
        """
    def on_data(self, data):
        try:

            datajson = json.loads(data)
            if not datajson['text'].startswith('RT'):
                text = re.sub(r"(?:https?\://)\S+", "", datajson['text']).encode("utf8")
                screen_name = datajson['user']['screen_name']
                tweet_id = datajson['id']
                created_at = parser.parse(datajson['created_at'])
                lang = datajson['lang']
                store_tweet(tweet_id, text, created_at, screen_name, lang)
                for hashtag in datajson['entities']['hashtags']:
                    store_tweet_tag(tweet_id, hashtag['text'])
                for url in datajson['entities']['urls']:
                    store_tweet_url(tweet_id, url['url'])
                if 'media' in datajson['entities']:
                    store_tweet_media_url(tweet_id, datajson['entities']['media'][0]['media_url'])
        except Exception as e:
            logging.info("osint-tw - ", e)
            time.sleep(5)

    def on_error(self, status):
        if status == 420:
            logging.info("osint-tw - Rate limit exceeded\n")
            time.sleep(200)
            return False
        else:
            logging.info("osint-tw - Error {}\n".format(status))
            return True



def main(args):
    
    myfilter = args.filter
    mylang = args.lang
    query = urlparse(myfilter)
    logging.basicConfig(level=logging.DEBUG, filename="/var/log/traphuman.log", filemode="a+", 
    format="%(asctime)-15s %(levelname)-8s %(message)s")
    auth = get_twitter_authen()
    twitter_stream = Stream(auth, CustomListener(query))
    twitter_stream.filter(track=query, languages=[mylang], async=True)
                                                                                                                  
if __name__ == '__main__':
    
    intro = '''
    
    Examples of use:
        osint-tw.py 
    
        osint-tw.py -f "phishing and #phishing" -l "en,es"
    '''
    par = argparse.ArgumentParser(description='Copyright - TrapHuman - @networkseg1 @forges32  - Harvester phishing tweets',
    epilog=intro, formatter_class=argparse.RawTextHelpFormatter)
    
    par.add_argument('-f', '--filter', help='words to filter in twitter', default='phishing and #phishing')
    par.add_argument('-l', '--lang', help='tweets language', default='en,es')
    argus = par.parse_args()
    main(argus)
                            
