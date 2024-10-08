from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

app = Flask(__name__)

# Load a pre-trained summarization model
summarizer = pipeline("summarization")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    url = request.json.get('url')
    
    # Fetch the web page
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to retrieve webpage"}), 400
    
    # Parse the web page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the main content (This can be more complex depending on the website structure)
    paragraphs = soup.find_all('p')
    text_content = ' '.join([para.get_text() for para in paragraphs])
    
    # Summarize the extracted text
    if len(text_content) > 1024:
        summary = summarizer(text_content[:1024], max_length=150, min_length=40, do_sample=False)[0]['summary_text']
    else:
        summary = summarizer(text_content, max_length=150, min_length=40, do_sample=False)[0]['summary_text']
    
    return jsonify({"summary": summary})

if __name__ == '__main__':
    app.run(debug=True)
