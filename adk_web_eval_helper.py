#!/usr/bin/env python3
"""
ADK Web Evaluation Quick Setup Tool
==================================

This script helps you quickly generate test case data that can be
copy-pasted directly into the ADK Web evaluation interface.
"""


def generate_basic_agent_test_cases():
    """Generate formatted test cases for basic agent evaluation"""
    print("🔬 BASIC AGENT TEST CASES FOR ADK WEB")
    print("=" * 60)
    print("Copy and paste these into the ADK Web evaluation interface:\n")

    test_cases = [
        {
            "name": "Simple Factual Query",
            "input": "What is the capital of Japan?",
            "expected": "Should clearly state Tokyo as the capital, provide accurate information",
            "score": "0.9",
        },
        {
            "name": "Current Events Query",
            "input": "Latest news about artificial intelligence in 2024",
            "expected": "Should find recent AI-related news from 2024 with specific examples",
            "score": "0.8",
        },
        {
            "name": "Technical Definition",
            "input": "What is machine learning?",
            "expected": "Should provide clear ML definition with key concepts like algorithms and data",
            "score": "0.85",
        },
        {
            "name": "Comparative Query",
            "input": "Difference between Python and JavaScript programming languages",
            "expected": "Should compare both languages clearly with key differences",
            "score": "0.8",
        },
        {
            "name": "Complex Search Query",
            "input": "Best practices for cloud security in enterprise environments",
            "expected": "Should provide comprehensive security practices for enterprises",
            "score": "0.75",
        },
    ]

    for i, tc in enumerate(test_cases, 1):
        print(f"Test Case {i}: {tc['name']}")
        print(f"Input: {tc['input']}")
        print(f"Expected: {tc['expected']}")
        print(f"Expected Score: {tc['score']}")
        print("-" * 40)


def generate_research_agent_test_cases():
    """Generate formatted test cases for research agent evaluation"""
    print("🔬 RESEARCH AGENT TEST CASES FOR ADK WEB")
    print("=" * 60)
    print("Copy and paste these into the ADK Web evaluation interface:\n")

    test_cases = [
        {
            "name": "Academic Paper Search",
            "input": "Find recent papers on transformer architecture improvements published in 2023-2024",
            "expected": "Should find actual papers with citations and analyze key contributions",
            "score": "0.9",
        },
        {
            "name": "Trend Analysis",
            "input": "Analyze the current trends in quantum computing research and their potential impact",
            "expected": "Should identify trends accurately with analytical insights and implications",
            "score": "0.85",
        },
        {
            "name": "Comparative Analysis",
            "input": "Compare different approaches to energy-efficient AI algorithms and their trade-offs",
            "expected": "Should compare multiple approaches with clear trade-offs discussion",
            "score": "0.8",
        },
        {
            "name": "Multi-Agent Coordination Test",
            "input": "Research the history of neural networks and analyze their evolution timeline",
            "expected": "Should demonstrate coordinated search and analysis with chronological timeline",
            "score": "0.9",
        },
        {
            "name": "Complex Research Task",
            "input": "Investigate the relationship between large language models and computational sustainability",
            "expected": "Should explore multiple aspects with diverse sources and comprehensive analysis",
            "score": "0.85",
        },
    ]

    for i, tc in enumerate(test_cases, 1):
        print(f"Test Case {i}: {tc['name']}")
        print(f"Input: {tc['input']}")
        print(f"Expected: {tc['expected']}")
        print(f"Expected Score: {tc['score']}")
        print("-" * 40)


def generate_home_automation_test_cases():
    """Generate formatted test cases for home automation agent evaluation"""
    print("🔬 HOME AUTOMATION AGENT TEST CASES FOR ADK WEB")
    print("=" * 60)
    print("Copy and paste these into the ADK Web evaluation interface:\n")

    test_cases = [
        {
            "name": "Basic Device Control",
            "input": "Turn on the living room lights and set brightness to 75%",
            "expected": "Should identify device, execute control command, and provide confirmation",
            "score": "0.9",
        },
        {
            "name": "Multi-Device Scenario",
            "input": "Set up a movie night scene: dim lights, close blinds, turn on TV",
            "expected": "Should control multiple devices and coordinate actions properly",
            "score": "0.85",
        },
        {
            "name": "Automation Routine Creation",
            "input": "Create a good morning routine that gradually turns on lights and starts coffee at 7 AM",
            "expected": "Should create scheduled automation with timing and coordinated actions",
            "score": "0.9",
        },
        {
            "name": "Security Management",
            "input": "Show me the security status and arm the alarm system for night mode",
            "expected": "Should display status, control alarm system, and provide confirmation",
            "score": "0.85",
        },
        {
            "name": "Energy Optimization",
            "input": "Analyze energy usage and suggest optimizations for reducing consumption",
            "expected": "Should provide usage data, identify high-consumption devices, suggest optimizations",
            "score": "0.8",
        },
        {
            "name": "Complex Smart Home Scenario",
            "input": "I'm leaving for vacation - secure the house and set energy-saving mode",
            "expected": "Should activate security features and set energy-saving configurations",
            "score": "0.9",
        },
    ]

    for i, tc in enumerate(test_cases, 1):
        print(f"Test Case {i}: {tc['name']}")
        print(f"Input: {tc['input']}")
        print(f"Expected: {tc['expected']}")
        print(f"Expected Score: {tc['score']}")
        print("-" * 40)


def show_adk_web_instructions():
    """Show step-by-step instructions for using evaluations in ADK Web"""
    print("\n🌐 ADK WEB EVALUATION SETUP INSTRUCTIONS")
    print("=" * 60)
    print(
        """
STEP 1: Access ADK Web Interface
• Open: http://127.0.0.1:8085
• You should see three agents: basic_agent, research_agent, home_automation_agent

STEP 2: Select an Agent
• Click on the agent you want to evaluate
• Look for "Evaluation" or "Eval" section in the interface

STEP 3: Create Evaluation Set
• Click "Create New Evaluation" or similar button
• Give your evaluation a descriptive name (e.g., "Basic Search Tests")

STEP 4: Add Test Cases
• For each test case above:
  1. Click "Add Test Case" 
  2. Enter the test name
  3. Paste the input text
  4. Add expected criteria/keywords
  5. Set expected score (0.0 to 1.0)

STEP 5: Run Evaluation
• Click "Run Evaluation" or "Start Tests"
• Monitor progress as each test case executes
• Review results when complete

STEP 6: Analyze Results
• Compare actual vs expected scores
• Review detailed feedback for each test
• Identify areas needing improvement
• Export results for further analysis

📊 EVALUATION METRICS TO WATCH:
• Response Accuracy (keyword matching)
• Response Quality (coherence, completeness)  
• Response Time (efficiency)
• Token Usage (cost optimization)
• Overall Score (weighted average)
"""
    )


def main():
    """Main function to run the evaluation setup tool"""
    print("🧪 ADK WEB EVALUATION QUICK SETUP TOOL")
    print("=" * 60)
    print("Choose an agent to generate test cases for:")
    print("1. Basic Agent (Google search capabilities)")
    print("2. Research Agent (Advanced research and analysis)")
    print("3. Home Automation Agent (Smart home management)")
    print("4. All agents")
    print("5. Show ADK Web instructions only")

    try:
        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            generate_basic_agent_test_cases()
        elif choice == "2":
            generate_research_agent_test_cases()
        elif choice == "3":
            generate_home_automation_test_cases()
        elif choice == "4":
            generate_basic_agent_test_cases()
            print("\n")
            generate_research_agent_test_cases()
            print("\n")
            generate_home_automation_test_cases()
        elif choice == "5":
            show_adk_web_instructions()
        else:
            print("❌ Invalid choice. Please run the script again.")
            return

        show_adk_web_instructions()

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
