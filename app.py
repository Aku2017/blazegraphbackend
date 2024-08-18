from flask import Flask,request, jsonify
from prometheus_client import Counter, Gauge, Histogram
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import database, namespace, file
from services.database_service import DatabaseService
import requests
import subprocess
import os
import time
import socket
import tempfile
from dotenv import load_dotenv
from flask_cors import CORS



app = Flask(__name__)
CORS(app)


# Load .env file and environment variables
load_dotenv()

ENV = os.getenv('ENV')

# Set the IP address based on the environment
if ENV == "test":
    ip = "localhost"
elif ENV == "prod":
    ip = "102.37.137.65"
else:
    ip = "default_ip"

app.config['SERVER_NAME'] = ip

# Configure your database
# DATABASE_URI = 'mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server'
engine = create_engine(
    'mssql+pyodbc://@DESKTOP-THU83U5/BlazerDb?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes')

# engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Initialize services
database_service = DatabaseService(session)





# In-memory store for connection details
connection_details = {
    'ipAddress': None,
    'port': None
}

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'ttl'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/create_database', methods=['POST'])
def create_database():
    # Extract data from the request
    data = request.get_json()

    # Access specific fields from the parsed data
    installation_path = data.get('installationPath')
    port_number = data.get('port')

    # Validate required fields
    if not installation_path or not port_number:
        return jsonify({'error': 'Installation path and port number are required'}), 400

    # Check if the installation path exists
    if not os.path.exists(installation_path):
        return jsonify({'error': 'Directory path does not exist'}), 400

    # Path to blazegraph.jar
    jar_path = os.path.join(installation_path, 'blazegraph.jar')
    if not os.path.isfile(jar_path):
        return jsonify({'error': f'blazegraph.jar not found in {installation_path}'}), 400

    # Get the IP address of the server
    ip_address = socket.gethostbyname(socket.gethostname())

    print("ip address", ip_address)

    # Construct the command to start Blazegraph with the specified port
    command = [
        'java', '-server', '-Xmx4g', f'-Djetty.port={port_number}', '-jar', jar_path
    ]

    try:
        # Start the Blazegraph server
        process = subprocess.Popen(command, cwd=installation_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for a few seconds to let the server start
        time.sleep(5)

        # Check if the server started by checking if the process is still running
        if process.poll() is not None:
            stderr = process.stderr.read().decode('utf-8')
            return jsonify({'error': f'Failed to start Blazegraph server: {stderr}'}), 500

        # Construct the full Blazegraph URL
        blazegraph_url = f"http://{ip_address}:{port_number}/blazegraph"

        connection_details['ipAddress'] = ip_address
        connection_details['port'] = port_number

        data = request.get_json()
        db = database_service.create_database(
            ip_address=ip_address,
            port_number=port_number,
            min_memory=data['minMemory'],
            max_memory=data['maxMemory'],
            blazegraph_url=blazegraph_url,
            status="Not Connected"
        )
        print(blazegraph_url)
        # Return a message with the clickable URL
        return jsonify({
            'message': f'Blazegraph server started successfully.',
            'url': blazegraph_url,
            'click_here': f'<a href="{blazegraph_url}">Click here to access Blazegraph</a>'
        }), 200


    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/connect_database', methods=['POST'])
def connect_database():
    data = request.get_json()
    ip_address = data.get('ipAddress')
    port_number = data.get('port')

    # Validate required fields
    if not ip_address or not port_number:
        return jsonify({'error': 'IP address and port number are required'}), 400

    connection_details['ipAddress'] = ip_address
    connection_details['port'] = port_number

    # Construct the Blazegraph URL
    # blazegraph_url = f'http://{ip_address}:{port_number}/blazegraph'

    blazegraph_url = f'http://{ip_address}:{port_number}/blazegraph'
    print('blazegraphurl', blazegraph_url)

    connect_ip_address, connect_port = database_service.find_database_by_ip(ip_address)
    update_status = database_service.update_status_by_ip(ip_address,"Connected")

    # Redirect the user to the Blazegraph URL or return it
    return jsonify({'message': 'Connected to Blazegraph database', 'url': blazegraph_url}), 200


# Route for creating a namespace to an existing Blazegraph database
@app.route('/create_namespacenew', methods=['POST'])
def create_new_namespace():
    data = request.get_json()
    namespace_name = data.get('namespace')
    print("my namespace", namespace_name)
    # namespace = "http://example.org/sola"
    create_query = f"CREATE GRAPH <{namespace_name}>"
    headers = {
        "Content-Type": "application/sparql-update"
    }

    ip_address, port_number, blazegraph_url, id = database_service.get_connected_database()

    blazegraph_url = f'http://{ip_address}:{port_number}/blazegraph'
    print('blazegraphurl', blazegraph_url)
    namespace = database_service.add_namespace_to_database(
        namespace_name=namespace_name,
        blaze_url=blazegraph_url,
        db_id=id
    )

    # ip_address = connection_details.get('ipAddress')
    # port_number = connection_details.get('port')
    # blazegraph_url = f'http://{ip_address}:{port_number}/blazegraph/'
    # blazegraph_url = "http://127.0.0.1:9999/blazegraph/namespace/kb/sparql"
    response = requests.post(blazegraph_url, data=create_query, headers=headers)
    # Parse the JSON response
    namespace_data = {
        'name': namespace_name,
        'url': f'{blazegraph_url}/namespace/{namespace_name}/sparql'
    }
    return jsonify(namespace_data), 201



@app.route('/database_info', methods=['GET'])
def get_database_info():
    ip_address = connection_details.get('ipAddress')
    port_number = connection_details.get('port')
    try:
        # Assuming the Blazegraph status can be fetched from a status endpoint
        # Replace with actual URL and endpoint if needed
        blazegraph_status_url = f'http://{ip_address}:{port_number}/blazegraph/status'

        # Fetch status data (e.g., using requests)
        # response = requests.get(blazegraph_status_url)
        # if response.status_code != 200:
        #     return jsonify({'error': 'Unable to fetch database status'}), 500
        #
        # status_data = response.json()  # Assuming the data is in JSON format
        # print("statusdata", status_data)

        # Construct the database info response
        database_info = {
            "databaseType": "Blazegraph",
            "ipAddress": ip_address,  # You might want to make this dynamic
            "port": port_number,  # This might also be dynamic
            "status":  {
                     "runningQueriesCount": 0,
                     "deadlineQueueSize":  0,
                     "queryPerSecond": 0,
                     "queryErrorCount": 0,
                     "operatorActiveCount": 0,
                     "operatorStartCount": 0,
                     "queryStartCount": 0,
                     "queryDoneCount": 0,
                     "operatorTasksPerQuery": 0,
                     "operatorHaltCount": 0
            }
            # "status": {
            #     "runningQueriesCount": status_data.get('runningQueriesCount', 0),
            #     "deadlineQueueSize": status_data.get('deadlineQueueSize', 0),
            #     "queryPerSecond": status_data.get('queryPerSecond', 0),
            #     "queryErrorCount": status_data.get('queryErrorCount', 0),
            #     "operatorActiveCount": status_data.get('operatorActiveCount', 0),
            #     "operatorStartCount": status_data.get('operatorStartCount', 0),
            #     "queryStartCount": status_data.get('queryStartCount', 0),
            #     "queryDoneCount": status_data.get('queryDoneCount', 0),
            #     "operatorTasksPerQuery": status_data.get('operatorTasksPerQuery', 0),
            #     "operatorHaltCount": status_data.get('operatorHaltCount', 0)
            # }
        }

        return jsonify(database_info), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/import_file', methods=['POST'])
def import_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    print("See file",file)
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Ensure the file is a .ttl file
    if not file.filename.lower().endswith('.ttl'):
        return jsonify({'error': 'Only .ttl files are allowed'}), 400

    # Save the file to a temporary location
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.ttl')
    file.save(temp_file.name)

    try:

        # namespace = database_service.get_first_namespace();
        # Load the file into Blazegraph
        ip_address = connection_details.get('ipAddress')
        port_number = connection_details.get('port')
        blazegraph_url = f'http://{ip_address}:{port_number}/blazegraph/namespace/kb/sparql'

        # Read the file content
        with open(temp_file.name, 'r') as f:
            ttl_data = f.read()

        # Construct the SPARQL LOAD query
        load_query = f"""
        INSERT DATA {{
            {ttl_data}
        }}
        """

        headers = {
            'Content-Type': 'application/sparql-update'
        }
        response = requests.post(blazegraph_url, data=load_query, headers=headers)

        if response.status_code == 200:
            return jsonify({'message': 'File imported successfully'}), 200
        else:
            return jsonify({'error': 'Failed to import file'}), response.status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(temp_file.name)  # Clean up the temporary file



if __name__ == '__main__':
    app.run(debug=True, port=5009)
