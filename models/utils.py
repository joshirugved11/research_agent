# utils.py

import os
import re
from fpdf import FPDF

def read_text_from_file(file_path):
    """Reads plain text from a file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def chunk_text(text, max_tokens=1024):
    """Split text into chunks that fit within model input limits."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_tokens):
        chunk = " ".join(words[i:i+max_tokens])
        chunks.append(chunk)
    return chunks

def save_summary_to_pdf(summary_text, filename):
    output_dir = "data/summaries"
    os.makedirs(output_dir, exist_ok=True)

    # Remove special characters from filename
    safe_filename = re.sub(r'[\\/*?:"<>|]', "_", filename)[:50] + ".pdf"
    output_path = os.path.join(output_dir, safe_filename)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    lines = summary_text.split('\n')
    for line in lines:
        pdf.multi_cell(0, 10, line)

    pdf.output(output_path)
    print(f"✅ Summary saved to {output_path}")