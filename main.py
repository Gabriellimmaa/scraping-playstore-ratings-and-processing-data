from google_play_scraper import Sort
from scraping import NLTK, PlayStore, Scraping

if __name__ == '__main__':
    scraper = Scraping(
        playstore_config=PlayStore(
            url='com.samsung.android.app.watchmanager',
            lang='pt',
            country='BR',
            sort=Sort.MOST_RELEVANT,
            filter_score_with=5,
            count=100
        ),
        nltk_config=NLTK(
            lang='portuguese',
            passes=35,
            num_topics=10
        ),
        filename=f"watchmanager"
    )

    scraper.get_matches_LDA()
    scraper.get_matches_NLP()
    scraper.save_result()
