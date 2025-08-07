#!/usr/bin/env python3
"""
Test Phase 3: EMEA Opportunities and Pipeline Uplift Query
==========================================================

This script tests the complete Phase 3 system with a specific business query
about EMEA opportunities and pipeline uplift planning.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

# Import our Phase 3 components
from fast_mcp_connectors import FastMCPClient
from o3_orchestrator import O3Orchestrator
from langgraph_workflow import WorkflowEngine

async def test_emea_query():
    """Test the EMEA opportunities and pipeline uplift query"""
    
    print("🎯 Testing Phase 3: EMEA Opportunities and Pipeline Uplift")
    print("=" * 60)
    
    # Initialize components
    print("🚀 Initializing Phase 3 components...")
    
    # Initialize Fast MCP Client
    fast_mcp_client = FastMCPClient()
    await fast_mcp_client.initialize()
    print("✅ Fast MCP Client initialized")
    
    # Initialize o3 Orchestrator
    orchestrator = O3Orchestrator(fast_mcp_client)
    print("✅ o3 Orchestrator initialized")
    
    # Initialize Workflow Engine
    workflow_engine = WorkflowEngine(fast_mcp_client)
    print("✅ Workflow Engine initialized")
    
    # Define the EMEA query
    emea_query = "I need to know which opportunities I should focus on in EMEA. Which assets would be ideal to push? I need to uplift pipeline for about +25%. Can you help me make a plan for this and identify which accounts to focus on?"
    
    print(f"\n📝 Processing EMEA Query:")
    print(f"Query: {emea_query}")
    print("-" * 60)
    
    try:
        # Step 1: Generate orchestration specification
        print("🤖 Step 1: Generating AI-powered orchestration...")
        orchestration_spec = await orchestrator.generate_orchestration_spec(emea_query)
        
        if orchestration_spec:
            print(f"✅ Orchestration generated with {len(orchestration_spec.get('workflow', {}).get('agents', []))} agents")
            
            # Save orchestration for reference
            orchestration_id = orchestration_spec.get('orchestration_id', 'emea_test')
            orchestration_file = f"orchestrations/emea_orchestration_{orchestration_id}.json"
            
            # Ensure orchestrations directory exists
            Path("orchestrations").mkdir(exist_ok=True)
            
            with open(orchestration_file, 'w') as f:
                json.dump(orchestration_spec, f, indent=2)
            
            print(f"💾 Saved orchestration to: {orchestration_file}")
            
            # Step 2: Execute the workflow
            print("\n🔄 Step 2: Executing workflow with Claude agents...")
            
            # Execute workflow and get full result
            result = await workflow_engine.execute_orchestration(orchestration_file)
            
            # Also get the raw workflow result for debugging
            try:
                with open(orchestration_file, 'r') as file:
                    orchestration_spec = json.load(file)
                
                # Initialize workflow state
                from langgraph_workflow import AgentState
                initial_state = AgentState(
                    orchestration_spec=orchestration_spec,
                    agent_outputs={},
                    current_agent="",
                    workflow_status="initialized",
                    final_output=""
                )
                
                # Execute workflow directly to get full state
                workflow_result = await workflow_engine.workflow_graph.ainvoke(initial_state)
                print(f"🔍 Full workflow result keys: {list(workflow_result.keys())}")
                
            except Exception as e:
                print(f"⚠️ Could not get full workflow result: {e}")
            
            if result:
                print("✅ Workflow execution completed successfully!")
                
                # Display results
                print("\n📊 EMEA Analysis Results:")
                print("=" * 40)
                
                # Extract key information
                final_output = result.get('final_output', '')
                agent_outputs = result.get('agent_outputs', {})
                
                # Try to get agent outputs from workflow result if available
                if 'workflow_result' in locals():
                    agent_outputs = workflow_result.get('agent_outputs', agent_outputs)
                    print(f"🔍 Agent outputs from workflow: {list(agent_outputs.keys()) if agent_outputs else 'None'}")
                
                print(f"🤖 Agents executed: {len(agent_outputs)}")
                
                # Show agent outputs
                for agent_id, output in agent_outputs.items():
                    print(f"\n🔍 {agent_id}:")
                    if isinstance(output, dict):
                        analysis = output.get('analysis', {})
                        if isinstance(analysis, dict):
                            # Extract key insights
                            insights = analysis.get('key_insights', [])
                            recommendations = analysis.get('recommendations', [])
                            
                            if insights:
                                print("  📈 Key Insights:")
                                for insight in insights[:3]:  # Show top 3
                                    print(f"    • {insight}")
                            
                            if recommendations:
                                print("  🎯 Recommendations:")
                                for rec in recommendations[:3]:  # Show top 3
                                    print(f"    • {rec}")
                        else:
                            print(f"    {str(analysis)[:200]}...")
                    else:
                        print(f"    {str(output)[:200]}...")
                
                # Show final synthesis
                if final_output:
                    print(f"\n📋 Executive Summary:")
                    print(f"{final_output[:500]}...")
                
                print(f"\n💾 Full results saved to: {orchestration_file}")
                
            else:
                print("❌ Workflow execution failed")
                
        else:
            print("❌ Failed to generate orchestration")
            
    except Exception as error:
        print(f"❌ Error during EMEA query processing: {error}")
        import traceback
        traceback.print_exc()

async def main():
    """Main test function"""
    print("🧪 Phase 3 EMEA Query Test")
    print("=" * 50)
    
    await test_emea_query()
    
    print("\n✅ EMEA Query Test Completed!")

if __name__ == "__main__":
    asyncio.run(main()) 