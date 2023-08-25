# Scraping PlayStore Ratings and Processing Data

This repository aims to extract reviews of applications hosted on the playstore and process the data with natural language in order to find relevant topics mentioned in user comments.

# About

This project aims to extract app reviews from the playstore, with this data we apply natural languages to determine which words were most approached according to the mass of data.

Based on this data, we can have an assessment with a certain precision and do a deeper research on what are the positive and negative points of the application.

# How to run the code

1. Clone this repository on your computer:

   git clone https://github.com/Gabriellimmaa/scraping-playstore-ratings-and-processing-data.git
2. Make sure you have all the necessary libraries installed.

   pip install -r requirements.txt
3. In the `Main.py` file you will find some configurations to be done

   ```
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
   ```

| PlayStore Configs   |                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **parameter** | **explanation**                                                                                                                                                                                                                                                                                                                                                                                                       |
| url                 | You can find it in the app url on playstore<br />(https://play.google.com/store/apps/details?id=com.samsung.android.app.watchmanager)                                                                                                                                                                                                                                                                                       |
| country & lang      | The country and language codes that can be included in the `lang` and `country` parameters described below depend on the [ISO 3166](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes) and [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) standards, respectively. <br />Therefore, we recommend using an ISO database library such as [pycountry](https://github.com/flyingcircusio/pycountry). |
| sort                | Sort.NEWEST or Sort.MOST_RELEVANT                                                                                                                                                                                                                                                                                                                                                                                           |
| filter_score_with   | 1-5                                                                                                                                                                                                                                                                                                                                                                                                                         |
| count               | counter how much data will return                                                                                                                                                                                                                                                                                                                                                                                           |

| NLTK Configs        |                                                                                                                                          |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **parameter** | **explanation**                                                                                                                    |
| lang                | instead of putting the abbreviation you need to put the name of the language                                                             |
| passes              | Control how many times the algorithm cycles through the complete data set during training.<br />The higher the value, the more accurate. |
| num_topics          | you are telling the model how many topics it should try to discover from your data                                                       |

4. Run `main.py`:

   `python Main.py`

# Autores

| [`<img src="https://github.com/Gabriellimmaa.png" width=115><br>``<sub>`Gabriel Lima `</sub>`](https://github.com/Gabriellimmaa) |
| :-------------------------------------------------------------------------------------------------------------------------------: |
