import arxiv

def get_arxiv_papers(query: str, max_results: int = 10) -> list:
    # Search for papers using the provided query
    search = arxiv.Search(query=query, max_results=max_results)
    
    # Extract relevant information from the results
    papers = []
    for result in search.results():
        paper_info = {
            'title': result.title,
            'authors': [author.name for author in result.authors],
            'content': result.summary,
            'year': result.published.year,
            'url': result.entry_id
        }
        papers.append(paper_info)

    return papers