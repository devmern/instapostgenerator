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


    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
            "role": "system",
            "content": "You are a helpful social media content writer.\n"
            },
            {
            "role": "user",
            "content": f'Generate content without hashtags for social media platforms:\\n\\nInstagram Post (150 characters): [INSTAGRAM_POST]\\n\\nFacebook Post (150 characters): [FACEBOOK_POST]\\n\\nTwitter Post (280 characters): [TWITTER_POST]\\n\\nBased on the following:\n{text}'

            }
        ],
        temperature=1,
        max_tokens=600,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )


    generated_content = response.choices[0].message.content.strip()

    #print (generated_content)

    # Extract content for each social media platform from the generated text
    content_parts = generated_content.split('\n\n')

    print (content_parts)

    instagram_post = ""
    facebook_post = ""
    twitter_post = ""

    for part in content_parts:
        if part.startswith("Instagram") or part.startswith('[INSTAGRAM_POST]'):
            instagram_post = part.replace("Instagram Post (150 characters):", "").replace("INSTAGRAM_POST: ", "").replace("Instagram Post:","").replace("[INSTAGRAM_POST]","")
        elif part.startswith("Facebook") or part.startswith("[FACEBOOK_POST]"):
            facebook_post = part.replace("Facebook Post (150 characters):", "").replace("FACEBOOK_POST: ", "").replace("Facebook Post:","").replace("[FACEBOOK_POST]","")
        elif part.startswith("Twitter") or part.startswith("[TWITTER_POST]"):
            twitter_post = part.replace("Twitter Post (280 characters):", "").replace("TWITTER_POST: ", "").replace("Twitter Post:","").replace("[TWITTER_POST]","")

    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
            "role": "system",
            "content": "You are a helpful social media content writer.\n"
            },
            {
            "role": "user",
            "content": f"Generate 15 relevant Instagram hashtags for:\n{instagram_post}\n\nHashtags:",

            }
        ],
        temperature=1,
        max_tokens=600,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    insta_hashtags = response.choices[0].message.content.strip()

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
            "role": "system",
            "content": "You are a helpful social media content writer.\n"
            },
            {
            "role": "user",
            "content": f"Generate 15 relevant Facebook hashtags for:\n{facebook_post}\n\nHashtags:",

            }
        ],
        temperature=1,
        max_tokens=600,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    facebook_hashtags = response.choices[0].message.content.strip()

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
            "role": "system",
            "content": "You are a helpful social media content writer.\n"
            },
            {
            "role": "user",
            "content": f"Generate 5 relevant Twitter hashtags for:\n{twitter_post}\n\nHashtags:",

            }
        ],
        temperature=1,
        max_tokens=600,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    twitter_hashtags = response.choices[0].message.content.strip()


    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
            "role": "system",
            "content": "You are a helpful social media content writer.\n"
            },
            {
            "role": "user",
            "content": f"Generate relevant Instagram locations for:\n{instagram_post}\n\nLocations:",

            }
        ],
        temperature=1,
        max_tokens=600,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    locations = response.choices[0].message.content.strip()

    return jsonify({
        "instagram_post": instagram_post,
        "insta_hashtag": insta_hashtags,
        "insta_locations": locations,
        "facebook_post": facebook_post,
        "fb_hashtags": facebook_hashtags,
        "twitter_post": twitter_post,
        "x_hashtags": twitter_hashtags
    })

    # # Generate relevant users to tag using ChatGPT
    # users_response = openai.Completion.create(
    #     engine="text-davinci-002",
    #     prompt=f"Generate relevant Instagram users to tag for:\n{post_content}\n\nUsers:",
    #     max_tokens=60  # You can adjust this number as needed
    # )

    # users_to_tag = users_response.choices[0].text.strip().split('\n')

    #return jsonify({"content": post_content, "hashtags": hashtags, "locations": locations, "users_to_tag": users_to_tag})

    #return jsonify({"content": post_content, "hashtags": '', "locations": "", "users_to_tag": ""})


if __name__ == '__main__':
    app.run(debug=True, port=port)
