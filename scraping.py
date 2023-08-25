import datetime
from google_play_scraper import Sort, reviews
import pandas as pd
from transformers import pipeline
import os
import re
from gensim import corpora, models
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('stopwords')


class PlayStore():
    def __init__(self, url, lang, country, count: int = 100, sort: Sort = Sort.NEWEST, filter_score_with: int = 5):
        self.url = url
        self.lang = lang
        self.country = country
        self.sort = sort
        self.count = count
        self.filter_score_with = filter_score_with


class NLTK():
    def __init__(self, lang: str = 'portuguese', num_topics: int = 10, passes: int = 35):
        self.stop_words = set(stopwords.words(lang))
        self.passes = passes
        self.num_topics = num_topics


class Scraping():
    def __init__(self, playstore_config: PlayStore, nltk_config: NLTK, filename: str, directory_save: str = "result"):
        self.playstore_config = playstore_config
        self.nltk_config = nltk_config
        self.result_scrape = None
        self.date_string = None
        self.result_LDA = None
        self.result_NLP = None
        self.directory_save = None

        result, continuation_token = reviews(
            self.playstore_config.url,
            lang=self.playstore_config.lang,
            country=self.playstore_config.country,
            sort=self.playstore_config.sort,
            count=self.playstore_config.count,
            filter_score_with=self.playstore_config.filter_score_with
        )

        result, _ = reviews(
            self.playstore_config.url,
            continuation_token=continuation_token
        )
        self.result_scrape = result

        df_busu = pd.DataFrame(result)

        if not os.path.exists(directory_save):
            os.makedirs(directory_save)

        current_datetime = datetime.datetime.now()
        date_string = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

        if not os.path.exists(f"{directory_save}/{filename}_score={self.playstore_config.filter_score_with}_{date_string}"):
            os.makedirs(
                f"{directory_save}/{filename}_score={self.playstore_config.filter_score_with}_{date_string}")

        self.directory_save = f"{directory_save}/{filename}_score={self.playstore_config.filter_score_with}_{date_string}/{filename}_score={self.playstore_config.filter_score_with}_sort={'MOST_RELEVANT' if self.playstore_config.sort == 1 else 'NEWEST' }"

        # Save the DataFrame to a CSV file with the current date and time in the filename
        df_busu.to_csv(
            f"{self.directory_save}.csv", index=False)

    def get_result(self):
        return self.result_scrape

    def get_matches_LDA(self):
        # Concatenate the content of reviews
        content = ' '.join([review['content']
                            for review in self.result_scrape])

        # preprocess
        content = re.sub(
            r'[^\w\s]', '', content)
        content = content.lower()

        # Tokenization and stopword removal
        words = [palavra for palavra in word_tokenize(
            content) if palavra not in self.nltk_config.stop_words]

        # Creating the dictionary and corpus
        dicionario = corpora.Dictionary([words])
        corpus = [dicionario.doc2bow(words)]

        # Topic modeling using LDA
        model_lda = models.LdaModel(
            corpus, num_topics=self.nltk_config.num_topics, id2word=dicionario, passes=self.nltk_config.passes)

        self.result_LDA = model_lda.print_topics()
        return model_lda.print_topics()

    def get_matches_NLP(self):
        reviews = [value['content'] for value in self.result_scrape]

        def preprocess_text(text):
            text = re.sub(r'[^\w\s]', '', text)
            text = text.lower()
            words = text.split()
            return words

        # Load the BERT model for sentiment analysis
        nlp = pipeline("feature-extraction")  # Extract features from text

        # Analyze the sentiment of each review
        features = []
        for review in reviews:
            sentiment = nlp(review)[0]
            features.append(sentiment)

        keywords_used = set()

        for idx, sentiment in enumerate(features):
            review = reviews[idx]
            words = preprocess_text(review)
            for word in words:
                keywords_used.add(word)

        self.result_NLP = keywords_used
        return keywords_used

    def save_result(self):
        with open(f"{self.directory_save}.txt", "w", encoding="utf-8") as f:
            f.write(f"""-------------------- Configs --------------------
PlayStore configs:
URL: {self.playstore_config.url}
Lang: {self.playstore_config.lang}
Country: {self.playstore_config.country}
Sort: {'MOST_RELEVANT' if self.playstore_config.sort == 1 else 'NEWEST' }
Count: {self.playstore_config.count}
Filter Score With: {self.playstore_config.filter_score_with}

LDA configs:
Passes: {self.nltk_config.passes}
Num Topics: {self.nltk_config.num_topics}\n\n""")
            f.write(f"---------------------- LDA ----------------------\n")
            for x in self.result_LDA:
                f.write(f"{x}\n")

            f.write(f"\n---------------------- NLP ----------------------\n")
            for x in self.result_NLP:
                f.write(f"{x}\n")

        print("██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████")
        print(f"\nResult saved in: {self.directory_save}\n")
        print("██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████")
