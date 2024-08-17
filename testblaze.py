from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
app.config['BLAZEGRAPH_URL'] = 'http://localhost:9999'  # Replace with your Blazegraph URL

def blazegraph_request(endpoint, method='GET', data=None, headers=None):
    url = f"{app.config['BLAZEGRAPH_URL']}/{endpoint}"
    if headers is None:
        headers = {'Content-Type': 'application/sparql-update'} if method == 'POST' else {'Accept': 'application/json'}

    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json() if method == 'GET' else response.text
    else:
        response.raise_for_status()

@app.route('/create_database', methods=['POST'])
def create_database():
    database_name = request.json.get('database_name')
    if not database_name:
        return jsonify({'error': 'Database name is required'}), 400

    create_query = f"""
    PREFIX db: <http://example.org/>
    CREATE GRAPH <{database_name}>
    """

    try:
        blazegraph_request(f'sparql', method='POST', data=create_query)
        return jsonify({'message': 'Database created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return 'Hello, Flask!'

if __name__ == '__main__':
    app.run(debug=True, port=5006)  # Change to another port like 5001