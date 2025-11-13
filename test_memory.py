#!/usr/bin/env python3
"""
Simple test guide to demonstrate persistent memory across sessions.
This shows how your agent will remember your name between runs.

To use this guide:
1. Set your API key: export GOOGLE_API_KEY='your-key'
2. Run the main memory demo: python3 memory_mgmt.py
3. Stop and run again - it should remember your name!
"""

import os
import sys


def main():
    """Main function that explains how to test persistent memory."""

    print("🧪 PERSISTENT MEMORY TEST GUIDE")
    print("=" * 50)
    print()

    # Check for API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Please set your Google API key first:")
        print("   export GOOGLE_API_KEY='your-api-key-here'")
        print()

    print("📋 How to test persistent memory:")
    print()
    print("1️⃣  First run:")
    print("   python3 memory_mgmt.py")
    print("   → Tell the agent your name when prompted")
    print()

    print("2️⃣  Stop the script (Ctrl+C)")
    print()

    print("3️⃣  Run again:")
    print("   python3 memory_mgmt.py")
    print("   → Ask: 'What is my name?'")
    print("   → Agent should remember! 🎉")
    print()

    print("🔧 Technical details:")
    print("   • Sessions saved to: agent_sessions.db")
    print("   • Memory auto-saved after each turn")
    print("   • Uses persistent session ID: demo_user_main_session")
    print("   • Agent has preload_memory tool for recall")
    print()

    print("💡 Files to check:")
    print("   • memory_mgmt.py - Main agent with persistent memory")
    print("   • agent.py - CLI version with --dry-run mode")
    print("   • STATEFUL_AGENT_GUIDE.md - Complete setup guide")
    print()

    print("🚀 Quick start:")
    print("   python3 memory_mgmt.py")
    print()


if __name__ == "__main__":
    main()
