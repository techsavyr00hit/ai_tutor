from sentence_transformers import SentenceTransformer
import chromadb

client = chromadb.Client()
collection = client.create_collection("ncert_chapters")
model = SentenceTransformer("all-MiniLM-L6-v2")

def add_chapter_to_vectorstore(chapter_name, text):
    embedding = model.encode(text).tolist()
    collection.add(
        documents=[text],
        metadatas={"chapter": chapter_name},
        ids=[chapter_name],
        embeddings=[embedding]
    )
def search_vectorstore(query, top_k=3):
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=['documents']
    )
    documents = results['documents'][0]  
    return documents