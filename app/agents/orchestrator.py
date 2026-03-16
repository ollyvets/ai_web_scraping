import os
import json
import google.generativeai as genai
from app.core.search_tool import search_web
from app.core.scraper_tool import scrape_website
from rust_lib import jaccard_similarity

class MarketMindAgent:
    def __init__(self):
        # init gemini model
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        # store texts to check for duplicates later
        self.seen_texts = []

    async def run(self, user_prompt: str) -> list[dict]:
        """Main execution pipeline."""
        print(f"Target: {user_prompt}")

        # let gemini build the best search query
        query = await self._build_search_query(user_prompt)
        print(f"Search Query: {query}")

        # get links
        results = await search_web(query)
        final_report = []

        for res in results:
            url = res.get("link")
            if not url: 
                continue
            
            print(f"Scraping: {url}...")
            content = await scrape_website(url)
            if content.startswith("Failed"):
                continue

            # check for duplicates using our rust module (super fast!)
            is_dupe = False
            for seen in self.seen_texts:
                if jaccard_similarity(content, seen) > 0.85:
                    is_dupe = True
                    break
                    
            if is_dupe:
                print(f"Skipped duplicate or mirrored site: {url}")
                continue
                
            self.seen_texts.append(content)

            # analyze the valid content
            print(f"Analyzing content with Gemini...")
            analysis = await self._analyze_lead(res.get("title"), url, content)
            if analysis:
                final_report.append(analysis)

        return final_report

    async def _build_search_query(self, prompt: str) -> str:
        # ask model to convert user intent into a specific google query
        sys_prompt = f"Convert this request into a highly specific Google search query to find company websites. Return ONLY the string without quotes.\nRequest: {prompt}"
        response = await self.model.generate_content_async(sys_prompt)
        return response.text.strip()

    async def _analyze_lead(self, title: str, url: str, content: str) -> dict:
        # truncate just in case to save tokens
        safe_content = content[:15000]
        
        prompt = f"""
        Analyze this company website:
        Name: {title}
        Content: {safe_content}
        
        Find their pain points and write a personalized B2B cold sales pitch.
        Return ONLY a valid JSON object matching this schema:
        {{
            "company_name": "Name",
            "pain_points": ["point 1", "point 2"],
            "pitch": "sales pitch"
        }}
        """
        try:
            res = await self.model.generate_content_async(prompt)
            # clean up markdown tags if gemini adds them
            raw_json = res.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(raw_json)
            data["url"] = url
            return data
        except Exception as e:
            print(f"Analysis failed for {url}: {e}")
            return None