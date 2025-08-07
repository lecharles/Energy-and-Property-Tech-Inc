#!/usr/bin/env python3
"""
Test Comprehensive Business Query - Phase 4
==========================================

Test the Phase 4 system with a complex business query that requires:
- Financial analysis (gross margin by region)
- Operational analysis (top selling assets)
- Strategic planning (upsell opportunities)
- Marketing strategy (communication channels)
- Multi-agent coordination and synthesis
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path

# Import our Phase 4 system
from main_integration_v2 import EnergyPropertyAISystemV2

async def test_comprehensive_query():
    """Test the comprehensive business query with Phase 4 system"""
    
    print("🎯 Testing Phase 4 System with Comprehensive Business Query")
    print("=" * 80)
    
    # Initialize Phase 4 system
    print("🚀 Initializing Phase 4 system...")
    system = EnergyPropertyAISystemV2()
    
    if not await system.initialize_system():
        print("❌ System initialization failed!")
        return
    
    print("✅ Phase 4 system initialized successfully!")
    
    # Define the comprehensive business query
    comprehensive_query = """I need to know which region is the most interesting one to focus on with regards to gross margin. Can you look at where to focus on and which are the top three selling assets that I should focus on? Make sure that in that region and for those potential accounts, those assets are not yet sold, so there's truly an upsell opportunity. After you've done that, can you come up with an explanation as to why we should focus on that region, those products, those assets, and those accounts? From there, I'm going to have to come up with a communication strategy - which marketing campaign can we aspire for and what is the best channel of communication. And why?"""
    
    print(f"\n📝 Comprehensive Business Query:")
    print(f"Query: {comprehensive_query}")
    print("-" * 80)
    
    # Process the query
    print("\n🔄 Processing comprehensive business query...")
    start_time = time.time()
    
    try:
        result = await system.process_user_query(comprehensive_query)
        
        execution_time = time.time() - start_time
        
        print(f"\n✅ Query processing completed in {execution_time:.2f}s")
        
        # Display results
        if "error" not in result:
            print("\n📊 Results Analysis:")
            print("=" * 50)
            
            # Show orchestration details
            if "orchestration_id" in result:
                print(f"🤖 Orchestration ID: {result['orchestration_id']}")
            
            # Show system version
            if "system_version" in result:
                print(f"🔧 System Version: {result['system_version']}")
            
            # Show workflow result
            if "workflow_result" in result:
                workflow_result = result["workflow_result"]
                print(f"\n🔄 Workflow Status: {workflow_result.get('workflow_status', 'unknown')}")
                
                # Show agent outputs if available
                if "agent_outputs" in workflow_result:
                    agent_outputs = workflow_result["agent_outputs"]
                    print(f"🤖 Agents Executed: {len(agent_outputs)}")
                    
                    for agent_id, output in agent_outputs.items():
                        print(f"  • {agent_id}: {output.get('status', 'unknown')}")
            
            # Show performance metrics
            if "performance_metrics" in result:
                metrics = result["performance_metrics"]
                if "overall_metrics" in metrics:
                    overall = metrics["overall_metrics"]
                    print(f"\n📈 Performance Metrics:")
                    print(f"  • Success Rate: {overall.get('success_rate', 0):.1f}%")
                    print(f"  • Average Execution Time: {overall.get('average_execution_time', 0):.2f}s")
                    print(f"  • Total Executions: {overall.get('total_executions', 0)}")
            
            # Show optimization metrics
            if "optimization_metrics" in result:
                opt_metrics = result["optimization_metrics"]
                print(f"\n⚡ Optimization Metrics:")
                if "cache_metrics" in opt_metrics:
                    cache = opt_metrics["cache_metrics"]
                    print(f"  • Cache Hit Rate: {cache.get('hit_rate', 0):.1f}%")
                    print(f"  • Cache Size: {cache.get('size', 0)}/{cache.get('max_size', 0)}")
                
                if "execution_metrics" in opt_metrics:
                    exec_metrics = opt_metrics["execution_metrics"]
                    print(f"  • Parallel Efficiency: {exec_metrics.get('parallel_efficiency', 0):.1f}%")
                    print(f"  • Total Executions: {exec_metrics.get('total_executions', 0)}")
            
            # Show final output if available
            if "workflow_result" in result and "final_output" in result["workflow_result"]:
                final_output = result["workflow_result"]["final_output"]
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
            results_file = f"test_results/comprehensive_query_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            Path("test_results").mkdir(exist_ok=True)
            
            with open(results_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"\n💾 Detailed results saved to: {results_file}")
            
        else:
            print(f"❌ Query processing failed: {result['error']}")
    
    except Exception as e:
        execution_time = time.time() - start_time
        print(f"❌ Error during query processing: {e}")
        print(f"⏱️ Execution time: {execution_time:.2f}s")
    
    # Get system status
    print(f"\n📊 System Status:")
    status = system.get_system_status()
    print(f"  • Status: {status['status']}")
    print(f"  • System Health: {status['system_health']}")
    
    print(f"\n🎉 Comprehensive Query Test Completed!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_comprehensive_query()) 