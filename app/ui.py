import streamlit as st
import asyncio
import pandas as pd
from app.agents.orchestrator import MarketMindAgent
from app.utils.exporter import export_to_csv

# Configure the Streamlit page layout and title
st.set_page_config(page_title="MarketMind AI", page_icon="🤖", layout="wide")

st.title("🤖 MarketMind: Lead Intelligence Agent")
st.markdown("""
Welcome to MarketMind! Enter your target audience parameters below. 
The AI will autonomously search the web, scrape competitor/prospect websites, 
filter out duplicates using Rust, and generate personalized B2B sales pitches.
""")

st.divider()

# UI Layout: Create two columns for user inputs
col1, col2 = st.columns(2)

with col1:
    # Input for the specific niche or industry
    niche = st.text_input(
        "🎯 Target Niche / Industry", 
        value="B2B marketing agencies for tech startups",
        help="E.g., Fintech startups, Real estate agencies, Healthcare SaaS"
    )

with col2:
    # Input for the geographical location
    region = st.text_input(
        "🌍 Target Region (City or Country)", 
        value="Berlin, Germany",
        help="E.g., London, New York, DACH region"
    )

st.divider()

# Button to trigger the AI agent
if st.button("🚀 Generate AI Leads Report", type="primary", use_container_width=True):
    # Combine inputs into the final prompt for the agent
    target_prompt = f"Find {niche} in {region}"
    
    # Display a loading spinner while the async pipeline runs
    with st.spinner(f"Agent is working... Target: {target_prompt}"):
        try:
            # Initialize the agent and run the async pipeline
            agent = MarketMindAgent()
            leads = asyncio.run(agent.run(target_prompt))
            
            if leads:
                st.success(f"✅ Successfully analyzed {len(leads)} companies!")
                
                # Convert results to a pandas DataFrame for a beautiful UI table
                df = pd.DataFrame(leads)
                st.dataframe(df, use_container_width=True)
                
                # Export to CSV and show the download path
                csv_filename = f"leads_{region.replace(' ', '_').lower()}.csv"
                export_status = export_to_csv(leads, csv_filename)
                st.info(export_status)
            else:
                st.warning("⚠️ No valid leads were generated. Try broadening your search terms.")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")