#!/usr/bin/env python3
"""
Plugin Demo - Research Agent Observability
Demonstrates how to use the CountInvocationPlugin with the research agent.
"""

import asyncio
import logging
import os
import sys

# Setup logging to see plugin output
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


async def demo_plugin_usage():
    """Demonstrate plugin usage with research agent."""

    print("🔌 PLUGIN DEMO - Research Agent Observability")
    print("=" * 60)

    # Check for API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Please set GOOGLE_API_KEY environment variable")
        return

    try:
        # Option 1: Import standalone plugin
        print("\n📦 Option 1: Using standalone plugin file")
        from invocation_plugin import create_invocation_plugin, get_plugin_instance

        standalone_plugin = create_invocation_plugin("research")
        print(f"✅ Standalone plugin created: {standalone_plugin.name}")
        print(f"Initial stats: {standalone_plugin.get_stats()}")

    except ImportError as e:
        print(f"⚠️  Could not import standalone plugin: {e}")

    try:
        # Option 2: Use integrated plugin in research agent
        print("\n🔬 Option 2: Using integrated plugin in research agent")

        # Import the research agent with integrated plugin
        sys.path.append("agents/research_agent")
        from agents.research_agent.agent import (
            research_agent,
            research_plugin,
            create_research_runner_with_plugin,
            get_research_plugin_stats,
        )

        print(f"✅ Research agent loaded with integrated plugin")
        print(f"Plugin stats: {get_research_plugin_stats()}")

        # Create services
        from google.adk.sessions import InMemorySessionService
        from google.adk.memory import InMemoryMemoryService
        from google.genai import types

        session_service = InMemorySessionService()
        memory_service = InMemoryMemoryService()

        # Create session
        session = await session_service.create_session(
            app_name="plugin_demo", user_id="demo_user", session_id="demo_session"
        )

        # Create runner with plugin
        runner = create_research_runner_with_plugin(
            session_service=session_service,
            memory_service=memory_service,
            app_name="plugin_demo",
        )

        print("🚀 Runner created with plugin enabled")

        # Run a simple query to test the plugin
        print("\n🧪 Testing plugin with a research query...")

        content = types.Content(
            role="user",
            parts=[
                types.Part(text="Find recent papers on machine learning optimization")
            ],
        )

        events = runner.run_async(
            user_id="demo_user", session_id="demo_session", new_message=content
        )

        response_text = ""
        async for event in events:
            if event.is_final_response():
                response_text = event.content.parts[0].text
                break

        print("\n📊 PLUGIN STATISTICS AFTER QUERY:")
        stats = get_research_plugin_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")

        print(f"\n📋 Research Response Preview:")
        print(f"{response_text[:200]}...")

        print("\n✅ Plugin demo completed successfully!")

    except Exception as e:
        logger.error(f"Error in plugin demo: {e}")
        print(f"❌ Plugin demo failed: {e}")


def show_plugin_usage_examples():
    """Show code examples for using the plugins."""

    print("\n📚 PLUGIN USAGE EXAMPLES")
    print("=" * 60)

    print(
        """
🔌 1. STANDALONE PLUGIN (invocation_plugin.py):

from invocation_plugin import create_invocation_plugin
from google.adk.runners import Runner

# Create plugin
plugin = create_invocation_plugin("research")

# Use with runner
runner = Runner(
    agent=your_agent,
    session_service=session_service,
    plugins=[plugin]  # Add plugin here
)

# Get stats
stats = plugin.get_stats()
print(f"Agent calls: {stats['agent_count']}")
"""
    )

    print(
        """
🔬 2. INTEGRATED PLUGIN (in research_agent/agent.py):

from agents.research_agent.agent import (
    create_research_runner_with_plugin,
    get_research_plugin_stats
)

# Create runner with plugin already configured
runner = create_research_runner_with_plugin(session_service)

# Use runner normally - plugin tracks automatically
events = runner.run_async(user_id, session_id, message)

# Check stats anytime
stats = get_research_plugin_stats()
print(f"LLM requests: {stats['llm_request_count']}")
"""
    )

    print(
        """
🌐 3. ADK WEB USAGE:

The integrated plugin automatically works with 'adk web agents':

1. Start ADK web: adk web agents --port 8082
2. Use research agent normally in the web UI
3. Plugin tracks all calls in the background
4. Check logs for plugin output: [Plugin] messages

The plugin tracks:
- 🤖 Agent invocations
- 🧠 LLM requests  
- 🔍 Search queries
- 📊 Paper analyses
"""
    )


if __name__ == "__main__":
    print("🔌 Research Agent Plugin Demo")

    # Show usage examples
    show_plugin_usage_examples()

    # Run the demo
    try:
        asyncio.run(demo_plugin_usage())
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        logger.error(f"Demo error: {e}")
        print(f"❌ Demo failed: {e}")
