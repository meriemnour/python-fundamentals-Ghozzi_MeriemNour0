from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100))
    title = Column(String(100))

    articles = relationship("ScientificArticle", back_populates="author")

    def __init__(self, full_name: str, title: str) -> None:
        self.full_name = full_name
        self.title = title


class ScientificArticle(Base):
    __tablename__ = "scientific_articles"

    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    summary = Column(String(500))
    file_path = Column(String(200))
    created_at = Column(DateTime, default=datetime.now)
    arxiv_id = Column(String(50), unique=True)

    author_id = Column(Integer, ForeignKey("authors.id"), nullable=True)
    author = relationship("Author", back_populates="articles")

    def __init__(self, title: str, summary: str, file_path: str, arxiv_id: str, author=None) -> None:
        self.title = title
        self.summary = summary
        self.file_path = file_path
        self.arxiv_id = arxiv_id
        self.author = author