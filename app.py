# app.py

import streamlit as st
from apis.semantic_scholar import fetch_papers_from_sematic_scholar
from apis.pubmed import fetch_papers_from_pubmed
from apis.core_api import fetch_papers_from_core
from models.summariser import load_summarizer
from models.utils import chunk_text, save_summary_to_pdf

# App title
st.set_page_config(page_title="Research Agent", layout="wide")
st.title("📚 Research Agent – Summarize Academic Papers")

# Source selection
source = st.selectbox("Select Source", ["Semantic Scholar", "PubMed", "CORE"])

query = st.text_input("Enter your search query")

# Search trigger
if st.button("Search"):
    st.info("Fetching papers...")
    
    if source == "Semantic Scholar":
        papers = fetch_papers_from_sematic_scholar(query)
    elif source == "PubMed":
        papers = fetch_papers_from_pubmed(query)
    elif source == "CORE":
        papers = fetch_papers_from_core(query)
    else:
        papers = []

    if not papers:
        st.warning("No papers found.")
    else:
        titles = [paper["title"] for paper in papers]
        selected_title = st.selectbox("Select a paper to summarize", titles)
        selected_paper = next(p for p in papers if p["title"] == selected_title)

        if st.button("Generate Summary"):
            st.info("Loading summarizer...")
            summarizer = load_summarizer()

            text = selected_paper["content"]
            chunks = chunk_text(text)

            st.info("Summarizing...")
            summary = ""
            for i, chunk in enumerate(chunks):
                result = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
                summary += result[0]["summary_text"] + "\n\n"

            st.success("Summary generated!")

            # Display summary
            st.subheader("🔍 Summary")
            st.write(summary)

            # Save summary files
            save_summary_to_pdf(summary, selected_title)

            # Download buttons
            pdf_path = f"data/summaries/{selected_title.replace(' ', '_')[:50]}.pdf"
            txt_path = f"data/summaries/{selected_title.replace(' ', '_')[:50]}.txt"

            with open(pdf_path, "rb") as f:
                st.download_button("Download PDF", f, file_name="summary.pdf")

            with open(txt_path, "rb") as f:
                st.download_button("Download Text", f, file_name="summary.txt")
