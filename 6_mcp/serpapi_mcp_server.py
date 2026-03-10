from mcp.server.fastmcp import FastMCP
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv(override=True)

mcp = FastMCP("serpapi-search")

@mcp.tool()
def serpapi_search(
    query: str,
    engine: str = "google",
    num_results: int = 5
):
    """
    Search the web using SerpAPI (Google, Bing, etc.)
    
    Args:
        query: The search query
        engine: Search engine to use (google, bing, etc.)
        num_results: Number of results to return (default: 5)
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return {"error": "SERPAPI_API_KEY not found in environment variables"}
    
    params = {
        "q": query,
        "engine": engine,
        "api_key": api_key,
        "num": num_results,
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    # Extract organic search results
    organic = results.get("organic_results", [])
    return [
        {
            "title": r.get("title"),
            "link": r.get("link"),
            "snippet": r.get("snippet"),
        }
        for r in organic[:num_results]
    ]

if __name__ == "__main__":
    mcp.run(transport='stdio')
