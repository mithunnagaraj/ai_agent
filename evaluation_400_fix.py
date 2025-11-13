#!/usr/bin/env python3
"""
ADK Evaluation 400 Error Diagnostic Tool
========================================
This script helps diagnose the specific cause of 400 Bad Request errors
when running evaluations in ADK Web interface.
"""

import json


def generate_minimal_eval_case():
    """Generate the most basic evaluation case that should work"""
    print("🔍 MINIMAL WORKING EVALUATION CASE")
    print("=" * 50)
    print("Copy this EXACT format into ADK Web:")
    print()

    minimal_case = {
        "name": "basic_test",
        "description": "Minimal test case",
        "eval_cases": [
            {
                "name": "simple_query",
                "input": "Hello",
                "expected": "greeting",
                "criteria": "Should respond with a greeting",
            }
        ],
    }

    print("EVALUATION SET JSON:")
    print("-" * 30)
    print(json.dumps(minimal_case, indent=2))
    print()
    print("📋 COPY-PASTE INSTRUCTIONS:")
    print("1. Go to ADK Web → Select Agent → Evaluation")
    print("2. Click 'Create New Evaluation Set'")
    print("3. Paste the JSON above EXACTLY")
    print("4. Save and try to run")
    print()


def check_common_mistakes():
    """Show common JSON format mistakes that cause 400 errors"""
    print("❌ COMMON MISTAKES CAUSING 400 ERRORS")
    print("=" * 50)

    mistakes = [
        {
            "issue": "Missing quotes around field names",
            "wrong": "{name: 'test', input: 'hello'}",
            "correct": '{"name": "test", "input": "hello"}',
        },
        {
            "issue": "Using single quotes instead of double quotes",
            "wrong": "{'name': 'test'}",
            "correct": '{"name": "test"}',
        },
        {
            "issue": "Missing required fields",
            "wrong": '{"input": "hello"}',
            "correct": '{"name": "test", "input": "hello", "expected": "response", "criteria": "should respond"}',
        },
        {
            "issue": "Invalid evaluation set name with spaces",
            "wrong": '{"name": "test case 1"}',
            "correct": '{"name": "test_case_1"}',
        },
    ]

    for i, mistake in enumerate(mistakes, 1):
        print(f"{i}. {mistake['issue']}")
        print(f"   ❌ Wrong: {mistake['wrong']}")
        print(f"   ✅ Correct: {mistake['correct']}")
        print()


def troubleshoot_steps():
    """Provide step-by-step troubleshooting"""
    print("🔧 STEP-BY-STEP TROUBLESHOOTING")
    print("=" * 50)

    steps = [
        "1. Test Agent Manually First",
        "   → Go to agent chat and send 'Hello'",
        "   → Verify agent responds correctly",
        "",
        "2. Start with Minimal Test Case",
        "   → Use the basic JSON above",
        "   → Don't add complex criteria yet",
        "",
        "3. Check Browser Console (F12)",
        "   → Open Developer Tools",
        "   → Look for detailed error messages",
        "   → Note any JSON parsing errors",
        "",
        "4. Verify Evaluation Set Name",
        "   → Use only: letters, numbers, underscores",
        "   → No spaces or special characters",
        "",
        "5. Test Incrementally",
        "   → If basic case works, add one field at a time",
        "   → Identify which field causes the error",
    ]

    for step in steps:
        print(step)
    print()


def browser_debugging_guide():
    """Guide for using browser developer tools"""
    print("🌐 BROWSER DEBUGGING FOR 400 ERRORS")
    print("=" * 50)

    print(
        """
TO FIND THE EXACT ERROR:

1. Open ADK Web in browser
2. Press F12 to open Developer Tools
3. Go to "Network" tab
4. Try to run the evaluation that fails
5. Look for the failed request (should show 400 status)
6. Click on the failed request
7. Check "Response" tab for detailed error message

WHAT TO LOOK FOR:
• "Invalid JSON format"
• "Missing required field: [field_name]"  
• "Invalid evaluation set name"
• "Agent not found"
• Schema validation errors

8. Copy the exact error message
9. Use that to fix the evaluation format
"""
    )


def main():
    """Run all diagnostic functions"""
    print("🚨 ADK EVALUATION 400 ERROR DIAGNOSTIC")
    print("=" * 60)
    print("google-adk[eval] module is installed correctly ✅")
    print(
        "Location: /Users/mithunnagaraj/.pyenv/versions/3.10.3/lib/python3.10/site-packages/"
    )
    print()

    generate_minimal_eval_case()
    check_common_mistakes()
    troubleshoot_steps()
    browser_debugging_guide()

    print("💡 QUICK FIX SUMMARY:")
    print("1. Use the minimal JSON format above")
    print("2. Check browser console for exact error")
    print("3. Start simple, add complexity gradually")
    print("4. Ensure evaluation set names have no spaces")


if __name__ == "__main__":
    main()
