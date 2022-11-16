import twitter_scraper as ts
import pandas as pd
import text_clean as tc
import traceback


class Model(ts.TwitterApi):
    def __init__(self,topic=None,user=None):
        super().__init__()
        self.tweets = ts.TwitterApi.get_tweets(topic,user)
        if topic==None:
            self.recent = pd.DataFrame().from_dict(self.tweets['recent'],orient='index')
            self.popular = pd.DataFrame()
        elif user==None:
            self.recent = pd.DataFrame().from_dict(self.tweets['recent'],orient='index')
            self.popular = pd.DataFrame().from_dict(self.tweets['popular'],orient='index')
    
    def prepare(self):
        try:
            s=0
            if self.recent.empty():
                self.recent['clean_text'] = tc.TextClean(self.recent['text'].values)
                s+=1
            if self.popular.empty():
                self.popular['clean_text'] = tc.TextClean(self.popular['text'].values)
                s+=1
            return s
        except Exception as e:
            print('error -> ',str(e))
            return 0
    
    def make_group(self):
        try:
            s = self.prepare()
            if s==0:
                raise Exception('error in prepare()')
            # use ML topic modeling model to classify given list of tweets
        except Exception as e:
            print('Error --> ',str(e))
            traceback.print_exc()