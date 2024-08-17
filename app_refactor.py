from flask import Flask, request, jsonify
from rdflib import Graph
import requests

app = Flask(__name__)
app.config.from_object('config.Config')


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


@app.route('/connect', methods=['GET'])
def connect():
    try:
        # Just a basic connectivity check
        response = blazegraph_request('')
        return jsonify({'status': 'connected', 'message': response}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/create-database', methods=['POST'])
def create_database():
    db_name = request.json.get('database')
    if not db_name:
        return jsonify({'status': 'error', 'message': 'Database name is required'}), 400

    create_query = f"""
    PREFIX db: <http://example.org/>
    CREATE GRAPH <{db_name}>
    """

    try:
        result = blazegraph_request(f'sparql', method='POST', data=create_query)
        return jsonify({'status': 'success', 'message': 'Database created'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/add-namespace', methods=['POST'])
def add_namespace():
    namespace = request.json.get('namespace')
    if not namespace:
        return jsonify({'status': 'error', 'message': 'Namespace is required'}), 400

    add_namespace_query = f"""
    PREFIX db: <http://example.org/>
    CREATE GRAPH <{namespace}>
    """

    try:
        result = blazegraph_request(f'sparql', method='POST', data=add_namespace_query)
        return jsonify({'status': 'success', 'message': 'Namespace added'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500




@app.route('/upload-ttl', methods=['POST'])
def upload_ttl():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400

    if file and file.filename.endswith('.ttl'):
        try:
            # Read TTL data
            ttl_data = file.read().decode('utf-8')

            # Parse TTL data (optional, depending on API requirements)
            g = Graph()
            g.parse(data=ttl_data, format='ttl')

            # Prepare data for Blazegraph (modify as needed)
            data = g.serialize(format='turtle')  # Serialize parsed data

            headers = {'Content-Type': 'application/x-turtle'}

            response = requests.post(
                f"{app.config['BLAZEGRAPH_URL']}/namespace/{request.json.get('namespace')}/sparql?update",
                data=data,
                headers=headers
            )

            if response.status_code == 200:
                return jsonify({'status': 'success', 'message': 'TTL file uploaded successfully'}), 200
            else:
                # Check for specific error messages in response
                error_message = response.json().get('message', 'Failed to upload TTL file')
                return jsonify({'status': 'error', 'message': error_message,
                                'details': response.text}), response.status_code

        except requests.exceptions.RequestException as e:
            return jsonify({'status': 'error', 'message': f'Network error: {str(e)}'}), 500
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    else:
        return jsonify({'status': 'error', 'message': 'Invalid file type. Only .ttl files are accepted.'}), 400


@app.route('/')
def home():
    return 'Hello, Flask!'


if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change to another port like 5001
