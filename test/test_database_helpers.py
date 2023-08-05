# tests/test_database_helpers.py

import pytest
from database_helpers import add_to_database, is_in_database, get_new_articles, update_article_in_database, mark_as_processed

def test_database_functions():
    test_article = {
        "id": "test_id",
        "title": "Test Article",
        "summary": "This is a test article.",
        "processed": False
    }

    # Test adding to the database
    add_to_database(test_article)
    assert is_in_database(test_article) == True

    # Test getting new articles
    new_articles = get_new_articles()
    assert any(a['id'] == test_article['id'] for a in new_articles)

    # Test updating an article in the database
    test_article['summary'] = "This is an updated test article."
    update_article_in_database(test_article)
    updated_article = next(a for a in get_new_articles() if a['id'] == test_article['id'])
    assert updated_article['summary'] == "This is an updated test article."

    # Test marking an article as processed
    mark_as_processed(test_article['id'])
    assert next((a for a in get_new_articles() if a['id'] == test_article['id']), None) is None

    # Teardown: remove test_article from database after test
