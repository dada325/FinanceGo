import openai

def process_with_gpt3(article):
    """
    Processes an article with the GPT-3 API.
    """
    prompt = article['content']
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100  # Limit the output length
    )

    processed_text = response.choices[0].text.strip()

    # Depending on what you're using GPT-3 for, you could modify the article data here
    # For example, if processed_text is a summary of the article:
    article['summary'] = processed_text

    return article
