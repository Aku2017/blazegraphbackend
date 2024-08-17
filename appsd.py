from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import subprocess

app = Flask(__name__)
CORS(app)


@app.route('/create_database', methods=['POST'])
def create_database():
    data = request.get_json()
    directory_path = data.get('installationPath')
    port_number = data.get('port')

    if not directory_path or not port_number:
        return jsonify({'error': 'Directory path and port number are required'}), 400

    try:
        port_number = int(port_number)
    except ValueError:
        return jsonify({'error': 'Invalid port number'}), 400

    print(f"Received directory path: {directory_path}")
    if not os.path.isdir(directory_path):
        return jsonify({'error': f'Directory path does not exist: {directory_path}'}), 400

    try:
        command = [
            'java', '-cp', 'C:\\Users\\Mike\\Downloads\\Db\\blazegraph.jar',
            'com.bigdata.jena.assembler.BDServer',
            '-d', directory_path,
            '-p', str(port_number)
        ]

        subprocess.run(command, check=True)

    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Database created and server started successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5007)
