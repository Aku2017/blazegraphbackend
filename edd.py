from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Blazegraph configuration
BLAZEGRAPH_URL = "http://localhost:9999/blazegraph/sparql"  # Replace with your Blazegraph SPARQL endpoint


def run_sparql_query(query):
    """
    Run a SPARQL query against the Blazegraph database.
    """
    headers = {
        "Accept": "application/sparql-results+json"  # This is for SELECT queries
    }
    response = requests.post(BLAZEGRAPH_URL, data={"query": query}, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


@app.route('/')
def index():
    return 'Welcome to the Blazegraph Flask App!'


@app.route('/query', methods=['POST'])
def query_blazegraph():
    sparql_query = request.json.get('query')
    try:
        results = run_sparql_query(sparql_query)
        return jsonify(results)
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run(debug=True)
