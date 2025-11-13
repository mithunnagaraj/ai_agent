# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import os
import argparse
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types

APP_NAME="google_search_agent"
USER_ID="user1234"
SESSION_ID="1234"


root_agent = Agent(
    name="basic_search_agent",
    model="gemini-2.0-flash",
    description="Agent to answer questions using Google Search.",
    instruction="I can answer your questions by searching the internet. Just ask me anything!",
    # google_search is a pre-built tool which allows the agent to perform Google searches.
    tools=[google_search]
)

# Session and Runner
async def setup_session_and_runner():
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
    return session, runner

# Agent Interaction
async def call_agent_async(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    session, runner = await setup_session_and_runner()
    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    async for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response: ", final_response)
# Note: In Colab, you can directly use 'await' at the top level.
# If running this code as a standalone Python script, you'll need to use asyncio.run() or manage the event loop.
def run_agent(query):
    try:
        loop = asyncio.get_running_loop()
        # If we're in a running event loop (e.g., Jupyter/Colab), schedule the task
        loop.create_task(call_agent_async(query))
    except RuntimeError:
        # No running event loop, safe to use asyncio.run()
        asyncio.run(call_agent_async(query))


def main():
    parser = argparse.ArgumentParser(description="Run the my_agent agent")
    parser.add_argument("--query", "-q", default="what's the latest ai news?", help="Query to send to the agent")
    parser.add_argument("--api-key", help="Provide a Google API key to use the Google AI API (will set GOOGLE_API_KEY env var)")
    parser.add_argument("--project", help="Google Cloud project id (for Vertex AI backend)")
    parser.add_argument("--location", help="Google Cloud location (for Vertex AI backend)")
    parser.add_argument("--dry-run", action="store_true", help="Do not call external APIs; simulate an agent response")

    args = parser.parse_args()

    # If provided, set environment variables used by the client library
    if args.api_key:
        os.environ["GOOGLE_API_KEY"] = args.api_key
    if args.project:
        os.environ["GOOGLE_CLOUD_PROJECT"] = args.project
    if args.location:
        os.environ["GOOGLE_CLOUD_LOCATION"] = args.location

    if args.dry_run:
        print("[dry-run] Agent would run with query:\n", args.query)
        print("[dry-run] Skipping external API calls. Example simulated response:\nAgent Response: This is a dry-run simulated response for the query.")
        return

    run_agent(args.query)


if __name__ == "__main__":
    main()