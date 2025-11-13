#!/usr/bin/env python3
"""
Simple test script to demonstrate persistent memory across sessions.
This shows how your agent will remember your name between runs.
"""

import asyncio
import sys
import os

# Add the parent directory to Python path so we can import from my_agent
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_agent.memory_mgmt import (
    session_service,
    memory_service,
    APP_NAME,
    USER_ID,
    PERSISTENT_SESSION_ID,
    auto_memory_agent,
    auto_runner,
    run_session,
    create_auto_save_callback,
)
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.tools import preload_memory
from google.genai import types


async def test_persistent_memory():
    """Test that demonstrates persistent memory across script runs."""

    print("🧪 PERSISTENT MEMORY TEST")
    print("=" * 50)

    # Create agent with memory capabilities
    retry_config = types.HttpRetryOptions(
        attempts=5, exp_base=7, initial_delay=1, http_status_codes=[429, 500, 503, 504]
    )

    auto_save_callback = create_auto_save_callback(
        memory_service, session_service, APP_NAME, USER_ID
    )

    agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="PersistentAgent",
        instruction="""You are a helpful assistant with long-term memory.

IMPORTANT: When users ask about personal information (their name, preferences, etc.), 
you MUST use the preload_memory tool to recall information from past conversations.

Always be friendly and use what you remember about the user to provide personalized responses.""",
        tools=[preload_memory],
        after_agent_callback=auto_save_callback,
    )

    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    # Check if this is the first run or a subsequent run
    try:
        existing_session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=PERSISTENT_SESSION_ID
        )
        is_first_run = len(existing_session.events) == 0
    except:
        is_first_run = True

    if is_first_run:
        print("👋 First time meeting! Tell me your name:")
        await run_session(
            runner,
            "Hi there! My name is Sarah and I'm a software developer. Please remember this about me.",
            PERSISTENT_SESSION_ID,
        )
    else:
        print("👋 Welcome back! Let me see if I remember you...")
        await run_session(
            runner,
            "Hi again! What's my name and what do you remember about me?",
            PERSISTENT_SESSION_ID,
        )

    print("\n✅ Test completed!")
    print(f"💾 Session data saved in: agent_sessions.db")
    print(f"🔑 Session ID: {PERSISTENT_SESSION_ID}")
    print("\n💡 To test persistence:")
    print("   1. Run this script again - the agent should remember your name!")
    print("   2. Or run: python3.12 my_agent/memory_mgmt.py")


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Please set your Google API key:")
        print("   export GOOGLE_API_KEY='your-api-key-here'")
        print("   python3.12 test_memory.py")
        sys.exit(1)

    asyncio.run(test_persistent_memory())
