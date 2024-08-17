import requests

BLAZEGRAPH_URL = "http://192.168.30.195:9999/blazegraph/namespace/kb/sparql"

def list_graphs():
    sparql_query = """
    SELECT DISTINCT ?g WHERE { GRAPH ?g { ?s ?p ?o } } LIMIT 100
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

if __name__ == "__main__":
    graphs = list_graphs()
    print("Namespaces in Blazegraph:")
    for graph in graphs:
        print(graph)
