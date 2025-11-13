"""
Research Agent for ADK Web Interface
Advanced research assistant with Google search and analysis capabilities.
"""

print("----- EXAMPLE PLUGIN - DOES NOTHING ----- ")

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search, preload_memory
from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.plugins.base_plugin import BasePlugin
from google.genai import types
from typing import List, Dict, Any
import logging

# Configure logging
logger = logging.getLogger(__name__)


# INTEGRATED PLUGIN: Applies to all agent and model calls
class CountInvocationPlugin(BasePlugin):
    """A custom plugin that counts agent and tool invocations."""

    def __init__(self) -> None:
        """Initialize the plugin with counters."""
        super().__init__(name="count_invocation")
        self.agent_count: int = 0
        self.tool_count: int = 0
        self.llm_request_count: int = 0
        self.search_queries: int = 0
        self.paper_analyses: int = 0

        # Setup plugin logging
        self.plugin_logger = logging.getLogger(f"{__name__}.CountInvocationPlugin")
        self.plugin_logger.info("🔌 Research CountInvocationPlugin initialized")

    # Callback 1: Runs before an agent is called. You can add any custom logic here.
    async def before_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> None:
        """Count agent runs."""
        self.agent_count += 1

        # Track specific research activities
        agent_name = agent.name.lower()
        if "search" in agent_name:
            self.search_queries += 1
            self.plugin_logger.info(
                f"🔍 [Plugin] Search agent called: {self.search_queries} total searches"
            )
        elif "analysis" in agent_name:
            self.paper_analyses += 1
            self.plugin_logger.info(
                f"📊 [Plugin] Analysis agent called: {self.paper_analyses} total analyses"
            )

        self.plugin_logger.info(
            f"🤖 [Plugin] Agent '{agent.name}' run count: {self.agent_count}"
        )

    # Callback 2: Runs before a model is called. You can add any custom logic here.
    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> None:
        """Count LLM requests."""
        self.llm_request_count += 1
        model_name = getattr(llm_request, "model", "unknown")
        self.plugin_logger.info(
            f"🧠 [Plugin] LLM request count: {self.llm_request_count} (Model: {model_name})"
        )

    def get_stats(self) -> Dict[str, int]:
        """Get current statistics."""
        return {
            "agent_count": self.agent_count,
            "llm_request_count": self.llm_request_count,
            "search_queries": self.search_queries,
            "paper_analyses": self.paper_analyses,
        }


# Create plugin instance
research_plugin = CountInvocationPlugin()

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

# Main research agent for ADK Web with plugin integration
research_agent = LlmAgent(
    name="advanced_research_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="🔬 Advanced AI Research Assistant with Observability",
    instruction="""You are an advanced research agent with comprehensive research capabilities and built-in observability.

    WORKFLOW:
    1. Use the research_search_agent to find relevant academic papers and research
    2. Use the research_analysis_agent to analyze and evaluate the findings
    3. Use preload_memory to recall any previous research context
    4. Provide a comprehensive research report with:
       - Key findings summary
       - Paper count and quality metrics
       - Recommendations for further research
       - Properly formatted citations

    OBSERVABILITY: This agent includes a CountInvocationPlugin that tracks:
    - Agent invocation counts
    - LLM request counts  
    - Search query counts
    - Paper analysis counts

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
    # Note: Plugins are typically configured at the Runner level, not directly on agents
    # The research_plugin instance is available for use with Runner configuration
)


# Helper function to create a runner with the plugin enabled
def create_research_runner_with_plugin(
    session_service, memory_service=None, app_name="research_app"
):
    """
    Create a Runner with the CountInvocationPlugin enabled.

    Usage example:
        from google.adk.runners import Runner
        from google.adk.sessions import InMemorySessionService

        session_service = InMemorySessionService()
        runner = create_research_runner_with_plugin(session_service)

        # The plugin will now track all agent and LLM calls
        # Check stats with: research_plugin.get_stats()
    """
    try:
        from google.adk.runners import Runner

        runner = Runner(
            agent=research_agent,
            app_name=app_name,
            session_service=session_service,
            memory_service=memory_service,
            plugins=[research_plugin],  # Enable the invocation tracking plugin
        )

        logger.info("🔌 Research runner created with CountInvocationPlugin enabled")
        return runner

    except Exception as e:
        logger.warning(f"Could not create runner with plugin: {e}")
        # Fallback to basic runner
        from google.adk.runners import Runner

        return Runner(
            agent=research_agent,
            app_name=app_name,
            session_service=session_service,
            memory_service=memory_service,
        )


# Function to get current plugin statistics
def get_research_plugin_stats():
    """Get current invocation statistics from the plugin."""
    return research_plugin.get_stats()


# ADK Web expects 'root_agent' as the main agent variable
root_agent = research_agent
