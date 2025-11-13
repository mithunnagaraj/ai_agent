"""
Comprehensive Evaluation Test Suites for ADK Agents
===================================================

This file contains structured evaluation test cases for:
1. Basic Agent (Google search capabilities)
2. Research Agent (Advanced research and analysis)
3. Home Automation Agent (Smart home management)

These test suites can be used in the ADK Web evaluation interface
to systematically test and improve agent performance.
"""

# =============================================================================
# BASIC AGENT EVALUATION SUITE
# =============================================================================

BASIC_AGENT_EVAL_SUITE = {
    "suite_name": "Basic Agent Search Capabilities",
    "description": "Tests fundamental Google search and information retrieval",
    "agent_name": "basic_agent",
    "test_cases": [
        {
            "id": "basic_001",
            "name": "Simple Factual Query",
            "input": "What is the capital of Japan?",
            "expected_keywords": ["Tokyo", "capital", "Japan"],
            "criteria": [
                "Response should clearly state Tokyo as the capital",
                "Information should be accurate and up-to-date",
                "Response should be concise and direct",
            ],
            "expected_score": 0.9,
        },
        {
            "id": "basic_002",
            "name": "Current Events Query",
            "input": "Latest news about artificial intelligence in 2024",
            "expected_keywords": [
                "AI",
                "artificial intelligence",
                "2024",
                "news",
                "recent",
            ],
            "criteria": [
                "Should find recent AI-related news",
                "Information should be from 2024",
                "Should provide specific examples or developments",
            ],
            "expected_score": 0.8,
        },
        {
            "id": "basic_003",
            "name": "Technical Definition",
            "input": "What is machine learning?",
            "expected_keywords": [
                "machine learning",
                "algorithms",
                "data",
                "AI",
                "training",
            ],
            "criteria": [
                "Should provide clear definition of ML",
                "Should mention key concepts like algorithms and data",
                "Should be understandable to general audience",
            ],
            "expected_score": 0.85,
        },
        {
            "id": "basic_004",
            "name": "Comparative Query",
            "input": "Difference between Python and JavaScript programming languages",
            "expected_keywords": [
                "Python",
                "JavaScript",
                "difference",
                "programming",
                "language",
            ],
            "criteria": [
                "Should compare both languages clearly",
                "Should mention key differences in usage/features",
                "Should be accurate and balanced",
            ],
            "expected_score": 0.8,
        },
        {
            "id": "basic_005",
            "name": "Complex Search Query",
            "input": "Best practices for cloud security in enterprise environments",
            "expected_keywords": [
                "cloud",
                "security",
                "enterprise",
                "best practices",
                "AWS",
                "Azure",
            ],
            "criteria": [
                "Should provide comprehensive security practices",
                "Should be relevant to enterprise environments",
                "Should include specific recommendations",
            ],
            "expected_score": 0.75,
        },
    ],
}

# =============================================================================
# RESEARCH AGENT EVALUATION SUITE
# =============================================================================

RESEARCH_AGENT_EVAL_SUITE = {
    "suite_name": "Research Agent Advanced Capabilities",
    "description": "Tests advanced research, analysis, and multi-agent coordination",
    "agent_name": "research_agent",
    "test_cases": [
        {
            "id": "research_001",
            "name": "Academic Paper Search",
            "input": "Find recent papers on transformer architecture improvements published in 2023-2024",
            "expected_keywords": [
                "transformer",
                "architecture",
                "papers",
                "2023",
                "2024",
                "research",
            ],
            "criteria": [
                "Should find actual academic papers",
                "Papers should be from specified time period",
                "Should provide proper citations and sources",
                "Should analyze key contributions",
            ],
            "expected_score": 0.9,
        },
        {
            "id": "research_002",
            "name": "Trend Analysis",
            "input": "Analyze the current trends in quantum computing research and their potential impact",
            "expected_keywords": [
                "quantum",
                "computing",
                "trends",
                "analysis",
                "impact",
                "research",
            ],
            "criteria": [
                "Should identify current trends accurately",
                "Should provide analytical insights",
                "Should discuss future implications",
                "Should cite relevant sources",
            ],
            "expected_score": 0.85,
        },
        {
            "id": "research_003",
            "name": "Comparative Analysis",
            "input": "Compare different approaches to energy-efficient AI algorithms and their trade-offs",
            "expected_keywords": [
                "energy",
                "efficient",
                "AI",
                "algorithms",
                "compare",
                "trade-offs",
            ],
            "criteria": [
                "Should compare multiple approaches",
                "Should discuss trade-offs clearly",
                "Should be technically accurate",
                "Should provide balanced analysis",
            ],
            "expected_score": 0.8,
        },
        {
            "id": "research_004",
            "name": "Multi-Agent Coordination Test",
            "input": "Research the history of neural networks and analyze their evolution timeline",
            "expected_keywords": [
                "neural networks",
                "history",
                "evolution",
                "timeline",
                "analysis",
            ],
            "criteria": [
                "Should demonstrate search agent finding sources",
                "Should show analysis agent processing information",
                "Should provide chronological timeline",
                "Should synthesize information coherently",
            ],
            "expected_score": 0.9,
        },
        {
            "id": "research_005",
            "name": "Complex Research Task",
            "input": "Investigate the relationship between large language models and computational sustainability",
            "expected_keywords": [
                "LLM",
                "language models",
                "sustainability",
                "computational",
                "energy",
            ],
            "criteria": [
                "Should explore multiple aspects of the topic",
                "Should find diverse, credible sources",
                "Should provide comprehensive analysis",
                "Should discuss environmental implications",
            ],
            "expected_score": 0.85,
        },
    ],
}

# =============================================================================
# HOME AUTOMATION AGENT EVALUATION SUITE
# =============================================================================

HOME_AUTOMATION_EVAL_SUITE = {
    "suite_name": "Home Automation Agent Smart Home Management",
    "description": "Tests smart home device control, automation, and security features",
    "agent_name": "home_automation_agent",
    "test_cases": [
        {
            "id": "home_001",
            "name": "Basic Device Control",
            "input": "Turn on the living room lights and set brightness to 75%",
            "expected_keywords": ["living room", "lights", "on", "75%", "brightness"],
            "criteria": [
                "Should identify specific device location",
                "Should execute control command correctly",
                "Should set precise brightness level",
                "Should provide confirmation of action",
            ],
            "expected_score": 0.9,
        },
        {
            "id": "home_002",
            "name": "Multi-Device Scenario",
            "input": "Set up a movie night scene: dim lights, close blinds, turn on TV",
            "expected_keywords": ["movie", "scene", "dim", "lights", "blinds", "TV"],
            "criteria": [
                "Should control multiple devices",
                "Should coordinate actions properly",
                "Should create appropriate ambiance",
                "Should confirm all actions completed",
            ],
            "expected_score": 0.85,
        },
        {
            "id": "home_003",
            "name": "Automation Routine Creation",
            "input": "Create a good morning routine that gradually turns on lights and starts coffee at 7 AM",
            "expected_keywords": [
                "morning",
                "routine",
                "lights",
                "coffee",
                "7 AM",
                "gradual",
            ],
            "criteria": [
                "Should create scheduled automation",
                "Should specify timing correctly",
                "Should include multiple coordinated actions",
                "Should save routine for future use",
            ],
            "expected_score": 0.9,
        },
        {
            "id": "home_004",
            "name": "Security Management",
            "input": "Show me the security status and arm the alarm system for night mode",
            "expected_keywords": ["security", "status", "alarm", "arm", "night mode"],
            "criteria": [
                "Should display current security status",
                "Should control alarm system properly",
                "Should set appropriate night mode configuration",
                "Should provide security confirmation",
            ],
            "expected_score": 0.85,
        },
        {
            "id": "home_005",
            "name": "Energy Optimization",
            "input": "Analyze energy usage and suggest optimizations for reducing consumption",
            "expected_keywords": [
                "energy",
                "usage",
                "analyze",
                "optimization",
                "reduce",
                "consumption",
            ],
            "criteria": [
                "Should provide energy usage data",
                "Should identify high-consumption devices",
                "Should suggest specific optimizations",
                "Should quantify potential savings",
            ],
            "expected_score": 0.8,
        },
        {
            "id": "home_006",
            "name": "Complex Smart Home Scenario",
            "input": "I'm leaving for vacation - secure the house and set energy-saving mode",
            "expected_keywords": [
                "vacation",
                "secure",
                "house",
                "energy-saving",
                "away",
            ],
            "criteria": [
                "Should activate security features",
                "Should set energy-saving configurations",
                "Should handle extended absence scenario",
                "Should provide comprehensive vacation setup",
            ],
            "expected_score": 0.9,
        },
    ],
}

# =============================================================================
# EVALUATION UTILITY FUNCTIONS
# =============================================================================


def print_eval_suite_summary():
    """Print a summary of all evaluation suites"""
    print("🧪 ADK AGENT EVALUATION SUITES SUMMARY")
    print("=" * 60)

    suites = [
        BASIC_AGENT_EVAL_SUITE,
        RESEARCH_AGENT_EVAL_SUITE,
        HOME_AUTOMATION_EVAL_SUITE,
    ]

    for suite in suites:
        print(f"\n📊 {suite['suite_name']}")
        print(f"Agent: {suite['agent_name']}")
        print(f"Description: {suite['description']}")
        print(f"Test Cases: {len(suite['test_cases'])}")

        avg_expected_score = sum(
            tc["expected_score"] for tc in suite["test_cases"]
        ) / len(suite["test_cases"])
        print(f"Average Expected Score: {avg_expected_score:.2f}")

        print("\nTest Case IDs:")
        for tc in suite["test_cases"]:
            print(f"  • {tc['id']}: {tc['name']}")


def export_eval_suite_for_adk_web(suite_name):
    """Export evaluation suite in ADK Web compatible format"""
    suites = {
        "basic": BASIC_AGENT_EVAL_SUITE,
        "research": RESEARCH_AGENT_EVAL_SUITE,
        "home": HOME_AUTOMATION_EVAL_SUITE,
    }

    if suite_name not in suites:
        print(f"❌ Suite '{suite_name}' not found. Available: {list(suites.keys())}")
        return None

    suite = suites[suite_name]
    print(f"📤 Exporting {suite['suite_name']} for ADK Web")
    print("=" * 60)

    for i, tc in enumerate(suite["test_cases"], 1):
        print(f"\n🧪 Test Case {i}: {tc['name']}")
        print(f"Input: {tc['input']}")
        print(f"Expected Keywords: {', '.join(tc['expected_keywords'])}")
        print(f"Expected Score: {tc['expected_score']}")
        print("Criteria:")
        for criterion in tc["criteria"]:
            print(f"  • {criterion}")
        print("-" * 40)


# =============================================================================
# USAGE INSTRUCTIONS
# =============================================================================

USAGE_INSTRUCTIONS = """
🔧 HOW TO USE THESE EVALUATION SUITES IN ADK WEB
============================================================

1. 🌐 ACCESS ADK WEB INTERFACE:
   • Start ADK web server: adk web agents --port 8085
   • Visit: http://127.0.0.1:8085
   • Select the agent you want to evaluate

2. 📊 CREATE EVALUATION SETS:
   • Look for "Evaluation" or "Eval" section in the agent interface
   • Click "Create New Evaluation" or "Add Eval Set"
   • Copy test cases from the suites above

3. 🧪 RUN EVALUATIONS:
   • Select evaluation set to run
   • Monitor progress as tests execute
   • Review results and performance metrics

4. 📈 ANALYZE RESULTS:
   • Compare actual vs expected scores
   • Identify areas for improvement
   • Track performance over time
   • Export results for analysis

5. 🔄 ITERATE AND IMPROVE:
   • Modify agent instructions based on results
   • Add new test cases for edge cases
   • Re-run evaluations to validate improvements
   • Create regression test suites

📋 EVALUATION BEST PRACTICES:
• Start with basic test cases before complex ones
• Use diverse input types and complexity levels
• Set realistic expected scores (0.7-0.9 range)
• Include both positive and negative test scenarios
• Document criteria clearly for consistent evaluation
• Regular re-evaluation to prevent regression

💡 TIPS FOR EFFECTIVE EVALUATION:
• Test one capability at a time for clarity
• Use specific, measurable success criteria
• Include edge cases and error scenarios
• Balance thoroughness with execution time
• Keep evaluation data for trend analysis
"""

if __name__ == "__main__":
    print_eval_suite_summary()
    print("\n" + USAGE_INSTRUCTIONS)

    print("\n🚀 QUICK START:")
    print("1. Choose a suite to export: basic, research, or home")
    print("2. Run: python3 evaluation_test_suites.py")
    print("3. Copy test cases to ADK Web evaluation interface")
    print("4. Execute evaluations and analyze results")
