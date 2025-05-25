from flask import Flask, render_template, jsonify, request, send_from_directory
import os

app = Flask(__name__)

# Load domains from the file
def load_domains():
    domains = []
    try:
        # Corrected path to the domains.txt file
        file_path = os.path.join(os.path.dirname(__file__), 'tms-cryptlex-registration', 'Data', 'domains.txt')
        with open(file_path, 'r') as f:
            for line in f:
                domains.extend(line.strip().split(','))
    except FileNotFoundError:
        print(f"Error: domains.txt not found at {file_path}")
    return [domain.strip() for domain in domains if domain.strip()]

DOMAINS = load_domains()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search_api(): # Renamed to avoid conflict with a potential 'search' variable
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    
    results = [domain for domain in DOMAINS if query in domain.lower()]
    return jsonify(results[:5])

@app.route('/domains.txt')
def serve_domains_txt():
    directory = os.path.join(os.path.dirname(__file__), 'tms-cryptlex-registration', 'Data')
    return send_from_directory(directory, 'domains.txt')

if __name__ == '__main__':
    if not DOMAINS:
        print("No domains loaded. Please check the path to domains.txt and ensure it's not empty.")
    else:
        print(f"Loaded {len(DOMAINS)} domains.")
    app.run(debug=True)
