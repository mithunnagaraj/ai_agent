"""
Home Automation Agent for ADK Web Interface
Advanced smart home management and automation assistant.
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search, preload_memory
from google.genai import types
from typing import List, Dict, Any, Optional
import logging
import json
from datetime import datetime, timedelta

# Configure logging
logger = logging.getLogger(__name__)

# Retry configuration for robust API calls
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


# Smart Home Device Management Tools
def list_smart_devices() -> List[Dict[str, Any]]:
    """
    List all connected smart home devices.

    Returns:
        List of smart devices with their current status
    """
    logger.info("Listing smart home devices")

    # Simulated smart home devices - in real implementation, this would connect to actual APIs
    devices = [
        {
            "id": "living_room_lights",
            "name": "Living Room Lights",
            "type": "lights",
            "brand": "Philips Hue",
            "status": "on",
            "brightness": 75,
            "color": "warm_white",
            "room": "living_room",
        },
        {
            "id": "bedroom_thermostat",
            "name": "Bedroom Thermostat",
            "type": "thermostat",
            "brand": "Nest",
            "status": "heating",
            "current_temp": 68,
            "target_temp": 72,
            "room": "bedroom",
        },
        {
            "id": "front_door_lock",
            "name": "Front Door Smart Lock",
            "type": "lock",
            "brand": "August",
            "status": "locked",
            "battery_level": 85,
            "room": "entrance",
        },
        {
            "id": "kitchen_camera",
            "name": "Kitchen Security Camera",
            "type": "camera",
            "brand": "Ring",
            "status": "recording",
            "motion_detected": False,
            "room": "kitchen",
        },
        {
            "id": "garage_door",
            "name": "Garage Door Opener",
            "type": "garage_door",
            "brand": "Chamberlain",
            "status": "closed",
            "room": "garage",
        },
    ]

    logger.debug(f"Found {len(devices)} smart devices")
    return devices


def control_device(device_id: str, action: str, value: str = "") -> Dict[str, Any]:
    """
    Control a smart home device.

    Args:
        device_id: Unique identifier for the device (e.g., "living_room_lights")
        action: Action to perform (e.g., "on", "off", "set_temperature", "lock", "unlock")
        value: Optional value for the action (e.g., "75" for brightness, "72" for temperature)

    Returns:
        Result of the device control action
    """
    logger.info(f"Controlling device {device_id} with action {action}")

    devices = list_smart_devices()
    device = next((d for d in devices if d["id"] == device_id), None)

    if not device:
        return {"success": False, "error": f"Device {device_id} not found"}

    # Simulate device control actions
    result = {"success": True, "device": device["name"], "action": action}

    if device["type"] == "lights":
        if action == "on":
            result["status"] = "Light turned on"
            if value and value.isdigit():
                result["brightness"] = f"{value}%"
        elif action == "off":
            result["status"] = "Light turned off"
        elif action == "set_brightness":
            brightness = int(value) if value and value.isdigit() else 50
            result["status"] = f"Brightness set to {brightness}%"

    elif device["type"] == "thermostat":
        if action == "set_temperature":
            temp = int(value) if value and value.isdigit() else 70
            result["status"] = f"Temperature set to {temp}°F"

    elif device["type"] == "lock":
        if action == "lock":
            result["status"] = "Door locked"
        elif action == "unlock":
            result["status"] = "Door unlocked"

    elif device["type"] == "garage_door":
        if action == "open":
            result["status"] = "Garage door opening"
        elif action == "close":
            result["status"] = "Garage door closing"

    logger.debug(f"Device control result: {result}")
    return result


def create_automation_routine(
    name: str, trigger: str, actions_description: str = "Multiple smart home actions"
) -> Dict[str, Any]:
    """
    Create a home automation routine.

    Args:
        name: Name of the automation routine (e.g., "Good Morning", "Bedtime")
        trigger: What triggers the routine (e.g., "time:7:00 AM", "sensor:motion", "manual")
        actions_description: Description of actions to perform when triggered

    Returns:
        Created automation routine details
    """
    logger.info(f"Creating automation routine: {name}")

    routine = {
        "id": f"routine_{name.lower().replace(' ', '_')}",
        "name": name,
        "trigger": trigger,
        "actions_description": actions_description,
        "created_at": datetime.now().isoformat(),
        "enabled": True,
        "last_run": None,
    }

    logger.debug(f"Created routine: {routine}")
    return {
        "success": True,
        "routine": routine,
        "message": f"Automation routine '{name}' created successfully",
    }


def get_energy_usage() -> Dict[str, Any]:
    """
    Get current energy usage statistics for smart home devices.

    Returns:
        Energy usage data and recommendations
    """
    logger.info("Retrieving energy usage data")

    # Simulated energy data - in real implementation, this would connect to smart meters/devices
    energy_data = {
        "current_usage_kw": 2.3,
        "daily_usage_kwh": 28.5,
        "monthly_usage_kwh": 847,
        "cost_today": 3.42,
        "cost_month": 101.64,
        "peak_hours": ["6:00 PM", "7:00 PM", "8:00 PM"],
        "device_breakdown": {
            "HVAC": {"usage_kwh": 15.2, "percentage": 53.3},
            "Lighting": {"usage_kwh": 3.8, "percentage": 13.3},
            "Kitchen Appliances": {"usage_kwh": 4.1, "percentage": 14.4},
            "Entertainment": {"usage_kwh": 2.9, "percentage": 10.2},
            "Other": {"usage_kwh": 2.5, "percentage": 8.8},
        },
        "recommendations": [
            "Consider lowering thermostat by 2°F during peak hours to save $12/month",
            "LED bulb upgrades could save $8/month on lighting costs",
            "Smart power strips could reduce phantom loads by 5-10%",
        ],
    }

    logger.debug(
        f"Energy usage data retrieved: {energy_data['current_usage_kw']} kW current"
    )
    return energy_data


def check_security_status() -> Dict[str, Any]:
    """
    Check the security status of all home security devices.

    Returns:
        Security status and alerts
    """
    logger.info("Checking home security status")

    security_status = {
        "overall_status": "secure",
        "armed": True,
        "devices": {
            "door_locks": {
                "front_door": {"status": "locked", "battery": 85},
                "back_door": {"status": "locked", "battery": 78},
            },
            "cameras": {
                "kitchen": {"status": "recording", "motion": False},
                "front_yard": {"status": "recording", "motion": False},
                "backyard": {
                    "status": "recording",
                    "motion": True,
                    "alert": "Cat detected",
                },
            },
            "sensors": {
                "motion_living_room": {"status": "clear"},
                "door_bedroom": {"status": "closed"},
                "window_kitchen": {"status": "closed"},
            },
        },
        "recent_activity": [
            {"time": "2:30 PM", "event": "Front door unlocked (mobile app)"},
            {"time": "2:28 PM", "event": "Motion detected - backyard camera"},
            {"time": "1:45 PM", "event": "Kitchen window opened"},
        ],
        "alerts": [
            {"level": "info", "message": "All entry points secure"},
            {"level": "low", "message": "Backyard motion - likely animal"},
        ],
    }

    logger.debug(f"Security status: {security_status['overall_status']}")
    return security_status


def get_weather_integration() -> Dict[str, Any]:
    """
    Get weather data for home automation integration.

    Returns:
        Weather data relevant for home automation decisions
    """
    logger.info("Getting weather data for automation")

    # Simulated weather data - in real implementation, would use weather API
    weather_data = {
        "current": {
            "temperature": 45,
            "humidity": 68,
            "conditions": "partly_cloudy",
            "wind_speed": 8,
            "uv_index": 3,
        },
        "forecast_24h": {
            "high": 52,
            "low": 38,
            "precipitation_chance": 20,
            "conditions": "sunny",
        },
        "automation_recommendations": [
            "Temperature dropping tonight - consider pre-heating home at 6 PM",
            "Low humidity - smart humidifiers can activate automatically",
            "UV index moderate - smart blinds can adjust for optimal lighting",
        ],
        "energy_impact": {
            "heating_hours_needed": 6,
            "cooling_hours_needed": 0,
            "natural_light_available": "good",
            "solar_generation_forecast": "moderate",
        },
    }

    logger.debug(
        f"Weather data: {weather_data['current']['temperature']}°F, {weather_data['current']['conditions']}"
    )
    return weather_data


# Create specialized smart home agents
device_control_agent = LlmAgent(
    name="device_control_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="Smart device control and management specialist",
    instruction="""You are a smart home device control specialist. Your role is to:

1. Help users control individual smart home devices (lights, thermostats, locks, etc.)
2. Provide device status and diagnostics
3. Troubleshoot device connectivity issues  
4. Recommend device settings for comfort and efficiency
5. Explain device features and capabilities

Always prioritize user safety and energy efficiency in your recommendations.""",
    tools=[list_smart_devices, control_device],
)

automation_agent = LlmAgent(
    name="automation_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="Home automation routine and scheduling specialist",
    instruction="""You are a home automation specialist. Your expertise includes:

1. Creating custom automation routines and schedules
2. Setting up smart triggers (time, sensor, location-based)
3. Integrating multiple devices for coordinated actions
4. Optimizing routines for energy savings and convenience
5. Troubleshooting automation issues

Focus on creating practical, user-friendly automations that enhance daily life.""",
    tools=[create_automation_routine, get_energy_usage, get_weather_integration],
)

security_agent = LlmAgent(
    name="security_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="Home security and monitoring specialist",
    instruction="""You are a home security expert. Your responsibilities include:

1. Monitoring security device status and alerts
2. Providing security recommendations and best practices
3. Analyzing security events and patterns
4. Helping configure security settings and notifications
5. Emergency response guidance

Always prioritize home safety and security in your advice.""",
    tools=[check_security_status, list_smart_devices],
)

# Main home automation agent
home_automation_agent = LlmAgent(
    name="smart_home_assistant",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="🏠 Smart Home & Automation Assistant",
    instruction="""You are an advanced smart home assistant with comprehensive home automation capabilities.

WORKFLOW:
1. Use device_control_agent for individual device management and control
2. Use automation_agent for creating routines, schedules, and energy optimization
3. Use security_agent for security monitoring and safety concerns  
4. Use preload_memory to remember user preferences and home configuration
5. Provide integrated smart home solutions that combine devices, automation, and security

CAPABILITIES:
- 💡 Lighting control and scenes
- 🌡️ Climate and temperature management
- 🔒 Security and access control  
- 📹 Camera and monitoring systems
- ⚡ Energy usage optimization
- 🤖 Automation routines and scheduling
- 🌤️ Weather-based automation
- 📱 Smart device integration

EXAMPLES:
- "Turn on the living room lights and set them to 60% brightness"
- "Create a good morning routine that opens blinds and starts coffee" 
- "Show me my energy usage and suggest ways to save money"
- "Check if all doors are locked and arm the security system"
- "Set up an automation to turn off all lights when I leave home"
- "What's the status of my smart home devices?"

IMPORTANT: Always consider safety, security, and energy efficiency. Ask for clarification when device names or actions are ambiguous.""",
    tools=[
        AgentTool(agent=device_control_agent),
        AgentTool(agent=automation_agent),
        AgentTool(agent=security_agent),
        preload_memory,
        list_smart_devices,
        control_device,
        create_automation_routine,
        get_energy_usage,
        check_security_status,
        get_weather_integration,
    ],
)

# ADK Web expects 'root_agent' as the main agent variable
root_agent = home_automation_agent
