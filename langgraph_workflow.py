"""
LangGraph Workflow for Energy & Property Tech Inc.
Phase 1: Foundation Setup - LangGraph Workflow Execution
"""

from langgraph.graph import StateGraph, END, START
from langgraph.types import Send
from typing import TypedDict, Annotated, List, Dict, Any
import operator
import json
from datetime import datetime
import asyncio

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
    orchestration_spec: Dict[str, Any]  # JSON orchestration specification
    agent_outputs: Annotated[Dict[str, Any], merge_agent_outputs]  # All agents write to this key
    current_agent: str  # Current executing agent
    workflow_status: str  # Workflow execution status
    final_output: str  # Final synthesized output

# Worker state for individual agents
class WorkerState(TypedDict):
    agent_id: str
    directives: List[str]
    data_sources: List[str]
    agent_outputs: Annotated[Dict[str, Any], merge_agent_outputs]

class LangGraphWorkflow:
    """LangGraph Workflow Execution Engine"""
    
    def __init__(self, fast_mcp_client):
        self.mcp_client = fast_mcp_client
        self.workflow = self._build_workflow()
    
    def _build_workflow(self):
        """Build the LangGraph workflow"""
        
        # Create the workflow builder
        workflow_builder = StateGraph(AgentState)
        
        # Add the nodes
        workflow_builder.add_node("orchestrator", self._orchestrator_node)
        workflow_builder.add_node("operations_summary_agent_worker", self._operations_summary_agent_worker)
        workflow_builder.add_node("upsell_discovery_agent_worker", self._upsell_discovery_agent_worker)
        workflow_builder.add_node("campaign_planner_agent_worker", self._campaign_planner_agent_worker)
        workflow_builder.add_node("financial_impact_agent_worker", self._financial_impact_agent_worker)
        workflow_builder.add_node("synthesizer", self._synthesizer_node)
        
        # Add edges to connect nodes
        workflow_builder.add_edge(START, "orchestrator")
        workflow_builder.add_conditional_edges(
            "orchestrator", 
            self._assign_workers, 
            [
                "operations_summary_agent_worker",
                "upsell_discovery_agent_worker", 
                "campaign_planner_agent_worker",
                "financial_impact_agent_worker"
            ]
        )
        workflow_builder.add_edge("operations_summary_agent_worker", "synthesizer")
        workflow_builder.add_edge("upsell_discovery_agent_worker", "synthesizer")
        workflow_builder.add_edge("campaign_planner_agent_worker", "synthesizer")
        workflow_builder.add_edge("financial_impact_agent_worker", "synthesizer")
        workflow_builder.add_edge("synthesizer", END)
        
        # Compile the workflow
        return workflow_builder.compile()
    
    def _orchestrator_node(self, state: AgentState) -> Dict[str, Any]:
        """Orchestrator that loads and validates the orchestration specification"""
        
        # Load orchestration spec from state
        spec = state["orchestration_spec"]
        
        # Validate and prepare for execution
        return {
            "workflow_status": "ready",
            "orchestration_spec": spec
        }
    
    def _operations_summary_agent_worker(self, state: WorkerState) -> Dict[str, Any]:
        """Operations Summary Agent worker"""
        
        # Mock agent execution for Phase 1
        result = {
            "agent_id": "operations_summary_agent",
            "timestamp": datetime.utcnow().isoformat(),
            "status": "completed",
            "output": {
                "total_installations": 18,
                "operational_status": {
                    "operational": 8,
                    "maintenance_due": 2,
                    "out_of_service": 1,
                    "obsolete": 7
                },
                "regional_breakdown": {
                    "APAC": 5,
                    "EMEA": 7,
                    "AMER": 6
                },
                "total_upsell_potential": "$5.2M",
                "critical_issues": [
                    "2 assets maintenance due",
                    "1 asset out of service"
                ]
            }
        }
        
        return {"agent_outputs": {state["agent_id"]: result}}
    
    def _upsell_discovery_agent_worker(self, state: WorkerState) -> Dict[str, Any]:
        """Upsell Discovery Agent worker"""
        
        # Mock agent execution for Phase 1
        result = {
            "agent_id": "upsell_discovery_agent",
            "timestamp": datetime.utcnow().isoformat(),
            "status": "completed",
            "output": {
                "opportunities": [
                    {
                        "customer": "Helios Energy",
                        "region": "APAC",
                        "current_products": ["PowerSecure Modular UPS"],
                        "recommended_upsell": "EnergyX Analytics Platform",
                        "potential_value": "$500K",
                        "justification": "High-value customer with UPS but no analytics",
                        "next_steps": "Schedule demo of analytics platform"
                    },
                    {
                        "customer": "United Government Complex",
                        "region": "EMEA", 
                        "current_products": ["DataShield DCIM Software"],
                        "recommended_upsell": "Service Contract",
                        "potential_value": "$34K",
                        "justification": "No service contract, high-value installation",
                        "next_steps": "Propose annual service agreement"
                    }
                ],
                "total_opportunities": 2,
                "total_potential_value": "$534K"
            }
        }
        
        return {"agent_outputs": {state["agent_id"]: result}}
    
    def _campaign_planner_agent_worker(self, state: WorkerState) -> Dict[str, Any]:
        """Campaign Planner Agent worker"""
        
        # Mock agent execution for Phase 1
        result = {
            "agent_id": "campaign_planner_agent",
            "timestamp": datetime.utcnow().isoformat(),
            "status": "completed",
            "output": {
                "campaign_name": "Q3 2025 EMEA Upsell Campaign",
                "target_customers": ["Helios Energy", "United Government Complex"],
                "total_potential_value": "$534K",
                "timeline": {
                    "week_1": "Intro emails to target customers",
                    "week_2": "Product demos and webinars",
                    "week_3": "Follow-up calls and proposals",
                    "week_4": "Closing and contract negotiations"
                },
                "channels": ["Email", "LinkedIn", "Webinar"],
                "content_assets": [
                    "EnergyX Analytics Platform demo video",
                    "Service contract benefits presentation",
                    "Customer success case studies"
                ],
                "expected_conversion_rate": "25%",
                "projected_revenue": "$133.5K"
            }
        }
        
        return {"agent_outputs": {state["agent_id"]: result}}
    
    def _financial_impact_agent_worker(self, state: WorkerState) -> Dict[str, Any]:
        """Financial Impact Agent worker"""
        
        # Mock agent execution for Phase 1
        result = {
            "agent_id": "financial_impact_agent",
            "timestamp": datetime.utcnow().isoformat(),
            "status": "completed",
            "output": {
                "current_quarter_revenue": "$116M",
                "campaign_investment": "$15K",
                "projected_upsell_revenue": "$133.5K",
                "net_impact": "$118.5K",
                "roi": "790%",
                "scenarios": {
                    "base_case": {
                        "conversion_rate": "25%",
                        "revenue_impact": "$133.5K",
                        "margin_impact": "$93.5K"
                    },
                    "optimistic": {
                        "conversion_rate": "40%",
                        "revenue_impact": "$213.6K", 
                        "margin_impact": "$149.5K"
                    },
                    "conservative": {
                        "conversion_rate": "15%",
                        "revenue_impact": "$80.1K",
                        "margin_impact": "$56.1K"
                    }
                },
                "quarterly_forecast": {
                    "Q3_2025_projected": "$116M + $133.5K = $116.13M",
                    "growth_rate": "0.11%",
                    "margin_improvement": "0.08%"
                }
            }
        }
        
        return {"agent_outputs": {state["agent_id"]: result}}
    
    def _synthesizer_node(self, state: AgentState) -> Dict[str, Any]:
        """Synthesize final output from all agent results"""
        
        # Combine all agent outputs
        agent_outputs = state["agent_outputs"]
        
        # Generate executive summary
        final_output = {
            "timestamp": datetime.utcnow().isoformat(),
            "orchestration_id": state["orchestration_spec"]["orchestration_id"],
            "user_query": state["orchestration_spec"]["user_query"],
            "executive_summary": {
                "total_upsell_potential": "$5.2M",
                "campaign_revenue_projection": "$133.5K",
                "roi": "790%",
                "recommended_actions": [
                    "Execute EMEA upsell campaign immediately",
                    "Focus on Helios Energy and United Government Complex",
                    "Allocate $15K budget for campaign execution"
                ]
            },
            "detailed_analysis": agent_outputs
        }
        
        return {"final_output": json.dumps(final_output, indent=2)}
    
    def _assign_workers(self, state: AgentState):
        """Assign workers to each agent in the orchestration spec"""
        
        spec = state["orchestration_spec"]
        agents = spec["workflow"]["agents"]
        
        # Create worker assignments for each agent
        worker_assignments = []
        for agent in agents:
            worker_assignments.append(
                Send(
                    f"{agent['agent_id']}_worker",
                    {
                        "agent_id": agent["agent_id"],
                        "directives": agent["directives"],
                        "data_sources": agent["data_sources"]
                    }
                )
            )
        
        return worker_assignments
    
    async def execute_orchestration(self, orchestration_file: str) -> str:
        """Execute orchestration workflow"""
        
        # Load orchestration spec
        with open(orchestration_file, 'r') as file:
            orchestration_spec = json.load(file)
        
        # Initialize state
        initial_state = {
            "orchestration_spec": orchestration_spec,
            "agent_outputs": {},
            "current_agent": None,
            "workflow_status": "running",
            "final_output": None
        }
        
        # Execute workflow
        result = await self.workflow.ainvoke(initial_state)
        return result["final_output"]

# Workflow Engine for integration
class WorkflowEngine:
    """Workflow Execution Engine"""
    
    def __init__(self, fast_mcp_client):
        self.mcp_client = fast_mcp_client
        self.workflow = LangGraphWorkflow(fast_mcp_client)
    
    async def execute_orchestration(self, orchestration_file: str) -> str:
        """Execute orchestration workflow"""
        return await self.workflow.execute_orchestration(orchestration_file)

# Demo function for LangGraph workflow testing
async def test_langgraph_workflow():
    """Test LangGraph workflow functionality"""
    print("🧪 Testing LangGraph Workflow")
    
    # Create a real Fast MCP client for testing
    from fast_mcp_connectors import FastMCPClient
    fast_mcp_client = FastMCPClient()
    
    workflow_engine = WorkflowEngine(fast_mcp_client)
    
    # Create a test orchestration spec
    test_orchestration = {
        "orchestration_id": "test-123",
        "timestamp": datetime.utcnow().isoformat(),
        "user_query": "Analyze Q2 2025 performance and plan Q3 2025 growth strategy",
        "workflow": {
            "agents": [
                {
                    "agent_id": "operations_summary_agent",
                    "directives": ["Generate operations summary"],
                    "data_sources": ["installed_assets"]
                },
                {
                    "agent_id": "upsell_discovery_agent",
                    "directives": ["Find upsell opportunities"],
                    "data_sources": ["installed_assets"]
                }
            ],
            "execution_order": ["operations_summary_agent", "upsell_discovery_agent"],
            "final_synthesis": {
                "agent_id": "synthesis_agent",
                "directives": ["Combine outputs"]
            }
        }
    }
    
    # Save test orchestration
    with open("test_orchestration.json", 'w') as file:
        json.dump(test_orchestration, file, indent=2)
    
    # Execute workflow
    result = await workflow_engine.execute_orchestration("test_orchestration.json")
    
    print("✅ Workflow execution completed!")
    print("📊 Final output preview:")
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Clean up test file
    import os
    if os.path.exists("test_orchestration.json"):
        os.remove("test_orchestration.json")
    
    print("✅ LangGraph Workflow testing completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_langgraph_workflow()) 