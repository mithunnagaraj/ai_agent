# How to Make Your Agent Stateful

## Current Setup (memory_mgmt.py)
Your agent currently uses:
- ✅ **InMemorySessionService** - sessions exist only while script runs
- ✅ **InMemoryMemoryService** - memories stored in RAM (lost on restart)
- ✅ **Callback auto-save** - automatically saves sessions to memory

## Making It Truly Stateful

### Option 1: Persistent Sessions (Recommended)
Use `DatabaseSessionService` to save sessions to disk:

```python
from google.adk.sessions import DatabaseSessionService

# Replace InMemorySessionService with:
session_service = DatabaseSessionService(db_url="sqlite:///agent_sessions.db")
```

**Benefits:**
- Sessions persist across script restarts
- User conversation history is preserved
- Works even if you close and reopen the program

### Option 2: Always Use Same Session ID
Instead of creating new sessions, reuse the same session for each user:

```python
# Instead of random session IDs like "session-01", "session-02"
# Always use the same one for each user:
PERSISTENT_SESSION_ID = f"user_{USER_ID}_main_session"

await run_session(
    runner,
    "What's my name?",
    PERSISTENT_SESSION_ID  # Same ID every time!
)
```

### Option 3: Combine Memory + Persistent Sessions
Best approach for production:

```python
from google.adk.sessions import DatabaseSessionService

# Persistent sessions
session_service = DatabaseSessionService(db_url="sqlite:///sessions.db")

# Memory service (can also use a database-backed one)
memory_service = InMemoryMemoryService()

# Agent with memory tools
agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction="""You have access to memory. When users ask about past 
    conversations or personal info, use preload_memory to recall it.""",
    tools=[preload_memory],
    after_agent_callback=auto_save_callback  # Auto-saves to memory
)
```

## Key Changes Needed

### 1. Update Session Service (Line ~73 in memory_mgmt.py)
```python
# Change from:
session_service = InMemorySessionService()

# To:
from google.adk.sessions import DatabaseSessionService
session_service = DatabaseSessionService(db_url="sqlite:///agent_sessions.db")
```

### 2. Use Consistent Session IDs
```python
# Define at the top:
MAIN_SESSION = f"{USER_ID}_persistent_session"

# Use everywhere:
await run_session(runner, "your query", MAIN_SESSION)
```

### 3. Agent Instructions (Already Updated!)
Your agent now has proper instructions to use memory:
```python
instruction="""You are a helpful assistant with access to long-term memory.
When the user asks about personal information, you MUST use the preload_memory 
tool to search for relevant information from past sessions."""
```

## Testing Stateful Behavior

1. **First run:**
   ```bash
   python3.12 my_agent/memory_mgmt.py
   # Tell the agent: "My name is John"
   ```

2. **Stop the script and run again:**
   ```bash
   python3.12 my_agent/memory_mgmt.py
   # Ask: "What's my name?"
   # Agent should remember "John"!
   ```

## Summary

**For stateful within a session:** Already working! ✅
**For stateful across sessions:** 
- Use `DatabaseSessionService` ✅
- Use same session ID for each user ✅
- Use memory + preload_memory (already setup) ✅

Your agent is now ready to be fully stateful!
