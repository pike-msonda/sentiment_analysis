from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
from nltk.corpus import twitter_samples, stopwords
from nltk.sentiment.util import *
from nltk.tokenize import TweetTokenizer
from textblob.sentiments import NaiveBayesAnalyzer, PatternAnalyzer

class TweetBank:

    def __init__(self, n_tweets):
        self.n_tweets =  n_tweets

    def data_set(self):
        if self.n_tweets is not None:
            self.n_tweets = int(self.n_tweets/2)
        tokenizer = TweetTokenizer()
        fields = ['id', 'text']
        positive_json = twitter_samples.abspath("positive_tweets.json")
        positive_csv = 'positive_tweets.csv'
        json2csv_preprocess(positive_json,positive_csv,fields,limit=self.n_tweets)

        negative_json = twitter_samples.abspath("negative_tweets.json")
        negative_csv = 'negative_tweets.csv'
        json2csv_preprocess(negative_json, negative_csv, fields, limit=self.n_tweets)

        neg_docs = parse_tweets_set(negative_csv, label='neg')
        pos_docs = parse_tweets_set(positive_csv, label='pos')

            # We separately split subjective and objective instances to keep a balanced
            # uniform class distribution in both train and test sets.
        train_pos_docs, test_pos_docs = split_train_test(pos_docs)
        train_neg_docs, test_neg_docs = split_train_test(neg_docs)

        training_tweets = train_pos_docs+train_neg_docs
        testing_tweets = test_pos_docs+test_neg_docs

        training_tweets = train_pos_docs+train_neg_docs
        testing_tweets = test_pos_docs+test_neg_docs

        return training_tweets, testing_tweets

class TweetSentimentService:

    def __init__(self,classifier, test_set):
        self.classifier = classifier
        self.test_set = test_set

    def classify_tweet(self,tweet):
        classification =self.classifier.prob_classify(tweet)
        return classification.prob('neg'), classification.prob('pos')

    def classify(self,text):
        return self.classifier.classify(text)

    def accuracy(self):
        return self.classifier.accuracy(self.test_set)
