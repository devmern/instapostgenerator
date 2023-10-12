from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import openai

app = Flask(__name__)

# OpenAI GPT-3 API Key
openai.api_key = ''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crawl')
def crawl_url():
    url = request.args.get('url')
    try:
        # Fetch the webpage content
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text content (excluding HTML tags, CSS, etc.)
        text = ' '.join(soup.stripped_strings)

        # text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        # text = ' '.join(text.split())

        return jsonify({"success": True, "text": text})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/generate-instagram-content', methods=['POST'])
def generate_instagram_content():
    data = request.get_json()
    text = data.get('text')

    # Generate Instagram post content using ChatGPT
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Create an Instagram post about:\n{text}\n\nCaption:",
        max_tokens=100
    )

    return jsonify({"content": response.choices[0].text.strip()})

if __name__ == '__main__':
    app.run(debug=True)
