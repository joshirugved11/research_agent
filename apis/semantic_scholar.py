import requests
from sympy import limit

def fetch_papers_from_sematic_scholar(query: str, max_results: int = 10) -> list:
    """
    Fetches research papers from Semantic Scholar based on a query string.
    Args:
        query (str): The search query for Semantic Scholar.
        max_results (int): The maximum number of results to return.
    Returns:
        list: A list of dictionaries containing paper details.
    """
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit={limit}&fields=title,abstract,url"
    response = requests.get(url)
    if response.status_code != 200:
        print("Error fetching from Semantic Scholar:", response.text)
        return []

    data = response.json()
    return [
        {
            "title": paper["title"],
            "content": paper.get("abstract", "No abstract available."),
            "url": paper["url"]
        }
        for paper in data.get("data", [])
    ]    
