import scholarly

def get_scholar_data(query: str, num_results: int = 50) -> list:
    """
    Fetches scholarly articles based on a query string.
    Args:
        query (str): The search query for Google Scholar.
        num_results (int): The maximum number of results to return.
    Returns:
        list: A list of dictionaries containing article details.
    """
    # Search for articles using the provided query
    search_query = scholarly.search_pubs(query)
    
    # Extract relevant information from the results
    papers = []
    for i, result in enumerate(search_query):
        if i >= num_results:
            break
        paper_info = {
            'title': result.bib['title'],
            'authors': result.bib['author'],
            'abstract': result.bib.get('abstract', ''),
            'year': result.bib.get('year', ''),
            'url': result.bib.get('url', '')
        }
        papers.append(paper_info)

    return papers