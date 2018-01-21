from nltk.tokenize import TweetTokenizer
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk.tokenize as tokenize
from nltk.sentiment import SentimentAnalyzer
from nltk.classify import NaiveBayesClassifier
from nltk.sentiment.util import *
from nltk.corpus import twitter_samples, stopwords

class SentimentService:

    # Different customizations for the TweetTokenizer

    # tokenizer = TweetTokenizer(preserve_case=True, strip_handles=True)
    # tokenizer = TweetTokenizer(reduce_len=True, strip_handles=True)
    def __init__(self):
        self.tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,
        reduce_len=True)

        self.sentim_analyzer = SentimentAnalyzer()

        self.vader_sentiment =  SentimentIntensityAnalyzer()
        self.test_set = ''

    def word_feats(self, words):
        return dict([(word, True) for word in words])

    def train_classifier(self, trainer, n_instances=None):

        if n_instances is not None:
            n_instances = int(n_instances/2)

        fields = ['id', 'text']
        positive_json = twitter_samples.abspath("positive_tweets.json")
        positive_csv = 'positive_tweets.csv'
        json2csv_preprocess(positive_json,positive_csv,fields,limit=n_instances)

        negative_json = twitter_samples.abspath("negative_tweets.json")
        negative_csv = 'negative_tweets.csv'
        json2csv_preprocess(negative_json, negative_csv, fields, limit=n_instances)

        neg_docs = parse_tweets_set(negative_csv, label='neg', word_tokenizer=self.tokenizer)
        pos_docs = parse_tweets_set(positive_csv, label='pos', word_tokenizer=self.tokenizer)

        # We separately split subjective and objective instances to keep a balanced
        # uniform class distribution in both train and test sets.
        train_pos_docs, test_pos_docs = split_train_test(pos_docs)
        train_neg_docs, test_neg_docs = split_train_test(neg_docs)

        training_tweets = train_pos_docs+train_neg_docs
        testing_tweets = test_pos_docs+test_neg_docs


        # stopwords = stopwords.words('english')
        # all_words = [word for word in sentim_analyzer.all_words(training_tweets) if word.lower() not in stopwords]
        all_words = [word for word in self.sentim_analyzer.all_words(training_tweets)]

        # Add simple unigram word features
        unigram_feats = self.sentim_analyzer.unigram_word_feats(all_words, top_n=1000)
        self.sentim_analyzer.add_feat_extractor(extract_unigram_feats,
                                            unigrams=unigram_feats)

        # Add bigram collocation features
        bigram_collocs_feats = self.sentim_analyzer.bigram_collocation_feats([tweet[0] for tweet in training_tweets],
            top_n=100, min_freq=12)
        self.sentim_analyzer.add_feat_extractor(extract_bigram_feats, bigrams=bigram_collocs_feats)

        training_set = self.sentim_analyzer.apply_features(training_tweets)
        self.test_set = self.sentim_analyzer.apply_features(testing_tweets)


        classifier = self.sentim_analyzer.train(trainer, training_set)
        # classifier = sentim_analyzer.train(trainer, training_set, max_iter=4)
        return classifier

    def classify_tweet(self, tweet):
        words = self.tokenizer.tokenize(tweet)
        features = self.word_feats(words)
        return  self.vader_sentiment.polarity_scores(tweet), self.sentim_analyzer.classify(features)

    def accuracy(self, classifier):
        try:
            classifier.show_most_informative_features()

            print 'accuracy:', nltk.classify.util.accuracy(classifier, self.test_set)
        except AttributeError:
            print('Your classifier does not provide a show_most_informative_features() method.')
        results = self.sentim_analyzer.evaluate(self.test_set)
        return results

# sentiment_service =  SentimentService()
# classifier = sentiment_service.train_classifier(NaiveBayesClassifier.train, 2000)
# results = sentiment_service.accuracy(classifier)
# print(sentiment_service.classify_tweet("I love going to school"))
