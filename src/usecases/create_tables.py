from models.relational import  ScientificArticle , Author # noqa: F401
from storage.relational_db import Base, engine

Base.metadata.create_all(engine)
