from resources import fetch_ncert_online
from vectorstore import search_vectorstore

def build_context(topic):
    subject = "physics"
    class_num = 9
    chapter_name = "motion"  
    ncert_text = fetch_ncert_online(subject, class_num, chapter_name)
    vs_context = search_vectorstore(topic)
    context = ncert_text + "\n\n" + "\n\n".join(vs_context)
    return context