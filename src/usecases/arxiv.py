from xml.etree import ElementTree as ET
from typing import Any

import pandas as pd
import requests


def fetch_arxiv_articles(search_query: str, max_results: int = 10) -> pd.DataFrame:
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,  
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    articles_data: list[dict[str, Any]] = []
    namespace = {"atom": "http://www.w3.org/2005/Atom"}

    for entry in root.findall("atom:entry", namespace):
        arxiv_id_elem = entry.find("atom:id", namespace)
        title_elem = entry.find("atom:title", namespace)
        summary_elem = entry.find("atom:summary", namespace)

        arxiv_id = arxiv_id_elem.text if arxiv_id_elem is not None else "Unknown"
        title = title_elem.text if title_elem is not None else "No title"
        summary = summary_elem.text if summary_elem is not None else "No summary"

        author_elem = entry.find("atom:author", namespace)
        if author_elem is not None:
            name_elem = author_elem.find("atom:name", namespace)
            author_name = name_elem.text if name_elem is not None else "Unknown"
        else:
            author_name = "Unknown"

        pdf_link = None
        for link in entry.findall("atom:link", namespace):
            if link.get("type") == "application/pdf":
                pdf_link = link.get("href")
                break

        articles_data.append(
            {
                "arxiv_id": arxiv_id,
                "title": title,
                "summary": summary,
                "author_full_name": author_name,
                "author_title": "PhD",
                "file_path": pdf_link if pdf_link else "",
            }
        )

    df = pd.DataFrame(articles_data).astype("string")
    return df


if __name__ == "__main__":
    df = fetch_arxiv_articles("quantum", max_results=5)
    print(df.head())
