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
    url = "https://html.duckduckgo.com/html/"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    data = {"q": query}
    
    response = requests.post(url, headers=headers, data=data)
    soup = BeautifulSoup(response.text, "html.parser")
    
    results = []
    
    for result in soup.find_all("div", class_="result")[:num_results]:
        title_tag = result.find("a", class_="result__a")
        snippet_tag = result.find("a", class_="result__snippet")
        
        if title_tag:
            results.append({
                "title": title_tag.get_text(),
                "link": title_tag.get("href"),
                "snippet": snippet_tag.get_text() if snippet_tag else ""
            })
    
    return results


@app.get("/search", response_model=list[SearchResponse])
def search(
    query: str = Query(..., description="Search query"),
    limit: int = Query(10, description="Number of results")
):
    return web_search(query, limit)