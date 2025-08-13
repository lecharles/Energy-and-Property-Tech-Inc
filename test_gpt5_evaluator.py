#!/usr/bin/env python3
"""
Test Script for GPT5 Evaluator Agent

This script tests the GPT5 Evaluator Agent with sample agent responses
to validate the evaluation framework and GPT-5 integration.

Author: Carlos Lozano
Date: August 11, 2025
Phase: 6 - Evaluation Phase
"""

import os
import json
import logging
from datetime import datetime
from gpt5_evaluator_agent import GPT5EvaluatorAgent, EvaluationResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_test_scenarios():
    """Create test scenarios with sample agent responses."""
    
    test_scenarios = [
        {
            "agent_type": "Financial Impact Agent",
            "query": "What is the most profitable region and why?",
            "response": "Based on the financial data analysis, EMEA is the most profitable region with a 23% profit margin. This is driven by strong revenue growth of 18% year-over-year and effective cost optimization initiatives. The region has shown consistent performance improvement over the last three quarters.",
            "expected_focus": "Financial accuracy, data-driven insights, regional analysis"
        },
        {
            "agent_type": "Upsell Discovery Agent", 
            "query": "Identify upsell opportunities in the EMEA region",
            "response": "EMEA region shows significant upsell potential with 45% of customers having only basic product packages. Top opportunities include: 1) Premium monitoring services for 23 customers, 2) Advanced analytics modules for 18 customers, 3) Extended warranty for 31 customers. Estimated total value: €2.4M annually.",
            "expected_focus": "Opportunity identification, customer targeting, value quantification"
        },
        {
            "agent_type": "Operations Summary Agent",
            "query": "Provide operational status and identify critical issues",
            "response": "Current operational status: 94% asset utilization across all regions. Critical issues identified: 1) EMEA region experiencing 15% higher maintenance costs due to aging infrastructure, 2) APAC region showing 8% decrease in lead conversion rates, 3) Americas region operating at optimal efficiency with 98% utilization.",
            "expected_focus": "Operational metrics, issue identification, regional breakdown"
        },
        {
            "agent_type": "Campaign Planner Agent",
            "query": "Create marketing campaign for new energy monitoring products",
            "response": "Marketing Campaign: 'Smart Energy Future' - Target: EMEA commercial customers. Channels: LinkedIn advertising (40% budget), industry conferences (30% budget), email marketing (20% budget), partner referrals (10% budget). Timeline: Q4 2025 launch. Expected ROI: 3.2x with €1.8M projected revenue.",
            "expected_focus": "Marketing strategy, channel selection, financial projections"
        },
        {
            "agent_type": "Synthesis Agent",
            "query": "Provide executive summary of regional performance and growth opportunities",
            "response": "Executive Summary: EMEA leads with 23% profit margin and €2.4M upsell potential. APAC shows growth opportunity with 8% conversion improvement needed. Americas operating optimally at 98% efficiency. Strategic focus: 1) EMEA upsell execution, 2) APAC conversion optimization, 3) Americas efficiency replication. Total growth potential: €4.2M annually.",
            "expected_focus": "Executive insights, strategic recommendations, business impact"
        }
    ]
    
    return test_scenarios


def test_individual_evaluation(evaluator: GPT5EvaluatorAgent, scenario: dict):
    """Test individual agent response evaluation."""
    
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {scenario['agent_type']}")
    print(f"{'='*60}")
    print(f"Query: {scenario['query']}")
    print(f"Response: {scenario['response']}")
    print(f"Expected Focus: {scenario['expected_focus']}")
    
    try:
        # Evaluate the response
        start_time = datetime.now()
        result = evaluator.evaluate_response(
            scenario['agent_type'],
            scenario['query'], 
            scenario['response']
        )
        evaluation_time = (datetime.now() - start_time).total_seconds()
        
        # Display results
        print(f"\n📊 Evaluation Results (Completed in {evaluation_time:.1f}s):")
        print(f"Total Score: {result.total_score}/10")
        print(f"Factuality: {result.factuality_rating}/4 ({result.factuality_points:.1f} pts)")
        print(f"Instruction Following: {result.instruction_following_rating}/4 ({result.instruction_following_points:.1f} pts)")
        print(f"Conciseness: {result.conciseness_rating}/4 ({result.conciseness_points:.1f} pts)")
        print(f"Completeness: {result.completeness_rating}/4 ({result.completeness_points:.1f} pts)")
        
        print(f"\n💬 Overall Assessment:")
        print(f"{result.overall_assessment}")
        
        print(f"\n🔧 Improvement Recommendations:")
        for i, rec in enumerate(result.improvement_recommendations, 1):
            print(f"{i}. {rec}")
        
        return result
        
    except Exception as e:
        print(f"❌ Evaluation failed: {str(e)}")
        logger.error(f"Evaluation failed for {scenario['agent_type']}: {str(e)}")
        return None


def test_batch_evaluation(evaluator: GPT5EvaluatorAgent, scenarios: list):
    """Test batch evaluation of multiple agent responses."""
    
    print(f"\n{'='*60}")
    print(f"🚀 Starting Batch Evaluation of {len(scenarios)} Responses")
    print(f"{'='*60}")
    
    # Prepare batch evaluation data
    batch_data = [
        (s['agent_type'], s['query'], s['response'], None) 
        for s in scenarios
    ]
    
    try:
        # Execute batch evaluation
        start_time = datetime.now()
        results = evaluator.batch_evaluate(batch_data)
        total_time = (datetime.now() - start_time).total_seconds()
        
        print(f"✅ Batch evaluation completed in {total_time:.1f}s")
        print(f"Results: {len(results)}/{len(scenarios)} successful")
        
        return results
        
    except Exception as e:
        print(f"❌ Batch evaluation failed: {str(e)}")
        logger.error(f"Batch evaluation failed: {str(e)}")
        return []


def generate_test_report(results: list, scenarios: list):
    """Generate comprehensive test report."""
    
    if not results:
        print("❌ No results to report")
        return
    
    print(f"\n{'='*60}")
    print(f"📋 Test Report Summary")
    print(f"{'='*60}")
    
    # Calculate statistics
    total_scores = [r.total_score for r in results]
    avg_score = sum(total_scores) / len(total_scores)
    min_score = min(total_scores)
    max_score = max(total_scores)
    
    print(f"📊 Performance Statistics:")
    print(f"- Total Evaluations: {len(results)}")
    print(f"- Average Score: {avg_score:.1f}/10")
    print(f"- Score Range: {min_score}/10 - {max_score}/10")
    print(f"- Success Rate: {len(results)}/{len(scenarios)} ({len(results)/len(scenarios)*100:.1f}%)")
    
    # Agent performance breakdown
    print(f"\n🤖 Agent Performance Breakdown:")
    for result in results:
        print(f"- {result.agent_type}: {result.total_score}/10")
    
    # Save detailed report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"test_reports/gpt5_evaluator_test_report_{timestamp}.json"
    
    try:
        os.makedirs("test_reports", exist_ok=True)
        with open(report_filename, 'w') as f:
            json.dump([r.to_dict() for r in results], f, indent=2)
        print(f"\n💾 Detailed report saved to: {report_filename}")
    except Exception as e:
        print(f"❌ Failed to save report: {str(e)}")
    
    return report_filename


def test_error_handling(evaluator: GPT5EvaluatorAgent):
    """Test error handling and edge cases."""
    
    print(f"\n{'='*60}")
    print(f"⚠️  Testing Error Handling and Edge Cases")
    print(f"{'='*60}")
    
    # Test 1: Invalid model
    try:
        print("Test 1: Invalid model specification...")
        invalid_evaluator = GPT5EvaluatorAgent("dummy_key", "gpt-4")
        print("❌ Should have failed with invalid model")
    except ValueError as e:
        print(f"✅ Correctly rejected invalid model: {str(e)}")
    
    # Test 2: Empty response
    try:
        print("\nTest 2: Empty response evaluation...")
        result = evaluator.evaluate_response("Test Agent", "Test query", "")
        print(f"✅ Empty response evaluated: {result.total_score}/10")
    except Exception as e:
        print(f"❌ Failed to handle empty response: {str(e)}")
    
    # Test 3: Very long response
    try:
        print("\nTest 3: Very long response evaluation...")
        long_response = "This is a very long response. " * 100
        result = evaluator.evaluate_response("Test Agent", "Test query", long_response)
        print(f"✅ Long response evaluated: {result.total_score}/10")
    except Exception as e:
        print(f"❌ Failed to handle long response: {str(e)}")
    
    print("\n✅ Error handling tests completed")


def main():
    """Main test function."""
    
    print("🚀 GPT5 Evaluator Agent - Comprehensive Test Suite")
    print("=" * 60)
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key to run the tests:")
        print("export OPENAI_API_KEY='your_api_key_here'")
        return
    
    try:
        # Initialize evaluator
        print("🔧 Initializing GPT5 Evaluator Agent...")
        evaluator = GPT5EvaluatorAgent(api_key)
        print("✅ GPT5 Evaluator Agent initialized successfully")
        
        # Create test scenarios
        scenarios = create_test_scenarios()
        print(f"📋 Created {len(scenarios)} test scenarios")
        
        # Test individual evaluations
        print(f"\n🧪 Testing Individual Evaluations...")
        individual_results = []
        for scenario in scenarios:
            result = test_individual_evaluation(evaluator, scenario)
            if result:
                individual_results.append(result)
        
        # Test batch evaluation
        print(f"\n🚀 Testing Batch Evaluation...")
        batch_results = test_batch_evaluation(evaluator, scenarios)
        
        # Generate test report
        if individual_results:
            generate_test_report(individual_results, scenarios)
        
        # Test error handling
        test_error_handling(evaluator)
        
        print(f"\n🎉 All tests completed successfully!")
        print(f"Individual evaluations: {len(individual_results)}/{len(scenarios)}")
        print(f"Batch evaluations: {len(batch_results)}/{len(scenarios)}")
        
    except Exception as e:
        print(f"❌ Test suite failed: {str(e)}")
        logger.error(f"Test suite error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
