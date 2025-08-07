"""
LangGraph Workflow for Energy & Property Tech Inc.
Phase 3: Enhanced with Real Claude-Powered Agents
"""

import asyncio
import json
from datetime import datetime
from typing import TypedDict, Annotated, List, Dict, Any
import operator
from pathlib import Path

# Import our real Claude agents
from claude_agents import ClaudeAgentFactory

# Custom merge function for agent outputs
def merge_agent_outputs(existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    """Merge agent outputs by combining dictionaries"""
    if existing is None:
        existing = {}
    if new is None:
        new = {}
    return {**existing, **new}

# Graph state
class AgentState(TypedDict):
    orchestration_spec: Dict[str, Any]
    agent_outputs: Annotated[Dict[str, Any], merge_agent_outputs]
    current_agent: str
    workflow_status: str
    final_output: str

# Worker state for individual agents
class WorkerState(TypedDict):
    agent_id: str
    directives: List[str]
    data_sources: List[str]
    agent_outputs: Annotated[Dict[str, Any], merge_agent_outputs]

class LangGraphWorkflow:
    """Enhanced LangGraph workflow with real Claude agents"""
    
    def __init__(self, fast_mcp_client):
        """Initialize the workflow with Fast MCP client"""
        self.fast_mcp_client = fast_mcp_client
        self.agent_factory = ClaudeAgentFactory()
        self.workflow = None
        
        print("🔄 LangGraph Workflow initialized with Claude agents")
    
    def _build_workflow(self):
        """Build the LangGraph workflow with real agent nodes"""
        from langgraph.graph import StateGraph, END
        
        # Create the workflow graph
        workflow = StateGraph(AgentState)
        
        # Add nodes for each agent type
        workflow.add_node("orchestrator_node", self._orchestrator_node)
        workflow.add_node("operations_summary_agent_worker", self._operations_summary_agent_worker)
        workflow.add_node("upsell_discovery_agent_worker", self._upsell_discovery_agent_worker)
        workflow.add_node("campaign_planner_agent_worker", self._campaign_planner_agent_worker)
        workflow.add_node("financial_impact_agent_worker", self._financial_impact_agent_worker)
        workflow.add_node("synthesis_agent_worker", self._synthesis_agent_worker)
        
        # Define the workflow edges
        workflow.set_entry_point("orchestrator_node")
        
        # Add conditional edges based on orchestration spec
        workflow.add_conditional_edges(
            "orchestrator_node",
            self._route_to_agents,
            {
                "operations_summary_agent_worker": "operations_summary_agent_worker",
                "upsell_discovery_agent_worker": "upsell_discovery_agent_worker",
                "campaign_planner_agent_worker": "campaign_planner_agent_worker",
                "financial_impact_agent_worker": "financial_impact_agent_worker",
                "synthesis_agent_worker": "synthesis_agent_worker",
                END: END
            }
        )
        
        # Add edges from agent workers to synthesis
        workflow.add_edge("operations_summary_agent_worker", "synthesis_agent_worker")
        workflow.add_edge("upsell_discovery_agent_worker", "synthesis_agent_worker")
        workflow.add_edge("campaign_planner_agent_worker", "synthesis_agent_worker")
        workflow.add_edge("financial_impact_agent_worker", "synthesis_agent_worker")
        
        # Add edge from synthesis to end
        workflow.add_edge("synthesis_agent_worker", END)
        
        self.workflow = workflow.compile()
        return self.workflow
    
    async def _orchestrator_node(self, state: AgentState) -> AgentState:
        """Orchestrator node that prepares the workflow"""
        print("🎯 Orchestrator node: Preparing workflow execution...")
        
        orchestration_spec = state["orchestration_spec"]
        workflow_status = "initialized"
        
        # Update state with workflow information
        state["workflow_status"] = workflow_status
        state["agent_outputs"] = {}
        
        print(f"✅ Orchestrator prepared workflow with {len(orchestration_spec.get('workflow', {}).get('agents', []))} agents")
        return state
    
    def _route_to_agents(self, state: AgentState) -> str:
        """Route to the appropriate agent based on orchestration spec"""
        orchestration_spec = state["orchestration_spec"]
        agents = orchestration_spec.get("workflow", {}).get("agents", [])
        
        # Check which agents need to be executed
        for agent in agents:
            agent_id = agent["agent_id"]
            if agent_id not in state.get("agent_outputs", {}):
                return f"{agent_id}_worker"
        
        # If all agents are done, go to synthesis
        return "synthesis_agent_worker"
    
    async def _operations_summary_agent_worker(self, state: AgentState) -> AgentState:
        """Real Claude-powered operations summary agent worker"""
        print("🏭 Operations Summary Agent Worker: Executing with Claude...")
        
        try:
            # Get agent configuration from orchestration spec
            orchestration_spec = state["orchestration_spec"]
            agent_config = self._get_agent_config(orchestration_spec, "operations_summary_agent")
            
            if not agent_config:
                print("⚠️ No operations summary agent configuration found")
                return state
            
            # Create and execute the real Claude agent
            agent = self.agent_factory.create_agent("operations_summary_agent", self.fast_mcp_client)
            result = await agent.execute(
                directives=agent_config["directives"],
                data_sources=agent_config["data_sources"]
            )
            
            # Update state with agent output
            agent_outputs = state.get("agent_outputs", {})
            agent_outputs["operations_summary_agent"] = result
            state["agent_outputs"] = agent_outputs
            
            print(f"✅ Operations Summary Agent completed: {result.get('status', 'unknown')}")
            return state
            
        except Exception as error:
            print(f"❌ Operations Summary Agent failed: {error}")
            # Add error to state
            agent_outputs = state.get("agent_outputs", {})
            agent_outputs["operations_summary_agent"] = {
                "error": str(error),
                "status": "failed"
            }
            state["agent_outputs"] = agent_outputs
            return state
    
    async def _upsell_discovery_agent_worker(self, state: AgentState) -> AgentState:
        """Real Claude-powered upsell discovery agent worker"""
        print("💰 Upsell Discovery Agent Worker: Executing with Claude...")
        
        try:
            # Get agent configuration from orchestration spec
            orchestration_spec = state["orchestration_spec"]
            agent_config = self._get_agent_config(orchestration_spec, "upsell_discovery_agent")
            
            if not agent_config:
                print("⚠️ No upsell discovery agent configuration found")
                return state
            
            # Create and execute the real Claude agent
            agent = self.agent_factory.create_agent("upsell_discovery_agent", self.fast_mcp_client)
            result = await agent.execute(
                directives=agent_config["directives"],
                data_sources=agent_config["data_sources"]
            )
            
            # Update state with agent output
            agent_outputs = state.get("agent_outputs", {})
            agent_outputs["upsell_discovery_agent"] = result
            state["agent_outputs"] = agent_outputs
            
            print(f"✅ Upsell Discovery Agent completed: {result.get('status', 'unknown')}")
            return state
            
        except Exception as error:
            print(f"❌ Upsell Discovery Agent failed: {error}")
            # Add error to state
            agent_outputs = state.get("agent_outputs", {})
            agent_outputs["upsell_discovery_agent"] = {
                "error": str(error),
                "status": "failed"
            }
            state["agent_outputs"] = agent_outputs
            return state
    
    async def _campaign_planner_agent_worker(self, state: AgentState) -> AgentState:
        """Real Claude-powered campaign planner agent worker"""
        print("📢 Campaign Planner Agent Worker: Executing with Claude...")
        
        try:
            # Get agent configuration from orchestration spec
            orchestration_spec = state["orchestration_spec"]
            agent_config = self._get_agent_config(orchestration_spec, "campaign_planner_agent")
            
            if not agent_config:
                print("⚠️ No campaign planner agent configuration found")
                return state
            
            # Create and execute the real Claude agent
            agent = self.agent_factory.create_agent("campaign_planner_agent", self.fast_mcp_client)
            result = await agent.execute(
                directives=agent_config["directives"],
                data_sources=agent_config["data_sources"]
            )
            
            # Update state with agent output
            agent_outputs = state.get("agent_outputs", {})
            agent_outputs["campaign_planner_agent"] = result
            state["agent_outputs"] = agent_outputs
            
            print(f"✅ Campaign Planner Agent completed: {result.get('status', 'unknown')}")
            return state
            
        except Exception as error:
            print(f"❌ Campaign Planner Agent failed: {error}")
            # Add error to state
            agent_outputs = state.get("agent_outputs", {})
            agent_outputs["campaign_planner_agent"] = {
                "error": str(error),
                "status": "failed"
            }
            state["agent_outputs"] = agent_outputs
            return state
    
    async def _financial_impact_agent_worker(self, state: AgentState) -> AgentState:
        """Real Claude-powered financial impact agent worker"""
        print("💰 Financial Impact Agent Worker: Executing with Claude...")
        
        try:
            # Get agent configuration from orchestration spec
            orchestration_spec = state["orchestration_spec"]
            agent_config = self._get_agent_config(orchestration_spec, "financial_impact_agent")
            
            if not agent_config:
                print("⚠️ No financial impact agent configuration found")
                return state
            
            # Create and execute the real Claude agent
            agent = self.agent_factory.create_agent("financial_impact_agent", self.fast_mcp_client)
            result = await agent.execute(
                directives=agent_config["directives"],
                data_sources=agent_config["data_sources"]
            )
            
            # Update state with agent output
            agent_outputs = state.get("agent_outputs", {})
            agent_outputs["financial_impact_agent"] = result
            state["agent_outputs"] = agent_outputs
            
            print(f"✅ Financial Impact Agent completed: {result.get('status', 'unknown')}")
            return state
            
        except Exception as error:
            print(f"❌ Financial Impact Agent failed: {error}")
            # Add error to state
            agent_outputs = state.get("agent_outputs", {})
            agent_outputs["financial_impact_agent"] = {
                "error": str(error),
                "status": "failed"
            }
            state["agent_outputs"] = agent_outputs
            return state
    
    async def _synthesis_agent_worker(self, state: AgentState) -> AgentState:
        """Real Claude-powered synthesis agent worker"""
        print("🎯 Synthesis Agent Worker: Combining all agent outputs with Claude...")
        
        try:
            # Get all agent outputs
            agent_outputs = state.get("agent_outputs", {})
            user_query = state["orchestration_spec"].get("user_query", "")
            
            # Create and execute the real Claude synthesis agent
            agent = self.agent_factory.create_agent("synthesis_agent", self.fast_mcp_client)
            result = await agent.execute(
                agent_results=agent_outputs,
                user_query=user_query
            )
            
            # Update state with final output
            state["final_output"] = result
            state["workflow_status"] = "completed"
            
            print(f"✅ Synthesis Agent completed: {result.get('status', 'unknown')}")
            return state
            
        except Exception as error:
            print(f"❌ Synthesis Agent failed: {error}")
            # Add error to state
            state["final_output"] = {
                "error": str(error),
                "status": "failed"
            }
            state["workflow_status"] = "failed"
            return state
    
    def _get_agent_config(self, orchestration_spec: Dict[str, Any], agent_id: str) -> Dict[str, Any]:
        """Get agent configuration from orchestration spec"""
        agents = orchestration_spec.get("workflow", {}).get("agents", [])
        for agent in agents:
            if agent["agent_id"] == agent_id:
                return agent
        return None

class WorkflowEngine:
    """Enhanced workflow engine with real Claude agents"""
    
    def __init__(self, fast_mcp_client):
        """Initialize the workflow engine"""
        self.fast_mcp_client = fast_mcp_client
        self.workflow = LangGraphWorkflow(fast_mcp_client)
        self.workflow_graph = self.workflow._build_workflow()
        
        print("🚀 Workflow Engine initialized with Claude agents")
    
    async def execute_orchestration(self, orchestration_file: str) -> Dict[str, Any]:
        """
        Execute orchestration using real Claude agents
        
        Args:
            orchestration_file: Path to orchestration specification file
            
        Returns:
            Final output from the workflow execution
        """
        print(f"🔄 Executing orchestration: {orchestration_file}")
        
        try:
            # Load orchestration specification
            with open(orchestration_file, 'r') as file:
                orchestration_spec = json.load(file)
            
            # Initialize workflow state
            initial_state = AgentState(
                orchestration_spec=orchestration_spec,
                agent_outputs={},
                current_agent="",
                workflow_status="initialized",
                final_output=""
            )
            
            # Execute the workflow
            print("🚀 Starting workflow execution with Claude agents...")
            result = await self.workflow_graph.ainvoke(initial_state)
            
            # Extract final output
            final_output = result.get("final_output", {})
            
            print(f"✅ Workflow execution completed: {final_output.get('status', 'unknown')}")
            return final_output
            
        except Exception as error:
            print(f"❌ Workflow execution failed: {error}")
            return {
                "error": str(error),
                "status": "failed",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get workflow engine status"""
        return {
            "service": "langgraph_workflow",
            "status": "ready",
            "claude_agents_available": True,
            "timestamp": datetime.utcnow().isoformat()
        }

# Test function for Phase 3
async def test_claude_workflow():
    """Test the enhanced workflow with real Claude agents"""
    print("🧪 Testing Enhanced LangGraph Workflow (Phase 3)")
    
    from fast_mcp_connectors import FastMCPClient
    
    # Initialize components
    fast_mcp_client = FastMCPClient()
    workflow_engine = WorkflowEngine(fast_mcp_client)
    
    # Test with a sample orchestration
    test_orchestration = {
        "orchestration_id": "test-claude-workflow",
        "timestamp": datetime.utcnow().isoformat(),
        "user_query": "Analyze Q2 2025 performance and plan Q3 2025 growth strategy",
        "workflow": {
            "agents": [
                {
                    "agent_id": "operations_summary_agent",
                    "activation_trigger": "always",
                    "directives": [
                        "Analyze operational performance for Q2 2025",
                        "Identify key performance indicators",
                        "Highlight critical operational issues"
                    ],
                    "data_sources": ["installed_assets", "lead_funnel"],
                    "output_format": "json",
                    "dependencies": []
                }
            ],
            "execution_order": ["operations_summary_agent"],
            "final_synthesis": {
                "agent_id": "synthesis_agent",
                "directives": [
                    "Combine all agent outputs into executive summary",
                    "Provide actionable recommendations",
                    "Format for presentation"
                ]
            }
        }
    }
    
    # Save test orchestration
    test_file = "test_claude_orchestration.json"
    with open(test_file, 'w') as file:
        json.dump(test_orchestration, file, indent=2)
    
    try:
        # Execute workflow
        result = await workflow_engine.execute_orchestration(test_file)
        
        print(f"✅ Test completed successfully!")
        print(f"📊 Result status: {result.get('status', 'unknown')}")
        print(f"🤖 Agent outputs: {len(result.get('analysis', {}))} analysis components")
        
    except Exception as error:
        print(f"❌ Test failed: {error}")
    
    finally:
        # Clean up test file
        import os
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    asyncio.run(test_claude_workflow()) 