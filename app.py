from flask import Flask, render_template, request, jsonify
from scraper import scrape_url
from auditor import audit_content

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/audit', methods=['POST'])
def audit():
    data = request.json
    text = data.get('text', '')
    url = data.get('url', '')
    
    if url:
        print(f"Fetching URL: {url}")
        text = scrape_url(url)
        if text.startswith("Error fetching URL"):
            return jsonify({"error": text}), 400
            
    if not text:
        return jsonify({"error": "No text provided"}), 400
        
    print("Running audit...")
    result = audit_content(text)
    
    # Return both the result and the text (in case it was scraped)
    return jsonify({
        "result": result,
        "full_text": text
    })

if __name__ == '__main__':
    app.run(debug=True, port=8080)
