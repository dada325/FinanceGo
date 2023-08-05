# tests/test_gpt4_processing.py

import pytest
from gpt4_processing import process_with_gpt4

def test_process_with_gpt4():
    article = {
        "title": "Test Article",
        "summary": "This is a test article."
    }

    result = process_with_gpt4(article)

    assert 'title' in result
    assert 'summary' in result
    assert 'stock_tickers' in result
    assert 'sentiment' in result
    assert 'reasoning' in result
