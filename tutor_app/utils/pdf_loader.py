import fitz # PyMuPDF
from pathlib import Path
import re

DATA_DIR = Path(__file__).resolve().parent.parent.parent / 'data' / 'ncert_pdfs'


def clean_text(t: str) -> str:
    t = t.replace('\r', '\n')
    t = re.sub(r"\n{2,}", '\n\n', t)
    t = re.sub(r"\s+", ' ', t)
    return t.strip()


def split_into_chunks(text, max_chars=800):
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    chunks = []
    cur = ''
    for p in paragraphs:
        if len(cur) + len(p) + 1 <= max_chars:
            cur = (cur + '\n' + p).strip()
        else:
            if cur:
                chunks.append(cur)
            cur = p
    if cur:
        chunks.append(cur)
    return chunks


def load_pdfs_and_split():
    docs = []
    file_id = 0
    for pdf_path in sorted(DATA_DIR.glob('*.pdf')):
        doc = fitz.open(pdf_path)
        text = ''
        for page in doc:
            text += page.get_text()
            text = clean_text(text)
            chunks = split_into_chunks(text)
        for i, c in enumerate(chunks):
            docs.append({
                'id': file_id,
                'text': c,
                'meta': {
                    'source_pdf': pdf_path.name,
                    'chunk_id': i,
                }
            })
            file_id += 1
    return docs