import os
import requests
from sympy import limit

def fetch_papers_from_core(query: str, max_results: int = 10) -> list:
    """
    Fetches research papers from CORE based on a query string.
    Args:
        query (str): The search query for CORE.
        max_results (int): The maximum number of results to return.
    Returns:
        list: A list of dictionaries containing paper details.
    """
    API_KEY = os.getenv("CORE_API_KEY")
    url = f"https://core.ac.uk:443/api-v2/search/{query}?page=1&pageSize={limit}&apiKey={API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Error fetching from CORE:", response.text)
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