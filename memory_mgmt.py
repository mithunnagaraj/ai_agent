import asyncio
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.tools import load_memory, preload_memory
from google.genai import types

print("✅ ADK components imported successfully.")

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)


async def run_session(
    runner_instance: Runner, user_queries: list[str] | str, session_id: str = "default"
):
    """Helper function to run queries in a session and display responses."""
    print(f"\n### Session: {session_id}")

    # Create or retrieve session
    try:
        session = await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )
    except:
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )

    # Convert single query to list
    if isinstance(user_queries, str):
        user_queries = [user_queries]

    # Process each query
    for query in user_queries:
        print(f"\nUser > {query}")
        query_content = types.Content(role="user", parts=[types.Part(text=query)])

        # Stream agent response
        async for event in runner_instance.run_async(
            user_id=USER_ID, session_id=session.id, new_message=query_content
        ):
            if event.is_final_response() and event.content and event.content.parts:
                text = event.content.parts[0].text
                if text and text != "None":
                    print(f"Model: > {text}")


print("✅ Helper functions defined.")

# Use persistent memory storage
memory_service = InMemoryMemoryService()  # For now - can upgrade to persistent later
print("✅ Memory service created")

# Define constants used throughout the notebook
APP_NAME = "StatefulAgentApp"
USER_ID = "demo_user"
# Use consistent session ID so user's context persists
PERSISTENT_SESSION_ID = f"{USER_ID}_main_session"
print(f"✅ Using persistent session ID: {PERSISTENT_SESSION_ID}")

# For stateful behavior: Use persistent session storage
from google.adk.sessions import DatabaseSessionService

# Using persistent storage so your name/conversations are remembered across restarts
session_service = DatabaseSessionService(db_url="sqlite:///agent_sessions.db")
print("✅ Using persistent session storage (agent_sessions.db)")

# Create agent
user_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="MemoryDemoAgent",
    instruction="Answer user questions in simple words.",
)

print("✅ Agent created")

# Create runner with BOTH services
runner = Runner(
    agent=user_agent,
    app_name="MemoryDemoApp",
    session_service=session_service,
    memory_service=memory_service,  # Memory service is now available!
)
print("✅ Agent and Runner created with memory support!")


async def main():
    """Main async function to run all sessions and memory operations."""
    # User tells agent about their favorite color - using persistent session
    await run_session(
        runner,
        "My favorite color is blue-green. Can you write a Haiku about it?",
        PERSISTENT_SESSION_ID,  # Use persistent session ID
    )

    session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=PERSISTENT_SESSION_ID
    )

    # Let's see what's in the session
    print("📝 Session contains:")
    for event in session.events:
        text = (
            event.content.parts[0].text[:60]
            if event.content and event.content.parts
            else "(empty)"
        )
        print(f"  {event.content.role}: {text}...")

    # This is the key method!
    await memory_service.add_session_to_memory(session)

    print("✅ Session added to memory!")

    # Create agent
    user_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="MemoryDemoAgent",
        instruction="Answer user questions in simple words. Use load_memory tool if you need to recall past conversations.",
        tools=[
            load_memory
        ],  # Agent now has access to Memory and can search it whenever it decides to!
    )

    print("✅ Agent with load_memory tool created.")

    # Create a new runner with the updated agent
    runner = Runner(
        agent=user_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    await run_session(runner, "What is my favorite color?", PERSISTENT_SESSION_ID)

    await run_session(runner, "My birthday is on March 15th.", PERSISTENT_SESSION_ID)

    # Manually save the session to memory
    birthday_session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=PERSISTENT_SESSION_ID
    )

    await memory_service.add_session_to_memory(birthday_session)

    print("✅ Session saved to memory!")

    # Test retrieval in the SAME session (should remember from conversation history)
    await run_session(
        runner, "When is my birthday?", PERSISTENT_SESSION_ID  # Same session ID
    )

    # Search for color preferences
    search_response = await memory_service.search_memory(
        app_name=APP_NAME, user_id=USER_ID, query="What is the user's favorite color?"
    )

    print("🔍 Search Results:")
    print(f"  Found {len(search_response.memories)} relevant memories")
    print()

    for memory in search_response.memories:
        if memory.content and memory.content.parts:
            text = memory.content.parts[0].text[:80]
            print(f"  [{memory.author}]: {text}...")


def create_auto_save_callback(memory_svc, session_svc, app_name, user_id):
    """Factory function that creates a callback closure with access to memory and session services."""

    async def auto_save_to_memory(callback_context):
        """Automatically save session to memory after each agent turn."""
        try:
            # Try to extract the session_id from callback_context
            session_id = None
            session_obj = None

            # Look for invocation_context or similar
            for attr in ("invocation_context", "_invocation_context", "context"):
                ctx = getattr(callback_context, attr, None)
                if ctx is not None:
                    # Try to get session object first
                    session_obj = getattr(ctx, "session", None)
                    if session_obj is not None:
                        session_id = getattr(session_obj, "id", None)
                        break

            # Fallback: try to get session_id directly
            if session_id is None:
                session_id = getattr(callback_context, "session_id", None)

            # Fallback: search for a session-like object
            if session_id is None:
                for name in dir(callback_context):
                    try:
                        val = getattr(callback_context, name)
                        if (
                            getattr(val, "id", None) is not None
                            and getattr(val, "events", None) is not None
                        ):
                            session_id = val.id
                            break
                    except Exception:
                        continue

            # IMPORTANT: Always fetch the latest session state from the session service
            # This ensures we save the complete conversation including the latest turn
            if session_id:
                session_obj = await session_svc.get_session(
                    app_name=app_name, user_id=user_id, session_id=session_id
                )

                if session_obj is not None:
                    await memory_svc.add_session_to_memory(session_obj)
                    print(
                        f"[auto_save] ✅ Saved session '{session_id}' to memory (with {len(session_obj.events)} events)"
                    )
                else:
                    print(
                        f"[auto_save] ⚠️  Could not fetch session '{session_id}' from session service"
                    )
            else:
                print("[auto_save] ⚠️  Could not locate session_id in callback context")

        except Exception as e:
            print(f"[auto_save] ❌ Error saving to memory: {e}")
            import traceback

            traceback.print_exc()

    return auto_save_to_memory


async def auto_memory_section():
    """Async function for automatic memory saving tests."""
    print("✅ Callback created.")

    # Create the callback with closure access to services
    auto_save_callback = create_auto_save_callback(
        memory_service, session_service, APP_NAME, USER_ID
    )

    # Agent with automatic memory saving
    auto_memory_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="AutoMemoryAgent",
        instruction="""You are a helpful assistant with access to long-term memory.

IMPORTANT: When the user asks about personal information (their name, preferences, past conversations, etc.), 
you MUST use the preload_memory tool to search for relevant information from past sessions.

The preload_memory tool automatically loads relevant memories at the start of each conversation.
Use the information from those memories to answer user questions about themselves.

Always be helpful and use memory to provide personalized responses.""",
        tools=[preload_memory],
        after_agent_callback=auto_save_callback,  # Saves after each turn!
    )

    print("✅ Agent created with automatic memory saving!")

    # Create a runner for the auto-save agent
    # This connects our automated agent to the session and memory services
    auto_runner = Runner(
        agent=auto_memory_agent,  # Use the agent with callback + preload_memory
        app_name=APP_NAME,
        session_service=session_service,  # Same services from Section 3
        memory_service=memory_service,
    )

    print("✅ Runner created.")

    # Test 1: Tell the agent your name (first conversation)
    # The callback will automatically save this to memory when the turn completes
    await run_session(
        auto_runner,
        "Hi! My name is John and I love programming. Remember this about me.",
        PERSISTENT_SESSION_ID,
    )

    # Verify memory was saved
    print("\n🔍 Checking saved memories...")
    search_response = await memory_service.search_memory(
        app_name=APP_NAME, user_id=USER_ID, query="What is the user's name?"
    )
    print(f"   Found {len(search_response.memories)} memories saved")
    if search_response.memories:
        for i, mem in enumerate(search_response.memories[:3]):  # Show first 3
            text = (
                mem.content.parts[0].text[:100]
                if mem.content and mem.content.parts
                else "(empty)"
            )
            print(f"   Memory {i+1}: [{mem.author}] {text}...")
    print()

    # Test 2: Test memory recall by asking about name
    # The agent should retrieve the memory using preload_memory and answer correctly
    print("🔄 Now testing if agent remembers your name...")
    await run_session(
        auto_runner,
        "What is my name? Tell me what you know about me.",
        PERSISTENT_SESSION_ID,  # Same session - should remember from conversation + memory
    )


if __name__ == "__main__":
    import asyncio
    import sys

    print("\n" + "=" * 60)
    print("Running memory_mgmt.py demo")
    print("=" * 60 + "\n")

    # Check for dry-run flag
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("🔧 DRY RUN mode - Skipping API calls\n")
        print("✅ In dry-run mode, both main() and auto_memory_section() are skipped")
        print("   because they require API credentials to call the model.")
        print("\n   To see the callback in action, run with valid API credentials:")
        print("   export GOOGLE_API_KEY='your-key'")
        print("   python3.12 my_agent/memory_mgmt.py\n")
    else:
        # Run the async main function
        print("▶️  Running main() demo...\n")
        try:
            asyncio.run(main())
            print("\n✅ main() completed\n")
        except Exception as e:
            print(f"❌ Error in main(): {e}")
            import traceback

            traceback.print_exc()
            print("\n")

        # Always run the auto memory section (for testing the callback)
        print("▶️  Running auto_memory_section() demo...\n")
        try:
            asyncio.run(auto_memory_section())
            print("\n✅ auto_memory_section() completed\n")
        except Exception as e:
            print(f"❌ Error in auto_memory_section(): {e}")
            import traceback

            traceback.print_exc()
            print("\n")

        # Optional: Add a truly stateful demo
        if "--stateful-demo" in sys.argv:
            print("▶️  Running STATEFUL demo (same session across multiple runs)...\n")
            print("💡 To make your agent truly stateful:")
            print("   1. Use DatabaseSessionService for persistent sessions")
            print("   2. Always use the same session_id for the same user")
            print("   3. Use memory + preload_memory for cross-session recall\n")
