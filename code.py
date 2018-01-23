import web
import serial
from textblob import TextBlob
from libs.analyse_sentiments import TweetBank, TweetSentimentService
from libs.twitterapi import TwitterAPI
from textblob.classifiers import NaiveBayesClassifier
from nltk.tokenize import TweetTokenizer
from textblob.sentiments import NaiveBayesAnalyzer, PatternAnalyzer

urls = (
    '/', 'search',
    '/index', 'index',
    '/show/(.*)', 'show'
)

def add_global_hook():
    tweets = TweetBank(2000)
    train, test = tweets.data_set()
    naive_bayes = NaiveBayesClassifier(train)
    tweetsent_service = TweetSentimentService(naive_bayes,test)
    g = web.storage({"tweetsent_service": tweetsent_service})
    def _wrapper(handler):
        web.ctx.globals = g
        return handler()
    return _wrapper

twitter= TwitterAPI()

render  = web.template.render('templates', base='base')


class search:
    def GET(self):
        return render.search()

class index:
    def POST(self):
        data =web.input()
        web.debug(data)
        tweets =  twitter.retrieve_tweets(data.search)
        if len(tweets) == 0:
            raise web.seeother('/')
        return render.index(tweets)

class show:
    def GET(self,tweet):
        web.debug(tweet)
        return render.show(tweet)

    def POST(self,tweet):
        data = web.data()
        # classification = TextBlob(tweet, analyzer=NaiveBayesAnalyzer())
        neg, pos =  web.ctx.globals.tweetsent_service.classify_tweet(tweet)
        #web.debug( web.ctx.globals.tweetsent_service.accuracy())
        cl =  web.ctx.globals.tweetsent_service.classify(tweet)
        # web.debug(cl)
        # web.debug(classification.sentiment)
        return render.show(tweet,neg, pos, cl)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.add_processor(add_global_hook())
    app.run()
