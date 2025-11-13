#!/usr/bin/env python3
"""
Home Automation Agent Demo
Demonstrates smart home management and automation capabilities.
"""

import asyncio
import os
import logging
from typing import Dict, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


async def demo_home_automation():
    """Demonstrate home automation agent capabilities."""

    print("🏠 HOME AUTOMATION AGENT DEMO")
    print("=" * 60)

    # Check for API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Please set GOOGLE_API_KEY environment variable")
        return

    try:
        # Import home automation agent components
        import sys

        sys.path.append("agents/home_automation_agent")

        from agents.home_automation_agent.agent import (
            home_automation_agent,
            list_smart_devices,
            control_device,
            create_automation_routine,
            get_energy_usage,
            check_security_status,
            get_weather_integration,
        )

        print("✅ Home automation agent loaded successfully")

        # Demo 1: List smart devices
        print("\n📱 DEMO 1: Smart Device Discovery")
        print("-" * 40)
        devices = list_smart_devices()
        for device in devices:
            status = device.get("status", "unknown")
            print(f"  🔌 {device['name']} ({device['type']}) - Status: {status}")

        # Demo 2: Device control
        print("\n💡 DEMO 2: Device Control")
        print("-" * 40)

        # Turn on living room lights
        result = control_device("living_room_lights", "on", "80")
        if result["success"]:
            print(f"  ✅ {result['status']}")

        # Set thermostat temperature
        result = control_device("bedroom_thermostat", "set_temperature", "72")
        if result["success"]:
            print(f"  🌡️ {result['status']}")

        # Lock front door
        result = control_device("front_door_lock", "lock")
        if result["success"]:
            print(f"  🔒 {result['status']}")

        # Demo 3: Automation routine
        print("\n🤖 DEMO 3: Automation Routine Creation")
        print("-" * 40)

        routine = create_automation_routine(
            "Good Night Routine",
            "time:10:00 PM",
            "Dim lights to 50%, set thermostat to 68°F, arm security cameras",
        )

        if routine["success"]:
            print(f"  ✅ {routine['message']}")
            print(f"  📋 Routine ID: {routine['routine']['id']}")

        # Demo 4: Energy usage
        print("\n⚡ DEMO 4: Energy Usage Analysis")
        print("-" * 40)

        energy = get_energy_usage()
        print(f"  🔋 Current usage: {energy['current_usage_kw']} kW")
        print(f"  📊 Daily usage: {energy['daily_usage_kwh']} kWh")
        print(f"  💰 Cost today: ${energy['cost_today']}")
        print("  💡 Top recommendations:")
        for i, rec in enumerate(energy["recommendations"][:2], 1):
            print(f"    {i}. {rec}")

        # Demo 5: Security status
        print("\n🔒 DEMO 5: Security System Status")
        print("-" * 40)

        security = check_security_status()
        print(f"  🛡️ Overall status: {security['overall_status'].upper()}")
        print(f"  🚨 System armed: {'YES' if security['armed'] else 'NO'}")
        print("  📋 Recent activity:")
        for activity in security["recent_activity"][:2]:
            print(f"    • {activity['time']}: {activity['event']}")

        # Demo 6: Weather integration
        print("\n🌤️ DEMO 6: Weather-Based Automation")
        print("-" * 40)

        weather = get_weather_integration()
        current = weather["current"]
        print(f"  🌡️ Current: {current['temperature']}°F, {current['conditions']}")
        print(f"  💧 Humidity: {current['humidity']}%")
        print("  🤖 Automation suggestions:")
        for suggestion in weather["automation_recommendations"][:2]:
            print(f"    • {suggestion}")

        # Demo 7: Interactive agent conversation
        print("\n🗣️ DEMO 7: Interactive Agent Conversation")
        print("-" * 40)

        from google.adk.sessions import InMemorySessionService
        from google.adk.memory import InMemoryMemoryService
        from google.adk.runners import Runner
        from google.genai import types

        # Setup services
        session_service = InMemorySessionService()
        memory_service = InMemoryMemoryService()

        # Create session
        session = await session_service.create_session(
            app_name="home_automation_demo",
            user_id="demo_user",
            session_id="demo_session",
        )

        # Create runner
        runner = Runner(
            agent=home_automation_agent,
            app_name="home_automation_demo",
            session_service=session_service,
            memory_service=memory_service,
        )

        # Test query
        test_query = "Show me the status of all my smart home devices and suggest an energy-saving automation routine"
        print(f"  💬 Query: {test_query}")

        content = types.Content(role="user", parts=[types.Part(text=test_query)])

        events = runner.run_async(
            user_id="demo_user", session_id="demo_session", new_message=content
        )

        response_text = ""
        async for event in events:
            if event.is_final_response():
                response_text = event.content.parts[0].text
                break

        print(f"  🤖 Agent Response Preview:")
        print(f"    {response_text[:300]}...")

        print("\n✅ HOME AUTOMATION DEMO COMPLETED!")
        print("\n🌟 Key Features Demonstrated:")
        print("  • 📱 Smart device discovery and control")
        print("  • 🤖 Automation routine creation")
        print("  • ⚡ Energy usage monitoring and optimization")
        print("  • 🔒 Security system integration")
        print("  • 🌤️ Weather-based automation suggestions")
        print("  • 🗣️ Natural language interaction")

    except Exception as e:
        logger.error(f"Demo error: {e}")
        print(f"❌ Demo failed: {e}")


def show_home_automation_examples():
    """Show practical home automation examples."""

    print("\n📚 HOME AUTOMATION EXAMPLES")
    print("=" * 60)

    examples = [
        {
            "title": "🌅 Morning Routine",
            "description": "Automated wake-up sequence",
            "actions": [
                "• Gradually brighten bedroom lights over 15 minutes",
                "• Start coffee maker at 7:00 AM",
                "• Open smart blinds when motion detected",
                "• Display weather and calendar on smart display",
                "• Adjust thermostat to 72°F",
            ],
        },
        {
            "title": "🏃 Leaving Home",
            "description": "Automated departure sequence",
            "actions": [
                "• Turn off all lights except security lighting",
                "• Lock all doors and arm security system",
                "• Set thermostat to away mode (65°F)",
                "• Close garage door if open",
                "• Activate all security cameras",
            ],
        },
        {
            "title": "🌙 Evening Routine",
            "description": "Automated wind-down sequence",
            "actions": [
                "• Dim lights to 30% throughout house",
                "• Close all smart blinds and curtains",
                "• Set thermostat for optimal sleep (68°F)",
                "• Check that all entry points are secure",
                "• Activate sleep mode on all devices",
            ],
        },
        {
            "title": "⚡ Energy Optimization",
            "description": "Smart energy management",
            "actions": [
                "• Automatically adjust HVAC during peak rate hours",
                "• Turn off unnecessary devices when away",
                "• Use smart plugs to eliminate phantom loads",
                "• Optimize water heater schedule",
                "• Coordinate with solar panels and battery storage",
            ],
        },
        {
            "title": "🔒 Security Automation",
            "description": "Intelligent security responses",
            "actions": [
                "• Auto-lock doors at 10 PM if forgotten",
                "• Turn on lights when motion detected at night",
                "• Send alerts for unusual activity patterns",
                "• Automatically disarm when family arrives",
                "• Emergency lighting during power outages",
            ],
        },
    ]

    for example in examples:
        print(f"\n{example['title']}")
        print(f"Description: {example['description']}")
        print("Actions:")
        for action in example["actions"]:
            print(f"  {action}")


if __name__ == "__main__":
    print("🏠 Smart Home Automation Agent")

    # Show examples first
    show_home_automation_examples()

    # Run the demo
    try:
        asyncio.run(demo_home_automation())
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        logger.error(f"Demo error: {e}")
        print(f"❌ Demo failed: {e}")

    print("\n🌐 Try the web interface:")
    print("   adk web agents --port 8084")
    print("   Then visit: http://127.0.0.1:8084")
