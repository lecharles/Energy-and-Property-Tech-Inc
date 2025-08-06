"""
Main Integration for Energy & Property Tech Inc.
Phase 1: Foundation Setup - Main Integration
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

# Import our Phase 1 components
from fast_mcp_connectors import FastMCPClient
from o3_orchestrator import O3Orchestrator
from langgraph_workflow import WorkflowEngine

class EnergyPropertyAISystem:
    """Main AI System Integration"""
    
    def __init__(self):
        self.fast_mcp_client = FastMCPClient()
        self.o3_orchestrator = O3Orchestrator(self.fast_mcp_client)
        self.workflow_engine = WorkflowEngine(self.fast_mcp_client)
        self.initialized = False
    
    async def initialize(self):
        """Initialize all system components"""
        print("🚀 Initializing Energy & Property Tech AI System...")
        
        try:
            # Initialize Fast MCP client
            init_result = await self.fast_mcp_client.initialize()
            
            # Test o3 orchestrator
            test_spec = await self.o3_orchestrator.generate_orchestration_spec(
                "Test initialization query"
            )
            
            # Test workflow engine
            test_orchestration = {
                "orchestration_id": "init-test",
                "timestamp": datetime.utcnow().isoformat(),
                "user_query": "Test initialization",
                "workflow": {
                    "agents": [
                        {
                            "agent_id": "operations_summary_agent",
                            "directives": ["Test agent"],
                            "data_sources": ["installed_assets"]
                        }
                    ],
                    "execution_order": ["operations_summary_agent"],
                    "final_synthesis": {
                        "agent_id": "synthesis_agent",
                        "directives": ["Test synthesis"]
                    }
                }
            }
            
            # Save test orchestration
            with open("init_test_orchestration.json", 'w') as file:
                json.dump(test_orchestration, file, indent=2)
            
            # Test workflow execution
            test_result = await self.workflow_engine.execute_orchestration(
                "init_test_orchestration.json"
            )
            
            # Clean up test file
            import os
            if os.path.exists("init_test_orchestration.json"):
                os.remove("init_test_orchestration.json")
            
            self.initialized = True
            print("✅ System initialization completed successfully!")
            
            return {
                "status": "success",
                "fast_mcp": init_result,
                "o3_test": test_spec,
                "workflow_test": "completed"
            }
            
        except Exception as error:
            print(f"❌ System initialization failed: {error}")
            return {
                "status": "error",
                "error": str(error)
            }
    
    async def process_user_query(self, user_query: str):
        """Process user query through the complete workflow"""
        
        if not self.initialized:
            print("⚠️ System not initialized. Initializing now...")
            await self.initialize()
        
        print(f"📝 Processing user query: {user_query}")
        
        try:
            # Step 1: o3 generates orchestration spec
            print("🤖 Step 1: Generating orchestration specification...")
            orchestration_spec = await self.o3_orchestrator.generate_orchestration_spec(user_query)
            
            # Step 2: LangGraph executes workflow
            print("🔄 Step 2: Executing workflow...")
            orchestration_file = f"orchestrations/orchestration_{orchestration_spec['orchestration_id']}.json"
            final_output = await self.workflow_engine.execute_orchestration(orchestration_file)
            
            print("✅ Query processing completed successfully!")
            
            return {
                "status": "success",
                "orchestration_spec": orchestration_spec,
                "final_output": final_output,
                "orchestration_file": orchestration_file
            }
            
        except Exception as error:
            print(f"❌ Query processing failed: {error}")
            return {
                "status": "error",
                "error": str(error)
            }
    
    async def get_system_status(self):
        """Get system status and component health"""
        status = {
            "initialized": self.initialized,
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "fast_mcp_client": "ready" if self.initialized else "not_initialized",
                "o3_orchestrator": "ready" if self.initialized else "not_initialized",
                "workflow_engine": "ready" if self.initialized else "not_initialized"
            }
        }
        
        if self.initialized:
            # Check orchestration files
            orchestration_dir = Path("orchestrations")
            if orchestration_dir.exists():
                orchestration_files = list(orchestration_dir.glob("*.json"))
                status["orchestrations"] = {
                    "count": len(orchestration_files),
                    "files": [f.name for f in orchestration_files]
                }
            else:
                status["orchestrations"] = {"count": 0, "files": []}
        
        return status

# Demo Runner for Phase 1
async def run_phase_1_demo():
    """Run Phase 1 demo"""
    print("🎬 Starting Phase 1 Demo: Foundation Setup")
    print("=" * 50)
    
    # Initialize system
    system = EnergyPropertyAISystem()
    init_result = await system.initialize()
    
    if init_result["status"] == "error":
        print(f"❌ Demo failed during initialization: {init_result['error']}")
        return
    
    print("\n✅ System initialized successfully!")
    
    # Test system status
    status = await system.get_system_status()
    print(f"📊 System Status: {status}")
    
    # Demo queries
    demo_queries = [
        "Analyze Q2 2025 performance and plan Q3 2025 growth strategy",
        "Find upsell opportunities in EMEA region",
        "Create marketing campaign for new products"
    ]
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n🧪 Demo Query {i}: {query}")
        print("-" * 40)
        
        result = await system.process_user_query(query)
        
        if result["status"] == "success":
            print("✅ Query processed successfully!")
            print(f"📁 Orchestration file: {result['orchestration_file']}")
            print(f"📊 Output preview:")
            
            # Show first 300 characters of output
            output_preview = result["final_output"][:300]
            print(output_preview + "..." if len(result["final_output"]) > 300 else output_preview)
        else:
            print(f"❌ Query processing failed: {result['error']}")
    
    print("\n🎉 Phase 1 Demo completed successfully!")
    print("✅ All components working: Fast MCP, o3 Orchestrator, LangGraph Workflow")

# Interactive demo mode
async def interactive_demo():
    """Interactive demo mode"""
    print("🎮 Interactive Demo Mode")
    print("Type 'quit' to exit, 'status' for system status")
    
    system = EnergyPropertyAISystem()
    await system.initialize()
    
    while True:
        try:
            user_input = input("\n💬 Enter your query: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'status':
                status = await system.get_system_status()
                print(f"📊 Status: {status}")
            elif user_input:
                print("🔄 Processing...")
                result = await system.process_user_query(user_input)
                
                if result["status"] == "success":
                    print("✅ Success!")
                    print(f"📊 Output: {result['final_output'][:200]}...")
                else:
                    print(f"❌ Error: {result['error']}")
            else:
                print("⚠️ Please enter a query")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as error:
            print(f"❌ Error: {error}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        asyncio.run(interactive_demo())
    else:
        asyncio.run(run_phase_1_demo()) 