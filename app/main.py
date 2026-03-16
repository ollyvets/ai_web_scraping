import asyncio
from app.agents.orchestrator import MarketMindAgent
from app.utils.exporter import export_to_csv

async def main():
    print("Initializing MarketMind Agent...")
    agent = MarketMindAgent()
    
    # test prompt - what kind of leads we want to find
    target = "Find B2B marketing agencies in Berlin that focus on tech startups"
    
    # run the AI pipeline
    leads = await agent.run(target)
    
    # export results
    if leads:
        print("\nPipeline finished! Exporting data...")
        status = export_to_csv(leads, "berlin_agencies_report.csv")
        print(status)
    else:
        print("\nNo valid leads were generated.")

if __name__ == "__main__":
    # execute async loop
    asyncio.run(main())