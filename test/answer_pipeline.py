from flask import Flask, request, jsonify
import requests, re
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

app = Flask(__name__)

MAX_PAGES = 5
MIN_WORDS = 6
MAX_WORDS = 30
HEADERS = {"User-Agent": "EchoSearchBot/1.0"}

def normalize(text):
    return re.sub(r"[^\w\s]", "", text.lower()).strip()

def valid_sentence(s, query):
    words = s.split()
    if not (MIN_WORDS <= len(words) <= MAX_WORDS):
        return False
    bad_starts = ("this", "it", "they", "these", "those", "he", "she")
    if s.lower().startswith(bad_starts):
        return False
    if any(w in s.lower() for w in ["may", "might", "often", "generally", "usually"]):
        return False
    return normalize(query) in normalize(s)

def search_web(query):
    url = f"https://duckduckgo.com/html/?q={quote_plus(query)}"
    r = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    links = [a["href"] for a in soup.select("a.result__a")[:MAX_PAGES]]
    return links

def extract_sentences(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script","style","noscript"]):
            tag.decompose()
        text = " ".join(soup.get_text().split())
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return sentences
    except:
        return []

def find_answer(query):
    urls = search_web(query)
    candidates = []

    for url in urls:
        sentences = extract_sentences(url)
        for s in sentences:
            if valid_sentence(s, query):
                candidates.append({"text": s.strip(), "url": url})

    # Deduplicate
    seen = set()
    unique = []
    for c in candidates:
        key = normalize(c["text"])
        if key not in seen:
            seen.add(key)
            unique.append(c)

    # Multi-source confirmation
    for c in unique:
        count = sum(1 for o in unique if normalize(o["text"]) == normalize(c["text"]))
        if count >= 2:
            return c
    return None

@app.route("/api/search")
def api_search():
    q = request.args.get("q","")
    answer = find_answer(q)
    if answer:
        return jsonify({"found": True, "text": answer["text"], "url": answer["url"]})
    else:
        return jsonify({"found": False})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
