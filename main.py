import os
from apis.semantic_scholar import fetch_papers_from_sematic_scholar
from apis.pubmed import fetch_papers_from_pubmed
from apis.arxiv_api import get_arxiv_papers
from models.summariser import load_summarizer
from models.utils import read_text_from_file, chunk_text, save_summary_to_pdf

def save_paper_text(paper, index):
    """Save the paper content to data/papers/ and return the saved file path."""
    os.makedirs("data/papers", exist_ok=True)
    safe_title = paper['title'].replace(" ", "_").replace("/", "_")[:50]
    file_path = os.path.join("data/papers", f"{index+1}_{safe_title}.txt")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(paper['content'])
    
    return file_path

def select_source():
    print("\n📚 Choose a source:")
    print("1. Semantic Scholar")
    print("2. PubMed")
    print("3. Arxiv")
    return input("Enter choice (1/2/3): ").strip()

def main():
    choice = select_source()
    query = input("\n🔍 Enter your search query: ")

    if choice == "1":
        papers = fetch_papers_from_sematic_scholar(query)
    elif choice == "2":
        papers = fetch_papers_from_pubmed(query)
    elif choice == "3":
        papers = get_arxiv_papers(query)
    else:
        print("❌ Invalid choice.")
        return
    
    if not papers:
        print("❌ No papers found.")
        return
    
    # save fetched paper contents
    print("\n📥 Saving fetched papers...")
    paper_paths = []
    for i, paper in enumerate(papers):
        path = save_paper_text(paper, i)
        paper_paths.append({
            "title": paper["title"],
            "file_path": path
        })

    # Display list
    print("\n📄 Available Papers:")
    for i, item in enumerate(paper_paths):
        print(f"{i+1}. {item['title']}")

    try:
        selected_index = int(input("\nSelect paper to summarize (1-N): ")) - 1
        selected_paper = paper_paths[selected_index]
    except (IndexError, ValueError):
        print("❌ Invalid selection.")
        return
    
    print(f"\n⏳ Loading summarizer for: {selected_paper['title']}")
    summarizer = load_summarizer()
    text = read_text_from_file(selected_paper['file_path'])
    chunks = chunk_text(text)

    print("\n📝 Generating summary...")
    summary = ""
    for i, chunk in enumerate(chunks):
        print(f"🔹 Summarizing chunk {i+1}/{len(chunks)}...")
        result = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
        summary += result[0]['summary_text'] + "\n\n"

    print("\n✅ Summary generated!\n")

    # Save outputs
    filename = selected_paper['title']
    save_summary_to_pdf(summary, filename=filename)

if __name__ == "__main__":
    main()