"""
Custom Plugin for Agent Observability
Counts agent and tool invocations for monitoring and debugging.
"""

print("----- EXAMPLE PLUGIN - DOES NOTHING ----- ")

import logging
from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.plugins.base_plugin import BasePlugin


# Applies to all agent and model calls
class CountInvocationPlugin(BasePlugin):
    """A custom plugin that counts agent and tool invocations."""

    def __init__(self) -> None:
        """Initialize the plugin with counters."""
        super().__init__(name="count_invocation")
        self.agent_count: int = 0
        self.tool_count: int = 0
        self.llm_request_count: int = 0
        self.session_stats = {}

        # Setup logging for the plugin
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.logger.info("🔌 CountInvocationPlugin initialized")

    # Callback 1: Runs before an agent is called. You can add any custom logic here.
    async def before_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> None:
        """Count agent runs."""
        self.agent_count += 1

        # Track per-session stats if session info is available
        session_id = getattr(callback_context, "session_id", "unknown")
        if session_id not in self.session_stats:
            self.session_stats[session_id] = {
                "agent_calls": 0,
                "llm_requests": 0,
                "start_time": (
                    callback_context.timestamp
                    if hasattr(callback_context, "timestamp")
                    else None
                ),
            }

        self.session_stats[session_id]["agent_calls"] += 1

        self.logger.info(
            f"🤖 [Plugin] Agent '{agent.name}' run count: {self.agent_count} (Session: {session_id})"
        )

    # Callback 2: Runs before a model is called. You can add any custom logic here.
    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> None:
        """Count LLM requests."""
        self.llm_request_count += 1

        # Track per-session stats
        session_id = getattr(callback_context, "session_id", "unknown")
        if session_id in self.session_stats:
            self.session_stats[session_id]["llm_requests"] += 1

        model_name = getattr(llm_request, "model", "unknown")
        self.logger.info(
            f"🧠 [Plugin] LLM request count: {self.llm_request_count} (Model: {model_name}, Session: {session_id})"
        )

    # Additional callback: Runs after an agent completes
    async def after_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> None:
        """Log completion stats."""
        session_id = getattr(callback_context, "session_id", "unknown")
        if session_id in self.session_stats:
            stats = self.session_stats[session_id]
            self.logger.info(
                f"✅ [Plugin] Agent '{agent.name}' completed. Session stats: {stats['agent_calls']} agent calls, {stats['llm_requests']} LLM requests"
            )

    def get_stats(self) -> dict:
        """Get current plugin statistics."""
        return {
            "total_agent_count": self.agent_count,
            "total_llm_request_count": self.llm_request_count,
            "total_tool_count": self.tool_count,
            "session_stats": self.session_stats,
            "active_sessions": len(self.session_stats),
        }

    def reset_stats(self) -> None:
        """Reset all counters."""
        self.agent_count = 0
        self.tool_count = 0
        self.llm_request_count = 0
        self.session_stats = {}
        self.logger.info("🔄 [Plugin] Statistics reset")


# Enhanced plugin with research-specific tracking
class ResearchInvocationPlugin(CountInvocationPlugin):
    """Enhanced plugin specifically for research agent tracking."""

    def __init__(self) -> None:
        super().__init__()
        self.name = "research_invocation"
        self.search_queries = 0
        self.paper_analyses = 0
        self.quality_checks = 0

    async def before_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> None:
        """Enhanced tracking for research agents."""
        await super().before_agent_callback(
            agent=agent, callback_context=callback_context
        )

        # Track specific research activities
        agent_name = agent.name.lower()
        if "search" in agent_name:
            self.search_queries += 1
            self.logger.info(
                f"🔍 [Research Plugin] Search queries: {self.search_queries}"
            )
        elif "analysis" in agent_name:
            self.paper_analyses += 1
            self.logger.info(
                f"📊 [Research Plugin] Paper analyses: {self.paper_analyses}"
            )

    def get_research_stats(self) -> dict:
        """Get research-specific statistics."""
        base_stats = self.get_stats()
        base_stats.update(
            {
                "search_queries": self.search_queries,
                "paper_analyses": self.paper_analyses,
                "quality_checks": self.quality_checks,
            }
        )
        return base_stats


# Factory function to create plugin instances
def create_invocation_plugin(plugin_type: str = "basic") -> BasePlugin:
    """
    Factory function to create invocation plugins.

    Args:
        plugin_type: "basic" for CountInvocationPlugin or "research" for ResearchInvocationPlugin

    Returns:
        Configured plugin instance
    """
    if plugin_type == "research":
        return ResearchInvocationPlugin()
    else:
        return CountInvocationPlugin()


# Global plugin instance for easy access
_plugin_instance = None


def get_plugin_instance() -> CountInvocationPlugin:
    """Get or create the global plugin instance."""
    global _plugin_instance
    if _plugin_instance is None:
        _plugin_instance = ResearchInvocationPlugin()
    return _plugin_instance


if __name__ == "__main__":
    # Test the plugin
    print("🧪 Testing CountInvocationPlugin...")

    plugin = create_invocation_plugin("research")
    print(f"Plugin created: {plugin.name}")
    print(f"Initial stats: {plugin.get_stats()}")
