from celery_config import app
from database_helpers import get_new_articles, update_article_in_database, mark_as_processed, add_to_database, is_in_database
from .gpt4_processing import process_with_gpt4
import requests
import os
import logging

logging.basicConfig(level=logging.INFO)

# Fetching Alpaca API credentials from environment variables
ALPACA_API_KEY_ID = os.environ.get('ALPACA_API_KEY_ID')
ALPACA_API_SECRET_KEY = os.environ.get('ALPACA_API_SECRET_KEY')

ALPACA_ENDPOINT = "https://data.alpaca.markets/v2/news"
HEADERS = {
    "APCA-API-KEY-ID": ALPACA_API_KEY_ID,
    "APCA-API-SECRET-KEY": ALPACA_API_SECRET_KEY
}

@app.task
def fetch_articles():
    try:
        response = requests.get(ALPACA_ENDPOINT, headers=HEADERS)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code

        news_data = response.json()

        for article in news_data:
            if not is_in_database(article):
                add_to_database(article)
                logging.info(f"Added article {article['id']} to database.")

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

@app.task
def process_articles():
    new_articles = get_new_articles()
    
    for article in new_articles:
        try:
            # Process the article with GPT-4
            processed_article = process_with_gpt4(article)

            # Update the article in the database with the processed data
            update_article_in_database(processed_article)

            # Mark the article as processed
            mark_as_processed(article['id'])
        except Exception as e:
            logging.error(f"An error occurred while processing article {article['id']}: {e}")
