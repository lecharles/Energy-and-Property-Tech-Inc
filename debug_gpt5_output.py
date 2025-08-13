#!/usr/bin/env python3
"""
Debug GPT-5 Output

This script tests the GPT-5 evaluation output to see exactly
what format it's returning so we can fix the parsing issue.

Author: Carlos Lozano
Date: August 11, 2025
Phase: 6 - Evaluation Phase
"""

import os
import openai
from openai import OpenAI


def test_gpt5_evaluation_output():
    """Test what GPT-5 actually returns for evaluation."""
    
    print("🔍 Debugging GPT-5 Evaluation Output")
    print("=" * 50)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Initialize client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Load system prompt
    with open("System Prompts/GPT5-Evaluator-Agent-System-Prompt.md", "r") as f:
        system_prompt = f.read()
    
    # Test evaluation prompt
    test_prompt = """Please evaluate the following agent response according to the evaluation framework.

AGENT TYPE: Financial Impact Agent
USER QUERY: What is the most profitable region and why?

AGENT RESPONSE:
Based on the financial data analysis, EMEA is the most profitable region with a 23% profit margin. This is driven by strong revenue growth of 18% year-over-year and effective cost optimization initiatives. The region has shown consistent performance improvement over the last three quarters.

IMPORTANT: Pay special attention to Data Source Validation - verify that the agent response references legitimate business data sources (Income Statement, Balance Sheet, Cash Flow, Installed Assets, Lead Funnel, Products) rather than making generic statements or hallucinations.

Please provide your evaluation in the exact format specified in the system prompt, including:
1. The evaluation table with ratings and points
2. Detailed assessment for each criterion (especially Data Source Validation)
3. Overall assessment
4. Improvement recommendations

Remember to use the 1-4 scale for each criterion and calculate the weighted 1-10 total score."""
    
    print("📤 Sending evaluation request to GPT-5...")
    print(f"System prompt length: {len(system_prompt)} characters")
    print(f"Test prompt length: {len(test_prompt)} characters")
    
    try:
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": test_prompt}
            ],
            max_completion_tokens=2000
        )
        
        result = response.choices[0].message.content
        
        print("\n📥 GPT-5 Response Received:")
        print("=" * 50)
        print(result)
        print("=" * 50)
        
        # Save raw output for analysis
        with open("debug_gpt5_output.txt", "w") as f:
            f.write(result)
        
        print(f"\n💾 Raw output saved to debug_gpt5_output.txt")
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


if __name__ == "__main__":
    test_gpt5_evaluation_output()
