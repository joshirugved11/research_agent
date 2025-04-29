from Bio import entrez

entrez.email = "rugvedsamruddhi@gmail.com"

def fetch_papers_from_pubmed(query: str, max_results: int = 10) -> list:
    handle = entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = entrez.read(handle)
    ids = record["IdList"]

    papers = []

    for pubmed_id in ids:
        fetch_handle = entrez.efetch(db="pubmed", id=pubmed_id, retmode="text")
        abstract = fetch_handle.read()
        papers.append({
            "title": f"PubMed Article {pubmed_id}",
            "content": abstract.strip(),
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/",
        })
    return papers