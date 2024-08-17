import requests

BLAZEGRAPH_URL = "http://192.168.30.195:9999/blazegraph/namespace/kb/sparql"

def insert_data(namespace):
    insert_query = f"""
    INSERT DATA {{
    GRAPH <{namespace}> {{
        <http://example.org/subject1> <http://example.org/predicate1> "object1" .
    }}
    }}
    """
    headers = {
        "Content-Type": "application/sparql-update"
    }
    response = requests.post(BLAZEGRAPH_URL, data=insert_query, headers=headers)
    if response.status_code == 200:
        print(f"Data inserted into namespace '{namespace}'.")
    else:
        raise Exception(f"Error inserting data: {response.text}")

if __name__ == "__main__":
    namespace_uri = "http://example.org/ojemba"
    insert_data(namespace_uri)
