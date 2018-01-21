import web
from libs.sentiment_service import SentimentService
from libs.twitterapi import TwitterAPI
from nltk.classify import NaiveBayesClassifier


urls = (
    '/', 'search',
    '/index', 'index',
    '/show/(.*)', 'show'
)
### Templates
t_globals = {
    'datestr': web.datestr
}
render  = web.template.render('templates/')

twitter= TwitterAPI()
sentiment_service =  SentimentService()
classifier = sentiment_service.train_classifier(NaiveBayesClassifier.train, 2000)
# results = sentiment_service.accuracy(classifier)

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
        web.debug(tweet)
        result, clas = sentiment_service.classify_tweet(tweet)
        web.debug(result)
        web.debug(clas)
        return render.show(tweet)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
