import os
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from transformers import pipeline
from .utils.pdf_loader import load_pdfs_and_split

BASE = Path(__file__).resolve().parent
EMB_DIR = BASE.parent / 'embeddings'
EMB_DIR.mkdir(parents=True, exist_ok=True)
META_PATH = EMB_DIR / 'metadata.json'
INDEX_PATH = EMB_DIR / 'faiss.index'

class AINcertEngine:
    def __init__(self, embed_model_name='sentence-transformers/all-MiniLM-L6-v2', qa_model_name='distilbert-base-cased-distilled-squad'):
        print('Loading embedding model...')
        self.embedder = SentenceTransformer(embed_model_name)
        print('Loading QA pipeline...')
        self.qa = pipeline('question-answering', model=qa_model_name, tokenizer=qa_model_name)

        if INDEX_PATH.exists() and META_PATH.exists():
            self._load_index()
        else:
            self._build_index()

    def _build_index(self):
        print('Building embeddings index from PDFs...')
        docs = load_pdfs_and_split()
        texts = [d['text'] for d in docs]
        metas = [d['meta'] for d in docs]

        emb = self.embedder.encode(texts, show_progress_bar=True, convert_to_numpy=True)

        dim = emb.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(emb)

        faiss.write_index(index, str(INDEX_PATH))
        with open(META_PATH, 'w', encoding='utf-8') as f:
            json.dump({'docs': docs}, f)

        self.index = index
        self.docs = docs
        print('Index built. Saved to disk.')

    def _load_index(self):
        print('Loading FAISS index and metadata...')
        index = faiss.read_index(str(INDEX_PATH))
        with open(META_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.index = index
        self.docs = data['docs']
        print(f'Loaded {len(self.docs)} document chunks.')

    def _embed_query(self, query):
        return self.embedder.encode([query], convert_to_numpy=True)

    def retrieve(self, query, top_k=5):
        q_emb = self._embed_query(query)
        D, I = self.index.search(q_emb, top_k)
        results = []
        for idx in I[0]:
            if idx < len(self.docs):
                results.append(self.docs[idx])
        return results

    def answer_question(self, question, top_k=3):
        contexts = self.retrieve(question, top_k=top_k)
        combined_context = "\n\n".join([c['text'] for c in contexts])

        qa_input = {
            'question': question,
            'context': combined_context
        }
        res = self.qa(qa_input)
        answer = res.get('answer', '')

        source_contexts = [{'meta': c['meta'], 'text': c['text'][:500]} for c in contexts]
        return answer, source_contexts