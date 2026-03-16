import os
import httpx

async def search_web(query: str, num_results: int = 5) -> list[dict]:
    """
    Performs a Google search using the Serper.dev API.
    
    Args:
        query (str): The search query (e.g., "B2B SaaS companies in London").
        num_results (int): The number of search results to return. Defaults to 5.
        
    Returns:
        list[dict]: A list of dictionaries containing organic search results (title, link, snippet).
    """
    # Retrieve the API key from Codespace secrets / environment variables
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("WARNING: SERPER_API_KEY not found in environment variables.")

    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query, 
        "num": num_results
    }

    # Asynchronously send the HTTP POST request to the Serper API
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Ensure we catch HTTP errors (e.g., 401, 403)
        
        data = response.json()
        
        # Return only the organic search results, filtering out ads and other noise
        return data.get("organic", [])