import tweepy
import re,string

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
        tweets = []
        results = self.api.search(search_topic)
        for tweet in results:
            tweets.append(self.strip_all_entities(self.strip_links(tweet.text)))
        return tweets

    def strip_links(self,text):
        link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
        links = re.findall(link_regex,text)
        for link in links:
            text = text.replace(link[0], ', ')
        return text

    def strip_all_entities(self,text):
        entity_prefixes = ['@','#','RT']
        for separator in  string.punctuation:
            if separator not in entity_prefixes :
                text = text.replace(separator,' ')
        words = []
        for word in text.split():
            word = word.strip()
            if word:
                if word[0] not in entity_prefixes:
                    words.append(word)
        return ' '.join(words)
