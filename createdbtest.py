import requests

BLAZEGRAPH_URL = "http://192.168.30.195:9999/blazegraph/namespace"

def create_namespace(namespace):
    # Define your namespace configuration here
    config = {
        "com.bigdata.rdf.sail.namespace": namespace,
        "com.bigdata.rdf.store.AbstractTripleStore.textIndex": "false",
        "com.bigdata.rdf.store.AbstractTripleStore.lexicalIV": "true",
        "com.bigdata.rdf.store.AbstractTripleStore.geoSpatial": "false",
        "com.bigdata.rdf.store.AbstractTripleStore.truthMaintenance": "false",
        "com.bigdata.rdf.store.AbstractTripleStore.justify": "false",
        "com.bigdata.namespace.class": "com.bigdata.rdf.sail.BigdataSailRepository"
    }

    headers = {"Content-Type": "application/xml"}

    response = requests.post(f"{BLAZEGRAPH_URL}/{namespace}", headers=headers, data=config)
    if response.status_code == 201:
        print(f"Namespace '{namespace}' created successfully.")
    else:
        print(f"Error creating namespace: {response.status_code} - {response.text}")

if __name__ == "__main__":
    namespace = "my_new_namespace"
    create_namespace(namespace)
