"""
Basic Search Agent for ADK Web Interface
Simple Google search functionality for general queries.
"""

from google.adk.agents import Agent
from google.adk.tools import google_search

# Basic search agent
root_agent = Agent(
    name="basic_search_agent",
    model="gemini-2.0-flash",
    description="🔍 Basic Google Search Agent",
    instruction="""I can answer your questions by searching the internet using Google Search. 

Just ask me anything and I'll search for the most relevant and up-to-date information!

EXAMPLES:
- "What's the latest news in AI?"
- "How does machine learning work?"
- "What are the best programming languages in 2024?"
- "Find information about quantum computing applications"
""",
    tools=[google_search],
)
