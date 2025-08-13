#!/usr/bin/env python3
"""
Test Script for GPT5 Evaluator Agent Storage System

This script tests the new organized storage system for evaluation results,
demonstrating individual and batch evaluation storage capabilities.

Author: Carlos Lozano
Date: August 13, 2025
Phase: 6 - Evaluation Phase
"""

import os
import json
from datetime import datetime
from gpt5_evaluator_agent import GPT5EvaluatorAgent


def test_evaluation_storage():
    """Test the evaluation storage system."""
    
    print("🧪 Testing GPT5 Evaluator Agent Storage System")
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
        
        # Test 1: Individual evaluation storage
        print(f"\n{'='*60}")
        print(f"🧪 Test 1: Individual Evaluation Storage")
        print(f"{'='*60}")
        
        test_scenarios = [
            {
                "agent_type": "Financial Impact Agent",
                "query": "What is the most profitable region?",
                "response": "Based on the financial data analysis, EMEA is the most profitable region with a 23% profit margin."
            },
            {
                "agent_type": "Upsell Discovery Agent", 
                "query": "Identify upsell opportunities in EMEA",
                "response": "EMEA region shows significant upsell potential with 45% of customers having only basic product packages."
            },
            {
                "agent_type": "Operations Summary Agent",
                "query": "Provide operational status overview",
                "response": "Current operational status: 94% asset utilization across all regions with critical issues identified."
            }
        ]
        
        individual_results = []
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n🧪 Evaluating {scenario['agent_type']}...")
            
            try:
                result = evaluator.evaluate_response(
                    scenario['agent_type'],
                    scenario['query'],
                    scenario['response']
                )
                
                print(f"✅ Evaluation completed - Score: {result.total_score}/10")
                
                # Save individual result
                saved_filepath = evaluator.save_evaluation_result(result)
                print(f"💾 Saved to: {saved_filepath}")
                
                individual_results.append(result)
                
            except Exception as e:
                print(f"❌ Failed to evaluate {scenario['agent_type']}: {str(e)}")
        
        # Test 2: Batch evaluation storage
        print(f"\n{'='*60}")
        print(f"🧪 Test 2: Batch Evaluation Storage")
        print(f"{'='*60}")
        
        if individual_results:
            print(f"📊 Saving batch evaluation results...")
            batch_filepath = evaluator.save_batch_evaluation_results(
                individual_results, 
                "demo_batch_evaluation"
            )
            print(f"💾 Batch results saved to: {batch_filepath}")
        
        # Test 3: List and retrieve evaluation results
        print(f"\n{'='*60}")
        print(f"🧪 Test 3: List and Retrieve Evaluation Results")
        print(f"{'='*60}")
        
        print("📁 Available evaluation results:")
        results_list = evaluator.list_evaluation_results(limit=10)
        
        if not results_list:
            print("   No evaluation results found.")
        else:
            for result_meta in results_list:
                if result_meta['type'] == 'individual':
                    print(f"   📄 {result_meta['filename']}")
                    print(f"      Agent: {result_meta['agent_type']}")
                    print(f"      Score: {result_meta['total_score']}/10")
                    print(f"      Time: {result_meta['timestamp']}")
                else:
                    print(f"   📊 {result_meta['filename']}")
                    print(f"      Type: Batch Evaluation")
                    print(f"      Count: {result_meta['total_evaluations']} evaluations")
                    print(f"      Average: {result_meta['average_score']:.1f}/10")
                    print(f"      Time: {result_meta['timestamp']}")
                print()
        
        # Test 4: Retrieve specific evaluation result
        if results_list:
            print(f"🧪 Test 4: Retrieve Specific Evaluation Result")
            print(f"{'='*60}")
            
            first_result = results_list[0]
            filename = first_result['filename']
            
            try:
                retrieved_data = evaluator.get_evaluation_result(filename)
                print(f"✅ Successfully retrieved: {filename}")
                print(f"   Data type: {type(retrieved_data)}")
                print(f"   Keys: {list(retrieved_data.keys()) if isinstance(retrieved_data, dict) else 'Not a dict'}")
                
            except Exception as e:
                print(f"❌ Failed to retrieve {filename}: {str(e)}")
        
        # Test 5: Generate evaluation report
        print(f"\n{'='*60}")
        print(f"🧪 Test 5: Generate Evaluation Report")
        print(f"{'='*60}")
        
        if individual_results:
            report = evaluator.generate_evaluation_report(individual_results)
            print("📊 Generated evaluation report:")
            print(report[:500] + "..." if len(report) > 500 else report)
            
            # Save report to evaluation_results folder
            evaluation_dir = "evaluation_results"
            os.makedirs(evaluation_dir, exist_ok=True)
            
            report_filename = f"evaluation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            report_filepath = os.path.join(evaluation_dir, report_filename)
            
            with open(report_filepath, 'w') as f:
                f.write(report)
            print(f"\n💾 Report saved to: {report_filepath}")
        
        print(f"\n🎉 All storage system tests completed successfully!")
        
        # Final summary
        print(f"\n📊 Storage System Summary:")
        print(f"   Individual evaluations: {len([r for r in results_list if r['type'] == 'individual'])}")
        print(f"   Batch evaluations: {len([r for r in results_list if r['type'] == 'batch'])}")
        print(f"   Total files: {len(results_list)}")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        raise


if __name__ == "__main__":
    test_evaluation_storage()
