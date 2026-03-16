from crawl4ai import AsyncWebCrawler

async def scrape_website(url: str) -> str:
    """
    Visits a target website and extracts all text content, converting it into Markdown format.
    This format is highly optimized for passing context to LLMs like Gemini.
    
    Args:
        url (str): The URL of the target company's website.
        
    Returns:
        str: The website's text content formatted as Markdown.
    """
    # Initialize the asynchronous web crawler (verbose=False keeps logs clean)
    async with AsyncWebCrawler(verbose=False) as crawler:
        # Execute the asynchronous crawling process
        result = await crawler.arun(url=url)
        
        # Fallback message in case the crawler is blocked or fails to parse content
        if not result.markdown:
            return f"Failed to extract content from the website: {url}. It might be protected or empty."
            
        return result.markdown