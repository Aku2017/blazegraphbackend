import requests

BLAZEGRAPH_URL = "http://192.168.30.195:9999/blazegraph/namespace/kb/sparql"

def create_namespace(namespace):
    create_query = f"CREATE GRAPH <{namespace}>"
    headers = {
        "Content-Type": "application/sparql-update"
    }
    response = requests.post(BLAZEGRAPH_URL, data=create_query, headers=headers)
    # Parse the JSON response

    if response.status_code == 200:
        print(f"Namespace '{namespace}' created successfully.")
    else:
        raise Exception(f"Error creating namespace: {response.text}")

if __name__ == "__main__":
    namespace_uri = "http://example.org/sola"
    create_namespace(namespace_uri)
