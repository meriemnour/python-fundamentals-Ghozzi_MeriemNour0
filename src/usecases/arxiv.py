import requests

url = "http://export.arxiv.org/api/query"


def fetch_arxiv_articles() -> None:
    params = {
        "search_query": "all:electron",
        "start": 0,
        "max_results": 10,
    }
    response = requests.get(url, params=params)
    xml_data = response.text
    with open("data/arwiv_articles.xml", "w", encoding="utf-8") as f:
        f.write(xml_data)
    return xml_data


if __name__ == "__main__":
    articles_xml = fetch_arxiv_articles()
    print(articles_xml)
