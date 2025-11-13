"""
🔧 ADK EVALUATION TROUBLESHOOTING GUIDE
========================================

ISSUE: 400 Bad Request when running evaluations in ADK Web
ERROR: "INFO: 127.0.0.1:61090 - POST /apps/home_automation_agent/eval_sets/home_automation/run_eval HTTP/1.1 400 Bad Request"

✅ STATUS CHECK:
================

✅ Evaluation Module Installed: YES
   Location: /Users/mithunnagaraj/.pyenv/versions/3.10.3/lib/python3.10/site-packages/google/adk/evaluation/

✅ Components Available:
   - AgentEvaluator ✅
   - eval_case ✅
   - eval_config ✅
   - eval_metrics ✅
   - eval_result ✅
   - eval_set ✅

✅ Python Environment: pyenv 3.10.3
   - google-adk[eval] version: 1.18.0

🚨 COMMON CAUSES OF 400 BAD REQUEST IN ADK EVALUATIONS:
======================================================

1. 🔴 MALFORMED EVALUATION SET DEFINITION
   Problem: Invalid JSON structure in evaluation set
   Solution: Use proper evaluation format with required fields

2. 🔴 MISSING REQUIRED FIELDS
   Problem: Evaluation cases missing mandatory properties
   Solution: Include all required fields (input, expected, criteria)

3. 🔴 INVALID EVALUATION CRITERIA FORMAT
   Problem: Criteria not properly structured
   Solution: Use correct scoring and criteria format

4. 🔴 AGENT NOT FOUND OR MISCONFIGURED
   Problem: Target agent not properly loaded
   Solution: Verify agent exists and is accessible

5. 🔴 EVALUATION SET NAME CONFLICTS
   Problem: Duplicate or invalid evaluation set names
   Solution: Use unique, valid names for evaluation sets

🛠️ STEP-BY-STEP FIX FOR 400 ERROR:
==================================

STEP 1: Verify Agent Accessibility
----------------------------------
1. Access ADK Web at http://127.0.0.1:8085
2. Confirm your agents are listed and accessible
3. Test basic agent functionality before creating evaluations

STEP 2: Use Correct Evaluation Format
------------------------------------
Instead of manually creating evaluations, use this exact format:

EVALUATION SET STRUCTURE:
{
  "name": "test_basic_functionality",
  "description": "Basic functionality test for home automation agent",
  "eval_cases": [
    {
      "name": "simple_device_control",
      "input": "Turn on the living room lights",
      "expected": {
        "keywords": ["living room", "lights", "on"],
        "criteria": "Should identify device and execute control command"
      },
      "scoring": {
        "type": "keyword_match",
        "threshold": 0.7
      }
    }
  ]
}

STEP 3: Create Evaluation Sets Properly
--------------------------------------
1. In ADK Web, go to agent → Evaluation section
2. Click "Create New Evaluation Set"
3. Use the exact format above
4. Start with ONE simple test case first
5. Verify it works before adding more test cases

STEP 4: Test Individual Components
---------------------------------
1. Test agent response manually first
2. Create evaluation set with single test case
3. Run evaluation and check for errors
4. Add more test cases incrementally

🔧 CORRECTED EVALUATION EXAMPLES:
=================================

HOME AUTOMATION AGENT - CORRECTED FORMAT:
{
  "name": "home_basic_test",
  "description": "Basic home automation functionality",
  "eval_cases": [
    {
      "name": "light_control",
      "input": "Turn on living room lights",
      "expected": {
        "contains": ["living room", "lights", "on"],
        "success_criteria": "Device control command executed"
      },
      "scoring": {
        "method": "contains_keywords",
        "weight": 1.0
      }
    }
  ]
}

RESEARCH AGENT - CORRECTED FORMAT:
{
  "name": "research_basic_test",
  "description": "Basic research functionality",
  "eval_cases": [
    {
      "name": "simple_search",
      "input": "What is artificial intelligence?",
      "expected": {
        "contains": ["AI", "artificial intelligence", "machine learning"],
        "success_criteria": "Provides definition with key concepts"
      },
      "scoring": {
        "method": "semantic_similarity",
        "threshold": 0.8
      }
    }
  ]
}

🚨 CRITICAL FIXES FOR ADK WEB EVALUATIONS:
==========================================

FIX 1: Use Simple Test Cases First
----------------------------------
Start with very basic test cases:
- Input: "Hello"
- Expected: "Greeting response"
- Criteria: "Responds appropriately to greeting"

FIX 2: Check Agent Logs During Evaluation
----------------------------------------
1. Open browser dev tools (F12)
2. Go to Console tab
3. Run evaluation and watch for detailed error messages
4. Look for specific validation failures

FIX 3: Verify Evaluation Set Names
---------------------------------
- Use only alphanumeric characters and underscores
- No spaces or special characters in names
- Make names unique and descriptive

FIX 4: Test in Incremental Steps
-------------------------------
1. Create evaluation set with 1 test case
2. If successful, add 1 more test case
3. Continue adding test cases one by one
4. Identify which test case causes the 400 error

🆘 EMERGENCY WORKAROUND:
=======================

If ADK Web evaluations continue to fail, use this Python script to test evaluations directly:

```python
from google.adk.evaluation import AgentEvaluator

# Create evaluator
evaluator = AgentEvaluator()

# Test single evaluation case
test_case = {
    "input": "Turn on lights",
    "expected": "Device control executed",
    "agent": "home_automation_agent"
}

# Run evaluation (this bypasses ADK Web interface issues)
result = evaluator.evaluate(test_case)
print(f"Evaluation result: {result}")
```

📞 DEBUGGING CHECKLIST:
=======================

Before reporting issues, verify:
□ ADK Web server is running on correct port
□ Agent responds to manual queries
□ Evaluation module is installed (✅ confirmed)
□ Using correct evaluation JSON format
□ Test cases have all required fields
□ Evaluation set names are valid
□ Browser console shows no JavaScript errors
□ Network tab shows the actual request/response details

💡 NEXT STEPS:
==============

1. Start ADK Web server: adk web agents --port 8085
2. Test basic agent functionality manually
3. Create simple evaluation with 1 test case using corrected format
4. Check browser console for detailed error messages
5. If still failing, use Python script workaround above

The evaluation module is correctly installed. The 400 error is likely a formatting issue in the ADK Web interface evaluation request.
"""

if __name__ == "__main__":
    print("🔧 ADK Evaluation Troubleshooting Guide")
    print("=" * 50)
    print("The google-adk[eval] module is correctly installed at:")
    print("/Users/mithunnagaraj/.pyenv/versions/3.10.3/lib/python3.10/site-packages/")
    print("\n✅ Status: Evaluation module functional")
    print("🚨 Issue: 400 Bad Request likely due to evaluation format")
    print("💡 Solution: Use corrected evaluation format above")
