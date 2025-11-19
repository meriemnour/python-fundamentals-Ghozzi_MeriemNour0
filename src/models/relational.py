from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from storage.relational_db import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100))
    title: Mapped[str] = mapped_column(String(100))

    articles: Mapped[List["ScientificArticle"]] = relationship(
        "ScientificArticle", back_populates="author"
    )


class ScientificArticle(Base):
    __tablename__ = "scientific_articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    summary: Mapped[str] = mapped_column(String(500))
    file_path: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    arxiv_id: Mapped[str] = mapped_column(String(50), unique=True)

    author_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("authors.id"), nullable=True
    )
    author: Mapped[Optional["Author"]] = relationship(
        "Author", back_populates="articles"
    )
