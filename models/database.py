from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base  # Import Base from a common module (explained below)

class Database(Base):
    __tablename__ = 'databases'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_address = Column(String, nullable=False)
    port_number = Column(Integer, nullable=False)
    min_memory = Column(Integer, nullable=False)
    max_memory = Column(Integer, nullable=False)
    status = Column(String, nullable=False)  # 'Connected' or 'Not Connected'
    blazegraph_url = Column(String, nullable=False)

    # Relationship with Namespace
    namespaces = relationship("Namespace", back_populates="database")
