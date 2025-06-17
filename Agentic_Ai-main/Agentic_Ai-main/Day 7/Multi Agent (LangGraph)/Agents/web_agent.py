import requests
from bs4 import BeautifulSoup

def web_node(state):
    query = state["query"]
    print("🌐 Fetching web data for:", query)

    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')

    texts = [r.get_text() for r in results[:5]]
    return {**state, "web_result": "\n".join(texts)}
