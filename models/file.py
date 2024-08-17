from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base  # Import Base from a common module (explained below)

class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String, nullable=False)
    graph_id = Column(String, nullable=False)

    # ForeignKey to associate File with a Namespace (optional)
    namespace_id = Column(Integer, ForeignKey('namespaces.id'), nullable=True)
    namespace = relationship("Namespace", back_populates="files")
