#!/usr/bin/env python3
"""
Advanced Research Agent with Web Interface and Observability
This agent provides comprehensive research capabilities with logging and web access.
"""

import asyncio
import os
import logging
import argparse
from typing import List, Dict, Any
from flask import Flask, render_template_string, request, jsonify
import threading
import time

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search, preload_memory
from google.genai import types

# Configuration
APP_NAME = "research_agent"
USER_ID = "researcher"
SESSION_ID = "research_session"

# Clean up previous logs
for log_file in ["research_agent.log", "web_server.log"]:
    if os.path.exists(log_file):
        os.remove(log_file)
        print(f"🧹 Cleaned up {log_file}")


# Configure logging
def setup_logging(log_level="INFO"):
    """Setup comprehensive logging for the research agent."""
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.FileHandler("research_agent.log"), logging.StreamHandler()],
    )
    return logging.getLogger(__name__)


logger = setup_logging()

# Retry configuration
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


# Research tools
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


# Specialized agents
def create_search_agent():
    """Create a specialized Google search agent for research."""
    return LlmAgent(
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


def create_analysis_agent():
    """Create a specialized analysis agent for research evaluation."""
    return LlmAgent(
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


# Main research agent
def create_research_agent():
    """Create the main research agent with observability."""
    search_agent = create_search_agent()
    analysis_agent = create_analysis_agent()

    return LlmAgent(
        name="advanced_research_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
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

        IMPORTANT: Always be thorough and academic in your approach. Provide detailed analysis and clear conclusions.""",
        tools=[
            AgentTool(agent=search_agent),
            AgentTool(agent=analysis_agent),
            preload_memory,
            count_papers,
            analyze_research_quality,
        ],
    )


# Web interface
app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Research Agent</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        .header { text-align: center; margin-bottom: 30px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .container { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .query-form { margin-bottom: 30px; }
        .query-input { width: 80%; padding: 15px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px; }
        .submit-btn { background: #007bff; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; margin-left: 10px; }
        .submit-btn:hover { background: #0056b3; }
        .loading { display: none; text-align: center; padding: 20px; color: #666; }
        .result { background: #f8f9fa; padding: 20px; border-left: 4px solid #007bff; margin: 20px 0; border-radius: 5px; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
        .metric-card { background: #e9ecef; padding: 15px; border-radius: 5px; text-align: center; }
        .metric-value { font-size: 24px; font-weight: bold; color: #007bff; }
        .logs { background: #343a40; color: #f8f9fa; padding: 15px; border-radius: 5px; font-family: monospace; max-height: 300px; overflow-y: auto; }
        .status { padding: 10px; border-radius: 5px; margin: 10px 0; }
        .status.success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .status.error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔬 Advanced Research Agent</h1>
        <p>AI-Powered Research Assistant with Observability & Analytics</p>
    </div>

    <div class="container">
        <div class="query-form">
            <input type="text" id="queryInput" class="query-input" placeholder="Enter your research query (e.g., 'recent AI papers on computer vision')" value="">
            <button onclick="submitQuery()" class="submit-btn">🔍 Research</button>
        </div>

        <div id="loading" class="loading">
            <h3>🧠 Agent is researching...</h3>
            <p>Searching databases, analyzing papers, and generating insights...</p>
        </div>

        <div id="status"></div>
        <div id="results"></div>
        <div id="metrics"></div>
        <div id="logs-container" style="display: none;">
            <h3>🔍 Agent Logs</h3>
            <div id="logs" class="logs"></div>
        </div>
    </div>

    <script>
        let currentResults = null;

        async function submitQuery() {
            const query = document.getElementById('queryInput').value;
            if (!query.trim()) {
                showStatus('Please enter a research query', 'error');
                return;
            }

            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').innerHTML = '';
            document.getElementById('metrics').innerHTML = '';
            showStatus('Research in progress...', 'success');

            try {
                const response = await fetch('/research', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query })
                });

                const data = await response.json();
                
                if (data.success) {
                    displayResults(data);
                    showStatus('Research completed successfully!', 'success');
                } else {
                    showStatus('Research failed: ' + data.error, 'error');
                }
            } catch (error) {
                showStatus('Error: ' + error.message, 'error');
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        }

        function displayResults(data) {
            currentResults = data;
            
            // Display main results
            document.getElementById('results').innerHTML = `
                <div class="result">
                    <h3>📊 Research Results</h3>
                    <div style="white-space: pre-wrap;">${data.response}</div>
                </div>
            `;

            // Display metrics if available
            if (data.metrics) {
                const metricsHTML = `
                    <h3>📈 Research Metrics</h3>
                    <div class="metrics">
                        <div class="metric-card">
                            <div class="metric-value">${data.metrics.papers_found || 'N/A'}</div>
                            <div>Papers Found</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">${(data.metrics.processing_time || 0).toFixed(2)}s</div>
                            <div>Processing Time</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">${data.metrics.agent_calls || 'N/A'}</div>
                            <div>Agent Calls</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">${data.metrics.quality_score || 'N/A'}</div>
                            <div>Quality Score</div>
                        </div>
                    </div>
                `;
                document.getElementById('metrics').innerHTML = metricsHTML;
            }

            // Show logs section
            if (data.logs) {
                document.getElementById('logs-container').style.display = 'block';
                document.getElementById('logs').innerHTML = data.logs.join('\\n');
            }
        }

        function showStatus(message, type) {
            const statusDiv = document.getElementById('status');
            statusDiv.innerHTML = `<div class="status ${type}">${message}</div>`;
            setTimeout(() => {
                statusDiv.innerHTML = '';
            }, 5000);
        }

        // Auto-focus on load
        window.onload = () => {
            document.getElementById('queryInput').focus();
            document.getElementById('queryInput').addEventListener('keypress', (e) => {
                if (e.key === 'Enter') submitQuery();
            });
        };
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    """Serve the main research interface."""
    return render_template_string(HTML_TEMPLATE)


@app.route("/research", methods=["POST"])
def research():
    """Handle research queries via API."""
    try:
        data = request.json
        query = data.get("query", "")

        if not query:
            return jsonify({"success": False, "error": "No query provided"})

        logger.info(f"Processing research query: {query}")
        start_time = time.time()

        # Run the research agent
        result = asyncio.run(run_research_agent(query))

        processing_time = time.time() - start_time
        logger.info(f"Research completed in {processing_time:.2f} seconds")

        # Prepare response with metrics
        response_data = {
            "success": True,
            "response": result["response"],
            "metrics": {
                "processing_time": processing_time,
                "papers_found": result.get("papers_count", 0),
                "agent_calls": result.get("agent_calls", 0),
                "quality_score": result.get("quality_score", 0),
            },
            "logs": result.get("logs", []),
        }

        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Research error: {str(e)}")
        return jsonify({"success": False, "error": str(e)})


# Agent execution
async def run_research_agent(query: str) -> Dict[str, Any]:
    """Run the research agent with observability."""
    logger.info(f"Starting research for: {query}")

    # Setup services (using InMemorySessionService for simplicity)
    from google.adk.sessions import InMemorySessionService

    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()

    # Create session
    session = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    logger.info(f"Created session: {SESSION_ID}")

    # Create the research agent
    research_agent = create_research_agent()

    # Setup runner
    runner = Runner(
        agent=research_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    # Create content
    content = types.Content(role="user", parts=[types.Part(text=query)])

    # Track metrics
    agent_calls = 0
    papers_count = 0
    quality_score = 0
    logs = []

    try:
        # Run the agent
        events = runner.run_async(
            user_id=USER_ID, session_id=SESSION_ID, new_message=content
        )

        response_text = ""
        async for event in events:
            agent_calls += 1

            if event.is_final_response():
                response_text = event.content.parts[0].text
                logger.info("Research completed successfully")

                # Extract metrics from response (simple parsing)
                if "papers" in response_text.lower():
                    papers_count = response_text.lower().count("paper")
                quality_score = min(len(response_text) / 100, 10.0)

                break

        return {
            "response": response_text,
            "papers_count": papers_count,
            "agent_calls": agent_calls,
            "quality_score": round(quality_score, 2),
            "logs": logs,
        }

    except Exception as e:
        logger.error(f"Research agent error: {str(e)}")
        raise e


def run_web_server(port=5000, debug=False):
    """Run the Flask web server."""
    logger.info(f"Starting research agent web server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=debug, threaded=True)


def main():
    """Main entry point with CLI support."""
    parser = argparse.ArgumentParser(
        description="Advanced Research Agent with Web Interface"
    )
    parser.add_argument(
        "--query", "-q", help="Direct research query (non-interactive mode)"
    )
    parser.add_argument("--web", "-w", action="store_true", help="Start web server")
    parser.add_argument(
        "--port", "-p", type=int, default=5000, help="Web server port (default: 5000)"
    )
    parser.add_argument(
        "--log_level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set logging level",
    )
    parser.add_argument(
        "--api-key", help="Google API key (will set GOOGLE_API_KEY env var)"
    )

    args = parser.parse_args()

    # Setup logging with specified level
    global logger
    logger = setup_logging(args.log_level)

    # Set API key if provided
    if args.api_key:
        os.environ["GOOGLE_API_KEY"] = args.api_key
        logger.info("API key set from command line")

    # Check for API key
    if not os.getenv("GOOGLE_API_KEY"):
        logger.error("❌ GOOGLE_API_KEY not found!")
        print("\n🔑 Please set your API key:")
        print("   export GOOGLE_API_KEY='your-api-key'")
        print("   python3 research_agent.py --web")
        return

    if args.web:
        # Web mode
        logger.info("🌐 Starting web interface...")
        print(f"\n🔬 Research Agent Web Interface")
        print(f"🌍 Access at: http://localhost:{args.port}")
        print(f"📊 Features: Research search, analysis, observability")
        print(f"🔄 Press Ctrl+C to stop\n")
        run_web_server(port=args.port, debug=(args.log_level == "DEBUG"))

    elif args.query:
        # Direct query mode
        logger.info("💭 Running direct query mode")
        result = asyncio.run(run_research_agent(args.query))
        print("\n" + "=" * 60)
        print("🔬 RESEARCH RESULTS")
        print("=" * 60)
        print(result["response"])
        print("\n" + "=" * 60)
        print(
            f"📊 Metrics: {result['papers_count']} papers, {result['agent_calls']} calls, Quality: {result['quality_score']}"
        )

    else:
        # Interactive mode
        logger.info("🤖 Starting interactive research mode")
        print("\n🔬 Advanced Research Agent")
        print("💡 Type your research queries or 'quit' to exit")
        print("🌐 Use --web flag to start web interface\n")

        while True:
            try:
                query = input("Research Query: ").strip()
                if query.lower() in ["quit", "exit", "q"]:
                    break
                if query:
                    result = asyncio.run(run_research_agent(query))
                    print(f"\n📋 Results:\n{result['response']}\n")
                    print(
                        f"📊 {result['papers_count']} papers analyzed, Quality score: {result['quality_score']}\n"
                    )
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                print(f"❌ Error: {e}")

        print("👋 Research session ended")


if __name__ == "__main__":
    main()
