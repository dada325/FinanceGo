from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
import logging
import os

logging.basicConfig(level=logging.INFO)

# Fetch MongoDB connection string from environment variables
MONGO_CONNECTION_STRING = os.environ.get('MONGO_CONNECTION_STRING', 'YOUR_MONGODB_ADDRESS')

client = MongoClient(MONGO_CONNECTION_STRING)
db = client.news_database

# Ensure the collection is indexed on 'id' for efficient lookups and to prevent duplicates
articles_collection = db.articles
articles_collection.create_index("id", unique=True)

def connect_to_database():
    """
    Ensure that the database connection is active.
    Retry connection if it fails.
    """
    MAX_RETRIES = 3
    retries = 0

    while retries < MAX_RETRIES:
        try:
            # Try connecting to the MongoDB server
            client.server_info()
            return
        except ConnectionFailure:
            retries += 1
            logging.warning(f"Failed to connect to MongoDB. Retrying ({retries}/{MAX_RETRIES})...")
            if retries == MAX_RETRIES:
                logging.error("Max retries reached. Could not connect to MongoDB.")
                raise

def is_in_database(article):
    """
    Check if the article is already in the database.
    """
    connect_to_database()
    return articles_collection.count_documents({'id': article['id']}) != 0

def add_to_database(article):
    """
    Add a new article to the database.
    """
    try:
        connect_to_database()
        articles_collection.insert_one(article)
        logging.info(f"Inserted article {article['id']} into the database.")
    except DuplicateKeyError:
        logging.warning(f"Article {article['id']} is already present in the database.")
    except Exception as e:
        logging.error(f"Error inserting article {article['id']}: {e}")

def get_new_articles():
    """
    Retrieve new articles that haven't been processed yet.
    """
    connect_to_database()
    return articles_collection.find({'processed': False})

def update_article_in_database(processed_article):
    """
    Update the article in the database with the processed data.
    """
    connect_to_database()
    articles_collection.update_one({'id': processed_article['id']}, {"$set": processed_article})

def mark_as_processed(article_id):
    """
    Mark the article as processed in the database.
    """
    connect_to_database()
    articles_collection.update_one({'id': article_id}, {"$set": {"processed": True}})
