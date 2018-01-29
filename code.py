import web
import serial
import numpy
from textblob import TextBlob
from libs.analyse_sentiments import TweetBank, TweetSentimentService
from libs.twitterapi import TwitterAPI
from textblob.classifiers import NaiveBayesClassifier, MaxEntClassifier, DecisionTreeClassifier
from nltk.tokenize import TweetTokenizer
from textblob.sentiments import NaiveBayesAnalyzer, PatternAnalyzer

urls = (
    '/', 'search',
    '/index', 'index',
    '/show/(.*)', 'show'
)

web.config.debug = False

def add_global_hook():
    tweets = TweetBank(50)
    train, test = tweets.data_set()

    naive_bayes = NaiveBayesClassifier(train)
    maxent = MaxEntClassifier(train)
    classifier_dictionary = {"Naive Bayes": naive_bayes, "Maxent": maxent}
    g = web.storage({"classifier_dictionary": classifier_dictionary,
    "test_set": test})
    def _wrapper(handler):
        web.ctx.globals = g
        return handler()
    return _wrapper

twitter= TwitterAPI()
app = web.application(urls, globals())
render  = web.template.render('templates', base='base')

if web.config.get('_session') is None:
    session =  web.session.Session(app, web.session.DiskStore('sessions'))
    web.config._session = session
else:
    session = web.config._session

class search:
    def GET(self):
        return render.search()

class index:
    def POST(self):
        data =web.input()
        session.classifier = data.classifiers
        tweets =  twitter.retrieve_tweets(data.search)
        if len(tweets) == 0:
            raise web.seeother('/')
        return render.index(tweets)

class show:
    def GET(self,tweet):
        web.debug(tweet)
        return render.show(tweet)

    def POST(self,tweet):
        data = web.input()
        classifier_name = session.classifier
        classifier = web.ctx.globals.classifier_dictionary[classifier_name]
        test_set = web.ctx.globals.test_set

        if (classifier_name == "Maxent"):
            kwargs = {'max_iter':3}
            classifier.train(**kwargs)
        tweetsent_service =  TweetSentimentService(classifier, test_set)
        neg, pos =  tweetsent_service.classify_tweet(tweet)
        cl =  tweetsent_service.classify(tweet)
        return render.show(tweet,neg, pos, cl, classifier_name)

if __name__ == "__main__":
    app.add_processor(add_global_hook())
    app.run()
