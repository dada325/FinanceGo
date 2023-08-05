from flask import Flask, jsonify
from gpt4_processing import process_with_gpt4
from database_helpers import get_new_articles

app = Flask(__name__)

@app.route('/api/articles', methods=['GET'])
def get_articles():
    articles = get_new_articles()
    processed_articles = [process_with_gpt4(article) for article in articles]
    return jsonify(processed_articles)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
