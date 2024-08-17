from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/create_namespace', methods=['POST'])
def create_namespace():
    data = request.get_json()
    database_type = data.get('databaseType')
    installation_path = data.get('installationPath')
    port_number = data.get('port')
    min_memory = data.get('minMemory')
    max_memory = data.get('maxMemory')
    namespace = "http://example.org/graph/JideSmith"  # Representing namespace

    if not database_type or not installation_path or not port_number:
        return jsonify({'error': 'Database type, installation path, and port number are required'}), 400

    if database_type.lower() != 'blazegraph':
        return jsonify({'error': 'Unsupported database type'}), 400

    try:
        port_number = int(port_number)
    except ValueError:
        return jsonify({'error': 'Invalid port number'}), 400

    blazegraph_url = f'http://{installation_path}:{port_number}/blazegraph/namespace'


    print(f'FIRSTull URL: {blazegraph_url}')

# Construct the query to create a graph
    create_query = f"CREATE GRAPH <{namespace}>"

    headers = {
        "Content-Type": "application/sparql-update"
    }

    # Define the payload for Blazegraph namespace creation
    payload = {
        "query": create_query,
        "config": {
            "minMemory": min_memory,
            "maxMemory": max_memory
        }
    }

    full_url = f"{blazegraph_url}/kb/sparql"
    print(f'Full URL: {full_url}')

    try:
        response = requests.post(f"{blazegraph_url}/kb/sparql", data=create_query, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Namespace created successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5007)
