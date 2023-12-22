from twitter_key_main import *
import tweepy
import traceback
import pandas as pd
import argparse
import sys


class TwitterApi:
    def __init__(self,consumer_key,consumer_secret,access_token,access_token_secret):
        self.c_key = consumer_key
        self.c_secret = consumer_secret
        self.a_token = access_token
        self.a_token_secret = access_token_secret
        self.api = self.Connect()
        try:
            if not self.test_api():
                raise Exception('\n[*] Connection Error')
        except Exception as e:
            print(str(e))
            traceback.print_exc()

    def Connect(self):
        print('[*] Attempting Connection to twitter...')
        try:
            auth = tweepy.OAuthHandler(self.c_key, self.c_secret)
            auth.set_access_token(self.a_token, self.a_token_secret)
            con = tweepy.API(auth, wait_on_rate_limit=True)
            return con
        except Exception as e:
            traceback.print_exc()
            return None

    def get_tweets(self,user=None,topic=None):
        try:
            if self.api == None:
                raise Exception('error connecting to twitter')
            data = {}
            if user!=None:
                data_recent = {}
                d = self.api.user_timeline(screen_name=user,tweet_mode='extended',count=150)
                for i in range(len(d)):
                    data_recent[i]={
                        'text':d[i].full_text,
                        'time':d[i].created_at,
                        'entities':d[i].entities
                    }
                data['recent_tweet'] = data_recent
                del data_recent
            elif topic!=None:
                d = self.api.search_tweets(q=topic,tweet_mode='extended',count=150,result_type='recent',include_entities=True)
                data_recent = {}
                for i in range(len(d)):
                    data_recent[i]={
                        'text':d[i].full_text,
                        'time':d[i].created_at,
                        'entities':d[i].entities
                    }
                data['recent_tweet'] = data_recent
                d_ = self.api.search_tweets(q=topic,tweet_mode='extended',count=150,result_type='popular',include_entities=True)
                data_popular = {}
                for i in range(len(d_)):
                    data_popular[i]={
                        'text':d_[i].full_text,
                        'time':d_[i].created_at,
                        'entities':d_[i].entities
                    }
                data['popular_tweet']=data_popular
                del data_popular,data_recent
            else:
                raise Exception('Please provide with correct name or topic !')               
            return data
        except Exception as e:
            print('\n[!] Error (get_tweets):',str(e))
            traceback.print_exc()
            return {}

    def test_api(self):
        print('[*] Testing Connection ...')
        try:
            tw = self.api.home_timeline()
            print('-'*19)
            for i in range(2):
                print(tw[i].text)
            print('-'*19)
            print('[*] Connection test success\n\n')
            return True
        except Exception as e:
            print('-'*19)
            print('\n[!] Error (test_api):',str(e),'\n\n')
            return False




if __name__=='__main__':
    try:
        parser = argparse.ArgumentParser(prog='python3 twitter_scrapper.py',
                        description='\n twitter_scrapper, scrpit helps you in scrapping tweets from twitter for a user or topic!')
        parser.add_argument('-u','--user',help='give a user name to collect tweets for that particular user')
        parser.add_argument('-t','--topic',help='give a topic name (person name, event name) to collect tweets related to that')
    
        args = parser.parse_args()
        user,topic = None,None
        if args.user !=None:
            user = str(args.user).strip()
        elif args.topic != None:
            topic = str(args.topic).strip()
        else:
            parser.print_help()
            raise Exception('[!] (No arguments passed) or (arguments passed incorectly)\n')
    
        # initiate & fetch -> twitter api
        ck,cs = consumer_key, consumer_secret
        at,ats = access_token, access_token_secret
        con_obj = TwitterApi(ck,cs,at,ats)
        t_data = con_obj.get_tweets(user=user,topic=topic)
        # store data (dictionary) -> csv file
        if user!=None:
            df = pd.DataFrame().from_dict(t_data['recent_tweet'],orient='index')
            df.to_csv('data/tweet_user_{}.csv'.format(user),index=False)
        elif topic!=None:
            if 'recent_tweet' in t_data.keys():
                df = pd.DataFrame().from_dict(t_data['recent_tweet'],orient='index')
                df.to_csv('data/tweet_topic_r_{}.csv'.format(topic),index=False)
            if 'popular_tweet' in t_data.keys():
                df = pd.DataFrame().from_dict(t_data['popular_tweet'],orient='index')
                df.to_csv('data/tweets_topic_p_{}.csv'.format(topic),index=False)
        print('\n[*] Data Saved !\n')

    except Exception:
        traceback.print_exc()