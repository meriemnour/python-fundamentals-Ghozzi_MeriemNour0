from models.relational import Author, ScientificArticle  # noqa: F401
from storage.relational_db import Base, engine

Base.metadata.create_all(engine)
