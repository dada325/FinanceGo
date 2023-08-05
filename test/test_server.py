# tests/test_server.py

import pytest
import requests
from database_helpers import add_to_database

def test_get_articles():
    # Add a test article to the database
    article = {
        "title": "Test Article",
        "summary": "This is a test article."
    }
    add_to_database(article)

    # Send a GET request to the /api/articles endpoint
    response = requests.get('http://localhost:8000/api/articles')

    # Check that the response status code is 200
    assert response.status_code == 200

    # Check that the response body contains the test article
    articles = response.json()
    assert any(a['title'] == article['title'] for a in articles)
