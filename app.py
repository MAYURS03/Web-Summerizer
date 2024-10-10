from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = 'Open Ai Key'  # Replace with your actual OpenAI API key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    url = data.get('url')
    summary_length = data.get('length', 'medium')
    summary_format = data.get('format', 'paragraph')

    # Fetch the webpage
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to retrieve webpage"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Parse the page content
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    text_content = ' '.join([para.get_text() for para in paragraphs])

    if len(text_content) > 2048:
        text_content = text_content[:2048]  # Limit input text size

    # Customize OpenAI prompt
    prompt = f"Summarize this text in a {summary_length} format using {summary_format}:\n\n{text_content}"

    try:
        # Summarize the text using OpenAI API
        openai_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        summary = openai_response.choices[0].text.strip()

        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": "Failed to generate summary."}), 500

if __name__ == '__main__':
    app.run(debug=True)
