import logging
import requests
import os
from database_helpers import is_in_database, add_to_database

logging.basicConfig(level=logging.INFO)

# Fetching Alpaca API credentials from environment variables
# Here must be change to your own API_KEY on ALPACA
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
        response = call_alpaca_api()
        news_data = response.json()
        
        for article in news_data:
            if not is_in_database(article):
                add_to_database(article)
                logging.info(f"Added article {article['id']} to database.")
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def call_alpaca_api():
    """
    Calls the Alpaca API and returns the response.
    Raises an error for non-2xx responses.
    """
    response = requests.get(ALPACA_ENDPOINT, headers=HEADERS)
    response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
    return response
