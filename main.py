from fastapi import FastAPI, Query
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI(
    title="Web Search API",
    description="Lightweight DuckDuckGo-based search API for real-time results",
    version="1.0.0"
)

class SearchResponse(BaseModel):
    title: str
    link: str
    snippet: str


def web_search(query: str, num_results: int = 10):
    try:
        url = "https://html.duckduckgo.com/html/"
        
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        
        
        params = {"q": query}
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        # ✅ Check status
        if response.status_code != 200:
            return [{"error": "Failed to fetch results"}]

        soup = BeautifulSoup(response.text, "html.parser")
        
        results = []
        
        for result in soup.find_all("div", class_="result")[:num_results]:
            title_tag = result.find("a", class_="result__a")
            snippet_tag = result.find("a", class_="result__snippet")
            
            if not title_tag:
                continue
            
            title = title_tag.get_text(strip=True)
            link = title_tag.get("href", "")
            snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
            
            results.append({
                "title": title,
                "link": link,
                "snippet": snippet
            })
        
        return results if results else [{"message": "No results found"}]

    except Exception as e:
        return [{"error": str(e)}]


@app.get("/search")
def search(query: str, limit: int = 10):
    try:
        return web_search(query, limit)
    except Exception as e:
        return {"error": str(e)}
     
