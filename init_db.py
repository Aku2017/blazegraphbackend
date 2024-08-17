from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.database import Database
from models.namespace import Namespace
from models.file import File
import config
from sqlalchemy import create_engine, text


def init_db():
    # Create an engine connected to the database
    from sqlalchemy import create_engine

    # Using Windows Authentication
    engine = create_engine(
        'mssql+pyodbc://@DESKTOP-THU83U5/BlazerDb?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes')

    # Now, you can proceed with using this engine in your SQLAlchemy session or ORM setup

    # Example of making a connection and executing a simple query
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print(result.fetchone())

    # Create all tables in the database
    Base.metadata.create_all(engine)

    print("Database and tables created.")


if __name__ == "__main__":
    init_db()
