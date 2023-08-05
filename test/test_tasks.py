# tests/test_tasks.py

import pytest
from tasks import fetch_articles, process_articles
from database_helpers import get_new_articles, is_in_database
from unittest.mock import patch

def test_fetch_articles():
    # Test that fetch_articles adds articles to the database
    fetch_articles()
    new_articles = get_new_articles()
    assert len(new_articles) > 0

@patch('tasks.process_with_gpt4')
def test_process_articles(mock_process_with_gpt4):
    # Mock the process_with_gpt4 function to return the same article
    mock_process_with_gpt4.side_effect = lambda article: article

    # Test that process_articles marks articles as processed
    process_articles()
    new_articles = get_new_articles()
    assert all(a['processed'] for a in new_articles)
