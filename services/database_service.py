from sqlalchemy.orm import Session
from models.database import Database
from models.namespace import Namespace
from models.file import File

class DatabaseService:
    def __init__(self, session: Session):
        self.session = session

    def create_database(self, ip_address, port_number, min_memory, max_memory, status, blazegraph_url):
        db = Database(
            ip_address=ip_address,
            port_number=port_number,
            min_memory=min_memory,
            max_memory=max_memory,
            status=status,
            blazegraph_url=blazegraph_url
        )
        self.session.add(db)
        self.session.commit()
        return db

    def add_namespace_to_database(self, namespace_name: str, blaze_url: str, db_id: int):
        namespace = Namespace(
            name=namespace_name,
            blaze_url=blaze_url,
            database_id=db_id
        )
        self.session.add(namespace)
        self.session.commit()
        return namespace

    def add_file_to_namespace(self, namespace: Namespace, file_name: str, graph_id: str):
        file = File(
            file_name=file_name,
            graph_id=graph_id,
            namespace=namespace
        )
        self.session.add(file)
        self.session.commit()
        return file

    def add_file_to_db(self, file_name: str):
        file = File(
            file_name=file_name

        )
        self.session.add(file)
        self.session.commit()
        return file

    def get_connected_database(self):
        # Query to fetch the connected database
        connected_db = self.session.query(Database).filter_by(status='Connected').first()
        if connected_db:
            return connected_db.ip_address, connected_db.port_number, connected_db.blazegraph_url, connected_db.id
        else:
            raise Exception("No connected database found")

    def find_database_by_ip(self, ip_address: str):
        """Check if a database with a specific IP address exists, and return the IP address and port number."""
        db = self.session.query(Database).filter_by(ip_address=ip_address).first()
        if db:
            return db.ip_address, db.port_number
        else:
            return None

    def update_status_by_ip(self, ip_address: str, new_status: str = "Connected"):
        """Update the status of a database to 'Connected' by using the IP address."""
        db = self.session.query(Database).filter_by(ip_address=ip_address).first()
        if db:
            db.status = new_status
            self.session.commit()
            return True
        else:
            return False

    def get_first_namespace(self):
        """Retrieve the first Namespace entry in the database."""
        first_namespace = self.session.query(Namespace).first()
        return first_namespace