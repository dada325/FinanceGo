import openai
import os

# Ensure the OpenAI key is correctly set in the environment
assert 'OPENAI_API_KEY' in os.environ, "The OpenAI API key is not set in the environment variables."

def process_with_gpt4(article):
    """
    Processes an article with the GPT-4 API.
    """
    # Prepare the prompt in a step-by-step manner
    prompt = f"""
    Given the following article:
    
    {article['content']}

    Let's analyze it step-by-step:

    1. First, identify the most relevant stock tickers mentioned in the article.
    """
    response = openai.Completion.create(
        engine="text-davinci-004",  # Update the engine ID for GPT-4
        prompt=prompt,
        temperature=0.4,
        max_tokens=50
    )

    stock_tickers = response.choices[0].text.strip()
    article['stock_tickers'] = stock_tickers

    # Continue the prompt to analyze sentiment
    prompt += f"\n\n2. The stock tickers identified are: {stock_tickers}. Now, analyze the overall sentiment of the article."
    response = openai.Completion.create(
        engine="text-davinci-004",  # Update the engine ID for GPT-4
        prompt=prompt,
        temperature=0.4,
        max_tokens=50
    )

    sentiment = response.choices[0].text.strip()
    article['sentiment'] = sentiment

    # Continue the prompt to make a prediction and provide reasoning
    prompt += f"\n\n3. The sentiment analysis result is: {sentiment}. Based on this, predict if the related stocks will be bearish or bullish and provide reasoning for this prediction."
    response = openai.Completion.create(
        engine="text-davinci-004",  # Update the engine ID for GPT-4
        prompt=prompt,
        temperature=0.4,
        max_tokens=100
    )

    prediction_and_reasoning = response.choices[0].text.strip()
    article['prediction_and_reasoning'] = prediction_and_reasoning

    # Continue the prompt to suggest similar articles
    prompt += f"\n\n4. Now, suggest similar articles or news events for further reading."
    response = openai.Completion.create(
        engine="text-davinci-004",  # Update the engine ID for GPT-4
        prompt=prompt,
        temperature=0.4,
        max_tokens=100
    )

    similar_articles = response.choices[0].text.strip()
    article['similar_articles'] = similar_articles

    return article
