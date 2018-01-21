import tweepy


class TwitterAPI:

    def __init__(self):
        self.api = ''


    def OAuth(self):
        # Step 1 - Authenticate
        consumer_key= 'QlI0uxmsJjtkMtMLbOcFlAWxp'
        consumer_secret= 'xdL2FbSlhJ9edICcFoWxqZkGAgjPoTDxbiHhbGIHUPbP6mUWHL'

        access_token='540384142-is3cHukZMOqRbcqV1l51L58XsXRIX6uvLaleHAPw'
        access_token_secret='sKSKtZ2UmgAv7GPl9IM1U0aAiGGLXTeaPKk5IU7TjPoRi'

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        return tweepy.API(auth)

    def retrieve_tweets(self, search_topic):
        self.api = self.OAuth()
        #Step 3 - Retrieve Tweets
        tweets = self.api.search(search_topic)

        return tweets
