"""
Research Agent for ADK Web Interface
Advanced research assistant with Google search and analysis capabilities.
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search, preload_memory
from google.genai import types
from typing import List, Dict, Any
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Retry configuration for robust API calls
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


def count_papers(papers: List[str]) -> int:
    """
    Count the number of research papers in a list.

    Args:
        papers: List of research paper titles/descriptions

    Returns:
        Number of papers in the list
    """
    logger.debug(f"Counting papers: {len(papers) if papers else 0}")
    return len(papers) if papers else 0


def analyze_research_quality(papers: List[str]) -> Dict[str, Any]:
    """
    Analyze the quality metrics of research papers.

    Args:
        papers: List of research paper titles/descriptions

    Returns:
        Dictionary with quality analysis
    """
    logger.info(f"Analyzing quality of {len(papers)} papers")

    analysis = {
        "total_papers": len(papers),
        "avg_title_length": (
            sum(len(paper) for paper in papers) / len(papers) if papers else 0
        ),
        "contains_keywords": {
            "AI": sum(1 for paper in papers if "AI" in paper.upper()),
            "machine learning": sum(
                1 for paper in papers if "machine learning" in paper.lower()
            ),
            "neural": sum(1 for paper in papers if "neural" in paper.lower()),
        },
        "quality_score": min(len(papers) * 0.1, 10.0),  # Simple quality metric
    }

    logger.debug(f"Research analysis completed: {analysis}")
    return analysis


# Create specialized search agent
research_search_agent = LlmAgent(
    name="research_search_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="Advanced research search agent with academic focus",
    instruction="""You are a specialized research search agent. Your task is to:
    
    1. Search for high-quality academic papers and research articles
    2. Focus on peer-reviewed content when possible
    3. Return comprehensive results with titles, sources, and brief descriptions
    4. Prioritize recent research (last 5 years when relevant)
    
    Always provide detailed, well-structured search results for academic research.""",
    tools=[google_search],
)

# Create specialized analysis agent
research_analysis_agent = LlmAgent(
    name="research_analysis_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="Research analysis and evaluation specialist",
    instruction="""You are a research analysis specialist. Your role is to:
    
    1. Evaluate the quality and relevance of research papers
    2. Identify key themes and trends in research findings
    3. Provide citations and methodology analysis
    4. Suggest related research areas and future directions
    
    Always provide thorough, academic-level analysis of research materials.""",
    tools=[count_papers, analyze_research_quality],
)

# Main research agent for ADK Web
research_agent = LlmAgent(
    name="advanced_research_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="🔬 Advanced AI Research Assistant",
    instruction="""You are an advanced research agent with comprehensive research capabilities.

    WORKFLOW:
    1. Use the research_search_agent to find relevant academic papers and research
    2. Use the research_analysis_agent to analyze and evaluate the findings
    3. Use preload_memory to recall any previous research context
    4. Provide a comprehensive research report with:
       - Key findings summary
       - Paper count and quality metrics
       - Recommendations for further research
       - Properly formatted citations

    IMPORTANT: Always be thorough and academic in your approach. Provide detailed analysis and clear conclusions.
    
    EXAMPLES:
    - "Find recent papers on transformer architecture improvements"
    - "Analyze the current state of quantum computing research" 
    - "What are the latest developments in computer vision?"
    - "Research sustainable AI and green computing approaches"
    """,
    tools=[
        AgentTool(agent=research_search_agent),
        AgentTool(agent=research_analysis_agent),
        preload_memory,
        count_papers,
        analyze_research_quality,
    ],
)

# ADK Web expects 'root_agent' as the main agent variable
root_agent = research_agent
