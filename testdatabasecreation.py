import requests

BLAZEGRAPH_URL = "http://192.168.30.195:9999/blazegraph/namespace/kb/sparql/"
DATABASE_NAME = "http://example.org/Michael_ojemba"

def list_graphs():
    sparql_query = """
    SELECT DISTINCT ?g WHERE { GRAPH ?g { ?s ?p ?o } }
    """
    headers = {
        "Accept": "application/sparql-results+json",
        "Content-Type": "application/sparql-query"
    }
    response = requests.post(BLAZEGRAPH_URL, data=sparql_query, headers=headers)
    if response.status_code == 200:
        results = response.json()
        return [result['g']['value'] for result in results['results']['bindings']]
    else:
        raise Exception(f"Error retrieving graphs: {response.text}")

def check_database_exists(database_name):
    graphs = list_graphs()
    return database_name in graphs

if __name__ == "__main__":
    if check_database_exists(DATABASE_NAME):
        print(f"Database '{DATABASE_NAME}' exists")
    else:
        print(f"Database '{DATABASE_NAME}' does not exist")
