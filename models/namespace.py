from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base  # Import Base from a common module (explained below)

class Namespace(Base):
    __tablename__ = 'namespaces'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    blaze_url = Column(String, nullable=False)

    # ForeignKey to associate Namespace with a Database
    database_id = Column(Integer, ForeignKey('databases.id'))
    database = relationship("Database", back_populates="namespaces")

    # Relationship with File
    files = relationship("File", back_populates="namespace", cascade="all, delete-orphan")
