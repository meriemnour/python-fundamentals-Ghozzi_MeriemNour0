"""Simple document processor with type hints."""

import json
from typing import List, Optional

from pydantic import BaseModel


class Document(BaseModel):
    """Simple document model."""

    id: int
    title: str
    authors: List[str]
    published: bool
    pages: Optional[int] = None
    tags: Optional[List[str]] = None


def load_documents(file_path: str) -> List[Document]:
    """Load documents from JSON file."""
    with open(file_path, "r") as file:
        data = json.load(file)

    documents: List[Document] = []
    for item in data:
        document = Document(**item)
        documents.append(document)

    return documents


def display_document_info(document: Document) -> None:
    """Display document info with missing field handling."""
    print(f"ID: {document.id}")
    print(f"Title: {document.title}")
    print(f"Authors: {', '.join(document.authors)}")
    print(f"Published: {document.published}")

    if document.pages:
        print(f"Pages: {document.pages}")
    else:
        print("Pages: Not specified")

    if document.tags:
        print(f"Tags: {', '.join(document.tags)}")
    else:
        print("Tags: None")


def main() -> None:
    """Main function to run the document processor."""
    try:
        documents = load_documents("data/documents.json")

        for doc in documents:
            print("\n" + "=" * 30)
            display_document_info(doc)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
