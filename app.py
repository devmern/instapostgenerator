import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import openai

load_dotenv()

app = Flask(__name__)

# OpenAI GPT-3 API Key
openai.api_key = os.getenv("OPENAI_API_KEY")
port = os.getenv("port")

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

    post_content = response.choices[0].text.strip()

    # Generate relevant hashtags using ChatGPT
    hashtags_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Generate relevant hashtags for:\n{post_content}\n\nHashtags:",
        max_tokens=100  # You can adjust this number as needed
    )

    hashtags = hashtags_response.choices[0].text.strip().split('\n')

    # Generate relevant locations using ChatGPT
    locations_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Generate relevant locations for:\n{post_content}\n\nLocations:",
        max_tokens=60  # You can adjust this number as needed
    )

    locations = locations_response.choices[0].text.strip().split('\n')

    # Generate relevant users to tag using ChatGPT
    users_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Generate relevant Instagram users to tag for:\n{post_content}\n\nUsers:",
        max_tokens=60  # You can adjust this number as needed
    )

    users_to_tag = users_response.choices[0].text.strip().split('\n')

    return jsonify({"content": post_content, "hashtags": hashtags, "locations": locations, "users_to_tag": users_to_tag})


if __name__ == '__main__':
    app.run(debug=True, port=port)
