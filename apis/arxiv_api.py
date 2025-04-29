import arxiv_api

def get_arxiv_papers(query: str, max_results: int = 10) -> list:
    """
    Fetches research papers from arXiv based on a query string.
    Args:
        query (str): The search query for arXiv.
        max_results (int): The maximum number of results to return.
    Returns:
        list: A list of dictionaries containing paper details.
    """
    # Search for papers using the provided query
    search = arxiv_api.Search(query=query, max_results=max_results)
    
    # Extract relevant information from the results
    papers = []
    for result in search.results():
        paper_info = {
            'title': result.title,
            'authors': [author.name for author in result.authors],
            'abstract': result.summary,
            'year': result.published.year,
            'url': result.entry_id
        }
        papers.append(paper_info)

    return papers