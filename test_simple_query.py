#!/usr/bin/env python3
"""
Test Simple Query - Phase 4 Core Functionality
=============================================

Test the core Phase 4 functionality using the original workflow
to bypass the LangGraph state management issue.
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path

# Import the original working components
from fast_mcp_connectors import FastMCPClient
from o3_orchestrator import O3Orchestrator
from langgraph_workflow import WorkflowEngine

async def test_simple_query():
    """Test with the original working workflow"""
    
    print("🎯 Testing Phase 4 Core Functionality")
    print("=" * 60)
    
    # Initialize components
    print("🚀 Initializing components...")
    
    # Initialize Fast MCP Client
    fast_mcp_client = FastMCPClient()
    await fast_mcp_client.initialize()
    print("✅ Fast MCP Client initialized")
    
    # Initialize o3 Orchestrator
    orchestrator = O3Orchestrator(fast_mcp_client)
    print("✅ o3 Orchestrator initialized")
    
    # Initialize Workflow Engine (original)
    workflow_engine = WorkflowEngine(fast_mcp_client)
    print("✅ Workflow Engine initialized")
    
    # Define the comprehensive business query
    comprehensive_query = """I need to know which region is the most interesting one to focus on with regards to gross margin. Can you look at where to focus on and which are the top three selling assets that I should focus on? Make sure that in that region and for those potential accounts, those assets are not yet sold, so there's truly an upsell opportunity. After you've done that, can you come up with an explanation as to why we should focus on that region, those products, those assets, and those accounts? From there, I'm going to have to come up with a communication strategy - which marketing campaign can we aspire for and what is the best channel of communication. And why?"""
    
    print(f"\n📝 Comprehensive Business Query:")
    print(f"Query: {comprehensive_query}")
    print("-" * 60)
    
    # Process the query
    print("\n🔄 Processing comprehensive business query...")
    start_time = time.time()
    
    try:
        # Step 1: Generate orchestration specification
        print("🤖 Step 1: Generating AI-powered orchestration...")
        orchestration_spec = await orchestrator.generate_orchestration_spec(comprehensive_query)
        
        if orchestration_spec:
            print(f"✅ Orchestration generated with {len(orchestration_spec.get('workflow', {}).get('agents', []))} agents")
            
            # Save orchestration for reference
            orchestration_id = orchestration_spec.get('orchestration_id', 'comprehensive_test')
            orchestration_file = f"orchestrations/comprehensive_orchestration_{orchestration_id}.json"
            
            # Ensure orchestrations directory exists
            Path("orchestrations").mkdir(exist_ok=True)
            
            with open(orchestration_file, 'w') as f:
                json.dump(orchestration_spec, f, indent=2)
            
            print(f"💾 Saved orchestration to: {orchestration_file}")
            
            # Step 2: Execute the workflow
            print("\n🔄 Step 2: Executing workflow...")
            
            # Execute workflow and get full result
            result = await workflow_engine.execute_orchestration(orchestration_file)
            
            execution_time = time.time() - start_time
            
            print(f"\n✅ Query processing completed in {execution_time:.2f}s")
            
            # Display results
            if result:
                print("\n📊 Results Analysis:")
                print("=" * 50)
                
                # Show orchestration details
                print(f"🤖 Orchestration ID: {orchestration_id}")
                print(f"⏱️ Execution Time: {execution_time:.2f}s")
                
                # Show agent outputs
                if isinstance(result, dict) and "agent_outputs" in result:
                    agent_outputs = result["agent_outputs"]
                    print(f"\n🤖 Agents Executed: {len(agent_outputs)}")
                    
                    for agent_id, output in agent_outputs.items():
                        print(f"  • {agent_id}: {output.get('status', 'unknown')}")
                        
                        # Show key insights if available
                        if "output" in output:
                            agent_output = output["output"]
                            if isinstance(agent_output, dict):
                                if "insights" in agent_output:
                                    print(f"    - Insights: {agent_output['insights']}")
                                if "recommendations" in agent_output:
                                    print(f"    - Recommendations: {agent_output['recommendations']}")
                
                # Show final output
                if isinstance(result, dict) and "final_output" in result:
                    final_output = result["final_output"]
                    print(f"\n📋 Final Output:")
                    print("-" * 30)
                    
                    try:
                        # Try to parse and display JSON output
                        if isinstance(final_output, str):
                            output_data = json.loads(final_output)
                        else:
                            output_data = final_output
                        
                        # Display key sections
                        if "execution_summary" in output_data:
                            summary = output_data["execution_summary"]
                            print(f"📊 Execution Summary:")
                            print(f"  • Total Agents: {summary.get('total_agents', 0)}")
                            print(f"  • Successful Agents: {summary.get('successful_agents', 0)}")
                            print(f"  • Success Rate: {summary.get('success_rate', 0):.1f}%")
                            print(f"  • Execution Time: {summary.get('execution_time', 0):.2f}s")
                        
                        if "recommendations" in output_data:
                            recommendations = output_data["recommendations"]
                            print(f"\n💡 Recommendations:")
                            if isinstance(recommendations, list):
                                for i, rec in enumerate(recommendations[:5], 1):
                                    print(f"  {i}. {rec}")
                            else:
                                print(f"  • {recommendations}")
                        
                        if "agent_outputs" in output_data:
                            print(f"\n🤖 Agent Outputs:")
                            for agent_id, agent_output in output_data["agent_outputs"].items():
                                print(f"  • {agent_id}: {agent_output.get('status', 'unknown')}")
                                if "output" in agent_output:
                                    output_content = agent_output["output"]
                                    if isinstance(output_content, dict):
                                        # Show key insights from agent output
                                        if "insights" in output_content:
                                            print(f"    - Insights: {output_content['insights']}")
                                        if "recommendations" in output_content:
                                            print(f"    - Recommendations: {output_content['recommendations']}")
                    
                    except Exception as e:
                        print(f"  • Raw output: {final_output[:200]}...")
                
                # Save detailed results
                results_file = f"test_results/simple_query_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                Path("test_results").mkdir(exist_ok=True)
                
                with open(results_file, 'w') as f:
                    json.dump({
                        "query": comprehensive_query,
                        "orchestration_id": orchestration_id,
                        "execution_time": execution_time,
                        "result": result,
                        "timestamp": datetime.now().isoformat()
                    }, f, indent=2)
                
                print(f"\n💾 Detailed results saved to: {results_file}")
                
            else:
                print("❌ No result generated from workflow")
                
        else:
            print("❌ Failed to generate orchestration specification")
    
    except Exception as e:
        execution_time = time.time() - start_time
        print(f"❌ Error during query processing: {e}")
        print(f"⏱️ Execution time: {execution_time:.2f}s")
    
    print(f"\n🎉 Simple Query Test Completed!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_simple_query()) 