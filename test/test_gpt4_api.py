# tests/test_gpt4_api.py

import pytest
from unittest.mock import Mock, patch
from gpt4_processing import process_with_gpt4

@patch('gpt4_processing.requests.post')
def test_process_with_gpt4(mock_post):
    # Mock the GPT-4 API response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'id': 'test_id',
        'object': 'text.completion',
        'choices': [
            {
                'text': 'Test text',
                'finish_reason': 'stop',
                'index': 0
            }
        ]
    }
    mock_post.return_value = mock_response

    # Define a test article
    test_article = {
        'id': 'test_id',
        'title': 'Test title',
        'summary': 'Test summary'
    }

    # Call the function with the test article
    processed_article = process_with_gpt4(test_article)

    # Check that the function made a request to the correct URL
    mock_post.assert_called_once_with(
        'https://api.openai.com/v1/engines/davinci-codex/completions',
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer YOUR_GPT4_API_KEY'
        },
        json={
            'prompt': 'Test summary',
            'max_tokens': 100
        }
    )

    # Check that the function processed the article correctly
    assert processed_article['id'] == 'test_id'
    assert processed_article['title'] == 'Test title'
    assert processed_article['summary'] == 'Test summary'
    assert processed_article['gpt4_output'] == 'Test text'
