import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://@DESKTOP-THU83U5/BlazerDb?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'


# Now, you can proceed with using this engine in your SQLAlchemy session or ORM setup
