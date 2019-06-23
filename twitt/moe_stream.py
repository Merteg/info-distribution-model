from tweepy import API 
from tweepy import Cursor
from tweepy import OAuthHandler
from tweepy import TweepError
import time
from datetime import datetime

import json
import config
import pytz


def to_timestamp(a_date):
    if a_date.tzinfo:
        epoch = datetime(1970, 1, 1, tzinfo=pytz.UTC)
        diff = a_date.astimezone(pytz.UTC) - epoch
    else:
        epoch = datetime(1970, 1, 1)
        diff = a_date - epoch
    return int(diff.total_seconds())


# # # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_api = API(self.auth)

        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_api.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets


# # # # TWITTER AUTHENTICATER # # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
        auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
        return auth

 
if __name__ == '__main__':
 
    # Authenticate using config.py and connect to Twitter Streaming API.
    # hash_tag_list = ["donal trump", "hillary clinton", "barack obama", "bernie sanders"]
    # fetched_tweets_filename = "tweets.txt"

    twitter_client = TwitterClient('Yatsenyuk_AP')

    original_tweet = twitter_client.get_user_timeline_tweets(1)[0]
    print original_tweet.created_at

    magic_dict = {
        "tweet_id": original_tweet.id,
        "time": to_timestamp(
            original_tweet.created_at
            # datetime.strptime(original_tweet.created_at, '%Y-%m-%d %H:%M:%s')
        ),
        "author_id": original_tweet.user.id,
        "author_name": original_tweet.user.name,
        "retweets": []
    }
    tmp_api = twitter_client.twitter_api
    try:
        results = tmp_api.retweets(original_tweet.id, 100)
    except TweepError:
        print "SLEEP"
        time.sleep(15 * 60)
        results = tmp_api.retweets(original_tweet.id)
    results.sort(key=lambda x: x.created_at, reverse=False)

    agents = [retweet.user.id for retweet in results]
    agents.append(original_tweet.user.id)
    try:
        agents_names = [
            (agent, tmp_api.get_user(agent).screen_name) for agent in agents
        ]
    except TweepError:
        print "SLEEP"
        time.sleep(15 * 60)
        agents_names = [
            (agent, tmp_api.get_user(agent).screen_name) for agent in agents
        ]
    for retweet in results:
        print retweet.created_at
        # datetime_object = datetime.strptime(retweet.created_at, '%Y-%m-%d %H:%M:%s')
        timestamp_re = to_timestamp(retweet.created_at)
        try:
            f_ids = tmp_api.friends_ids(id=retweet.user.id)
        except TweepError:
            print "SLEEP"
            time.sleep(15 * 60)
            f_ids = tmp_api.friends_ids(id=retweet.user.id)

        press_from = []
        find = False
        for agent in agents_names:
            if agent[0] in f_ids:
                print str(retweet.user.id) + " -> " + str(agent[0])
                press_from.append(agent)
                find = True
        if not find:
            print "SHIT"

        magic_dict["retweets"].append({
            "time": timestamp_re,
            "author_id": retweet.user.id,
            "author_name": retweet.user.name,
            "press_from": press_from
        })

    with open('result_Yatsenyuk_AP.json', 'w') as fp:
        json.dump(magic_dict, fp)

#    twitter_streamer = TwitterStreamer()
#    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)

