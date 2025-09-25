import requests
from bs4 import BeautifulSoup

def fetch_ncert_online(subject, class_num, chapter_name):
    try:
        url = f"https://ncert.nic.in/textbook.php?subject={subject}&class={class_num}&chapter={chapter_name}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        content = "\n".join(paragraphs).strip()
        if not content:
            return "No content found for this chapter."
        return content
    except requests.RequestException:
        return "Could not fetch NCERT chapter online."
