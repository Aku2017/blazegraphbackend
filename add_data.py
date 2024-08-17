import requests

BLAZEGRAPH_URL = "http://localhost:9999/blazegraph/sparql"  # Replace with your Blazegraph SPARQL endpoint


def add_data():
    sparql_update = """
    PREFIX ex: <http://example.org/>

    INSERT DATA {
        ex:subject1 ex:predicate1 "object1" .
        ex:subject2 ex:predicate2 "object2" .
    }
    """

    headers = {
        "Content-Type": "application/sparql-update"
    }

    response = requests.post(BLAZEGRAPH_URL, data=sparql_update, headers=headers)

    if response.status_code == 204:
        print("Data added successfully!")
    else:
        print(f"Failed to add data. Status code: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    add_data()
