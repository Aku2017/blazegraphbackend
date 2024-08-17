from flask import Flask, jsonify
import requests

app = Flask(__name__)

# In-memory store for connection details
connection_details = {
    'ipAddress': '192.168.0.195',  # Example values
    'port': '9999'
}


@app.route('/database_info', methods=['GET'])
def get_database_info():
    print("Fetching database info...")  # Debug statement

    # Fetch the IP address and port number from connection details
    ip_address = connection_details.get('ipAddress')
    port_number = connection_details.get('port')

    print(f"IP Address: {ip_address}, Port: {port_number}")  # Debug statement

    # Construct the Blazegraph status URL
    blazegraph_status_url = f'http://{ip_address}:{port_number}/blazegraph/status'

    print(f"Blazegraph Status URL: {blazegraph_status_url}")  # Debug statement

    try:
        # Make a GET request to the Blazegraph status endpoint
        response = requests.get(blazegraph_status_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Parse the JSON response
        status_data = response.json()

        print(f"Status Data: {status_data}")  # Debug statement

        # Construct the database info response
        database_info = {
            'databaseType': 'blazegraph',
            'ipAddress': ip_address,
            'port': port_number,
            'status': {
                "runningQueriesCount": status_data.get('runningQueriesCount', 0),
                "deadlineQueueSize": status_data.get('deadlineQueueSize', 0),
                "queryPerSecond": status_data.get('queryPerSecond', 0),
                "queryErrorCount": status_data.get('queryErrorCount', 0),
                "operatorActiveCount": status_data.get('operatorActiveCount', 0),
                "operatorStartCount": status_data.get('operatorStartCount', 0),
                "queryStartCount": status_data.get('queryStartCount', 0),
                "queryDoneCount": status_data.get('queryDoneCount', 0),
                "operatorTasksPerQuery": status_data.get('operatorTasksPerQuery', 0),
                "operatorHaltCount": status_data.get('operatorHaltCount', 0)
            }
        }
        return jsonify(database_info)

    except requests.exceptions.RequestException as e:
        # Handle request-related errors
        return jsonify({'error': f'Failed to fetch database status: {str(e)}'}), 500



@app.route('/databaseinfo', methods=['GET'])
def get_database_info_ed():
    ip_address = connection_details.get('ipAddress')
    port_number = connection_details.get('port')

    # Use a specific namespace and a SPARQL query
    namespace = 'kb'  # Replace with your actual namespace
    sparql_query = 'SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o }'  # Example query
    blazegraph_status_url = f'http://{ip_address}:{port_number}/blazegraph/namespace/{namespace}/sparql?query={requests.utils.quote(sparql_query)}'

    try:
        response = requests.get(blazegraph_status_url)
        response.raise_for_status()  # Raise an error for HTTP error responses

        # Log the response text for debugging
        print('Response Text:', response.text)

        # Attempt to parse the response as JSON
        try:
            status_data = response.json()
        except ValueError:
            return jsonify({'error': 'Received non-JSON response from Blazegraph'}), 500

        database_info = {
            'databaseType': 'blazegraph',
            'ipAddress': ip_address,
            'port': port_number,
            'status': status_data  # Include relevant fields from your response
        }
        return jsonify(database_info)
    except requests.RequestException as e:
        return jsonify({'error': f'Failed to fetch database status: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5009)
