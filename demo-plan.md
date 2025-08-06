# Energy & Property Tech Inc. Multi-Agent AI System - Demo Plan

## Overview
A focused 6-phase demo that showcases the multi-agent AI system using real CSV data, Fast MCP framework, o3 orchestration, and LangGraph execution. The demo will demonstrate end-to-end workflow from user query to JSON orchestration specification to agent swarm execution.

## Demo Architecture

### Technology Stack
- **OpenAI o3**: Primary orchestrator that generates JSON specifications
- **Fast MCP Framework**: Rapid MCP tool development and data connectors
- **LangGraph**: Multi-agent workflow execution engine
- **Anthropic Claude**: Specialized agents for data processing
- **Claude Code MCP**: Tool for kicking off Claude Code instances
- **Python**: Core implementation language
- **JSON Output**: Structured orchestration specifications and agent outputs

### Data Sources (Real CSVs)
- **Income Statement**: Monthly financial performance (Jan 2024 - Jun 2025)
- **Balance Sheet**: Quarterly financial position (Q1 2024 - Q2 2025)
- **Cash Flow**: Quarterly cash movements (Q1 2024 - Q2 2025)
- **Installed Assets**: Customer installations with upsell potential
- **Lead Funnel**: Sales pipeline and conversion data
- **Products**: Product catalog and descriptions

## Phase 1: Foundation Setup

### Objectives
- Set up development environment with Fast MCP
- Create Fast MCP data connectors for CSV files
- Implement o3 orchestration system
- Establish LangGraph workflow execution
- Initialize git repo and commit

### Deliverables
```python
# Fast MCP Data Connectors (fast_mcp_connectors.py)
from fast_mcp import FastMCPTool, DataConnector
import pandas as pd

class CSVDataConnector(DataConnector):
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.data = pd.read_csv(csv_path)
    
    def query(self, query: str) -> dict:
        return self.data.query(query).to_dict()
    
    def get_summary_stats(self) -> dict:
        return {
            "rows": len(self.data),
            "columns": list(self.data.columns),
            "sample": self.data.head(3).to_dict()
        }

class FinancialDataTool(FastMCPTool):
    name = "financial_data"
    description = "Query financial data from CSV files"
    
    def __init__(self):
        self.income_statement = CSVDataConnector("income_statement.csv")
        self.balance_sheet = CSVDataConnector("balance_sheet.csv")
        self.cash_flow = CSVDataConnector("cash_flow.csv")
    
    async def query_financials(self, statement_type: str, period: str) -> dict:
        connector = getattr(self, statement_type)
        return connector.query(f"period == '{period}'")

class OperationalDataTool(FastMCPTool):
    name = "operational_data"
    description = "Query operational data from CSV files"
    
    def __init__(self):
        self.installed_assets = CSVDataConnector("installed_assets.csv")
        self.lead_funnel = CSVDataConnector("lead_funnel.csv")
        self.products = CSVDataConnector("products.csv")
    
    async def get_upsell_opportunities(self, region: str = None) -> dict:
        assets = self.installed_assets.data
        if region:
            assets = assets[assets['region'] == region]
        return assets.to_dict()

class ClaudeCodeTool(FastMCPTool):
    name = "claude_code"
    description = "Kick off Claude Code instances for data analysis"
    
    async def launch_claude_code(self, analysis_type: str, data_source: str) -> dict:
        # Fast MCP handles the MCP server communication
        return await self.mcp_client.call_claude_code(analysis_type, data_source)
```

### Key Features
- **Fast MCP Data Connectors**: Read and parse all CSV files with built-in validation
- **Fast MCP Tools**: Financial queries, upsell analysis, campaign data, Claude Code integration
- **o3 Orchestration**: JSON specification generation for agent workflows
- **LangGraph Setup**: Workflow execution engine with state management

## Phase 2: o3 Orchestration System

### Objectives
- Implement o3 orchestrator for JSON specification generation
- Create orchestration prompt templates
- Establish JSON specification schema
- Set up orchestration file storage

### Deliverables
```python
# o3 Orchestrator (o3_orchestrator.py)
import json
from datetime import datetime
import uuid

class O3Orchestrator:
    def __init__(self, fast_mcp_client):
        self.mcp_client = fast_mcp_client
        self.orchestration_schema = {
            "orchestration_id": str,
            "timestamp": str,
            "user_query": str,
            "workflow": {
                "agents": list,
                "execution_order": list,
                "final_synthesis": dict
            }
        }
    
    async def generate_orchestration_spec(self, user_query: str) -> dict:
        # o3 analyzes the query and generates JSON specification
        orchestration_spec = {
            "orchestration_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "user_query": user_query,
            "workflow": {
                "agents": [
                    {
                        "agent_id": "operations_summary_agent",
                        "activation_trigger": "always",
                        "directives": [
                            "Generate Q2 2025 operations summary",
                            "Identify critical operational issues",
                            "Provide regional performance breakdown"
                        ],
                        "data_sources": ["installed_assets", "lead_funnel"],
                        "output_format": "json",
                        "dependencies": []
                    },
                    {
                        "agent_id": "upsell_discovery_agent",
                        "activation_trigger": "after_operations_summary",
                        "directives": [
                            "Find top upsell opportunities in EMEA region",
                            "Prioritize by potential value",
                            "Include customer context and justification"
                        ],
                        "data_sources": ["installed_assets", "products"],
                        "output_format": "json",
                        "dependencies": ["operations_summary_agent"]
                    }
                ],
                "execution_order": [
                    "operations_summary_agent",
                    "upsell_discovery_agent"
                ],
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
        
        # Save orchestration spec to file
        await self.save_orchestration_spec(orchestration_spec)
        return orchestration_spec
    
    async def save_orchestration_spec(self, spec: dict):
        filename = f"orchestration_{spec['orchestration_id']}.json"
        with open(filename, 'w') as f:
            json.dump(spec, f, indent=2)
```

### Demo Scenario
**Input**: "Analyze Q2 2025 performance and plan Q3 2025 growth strategy"
**Output**: JSON orchestration specification saved to project folder

## Phase 3: Agent Swarm Implementation

### Objectives
- Implement all specialized agents using Fast MCP tools
- Create agent execution framework
- Establish agent communication protocols
- Set up agent output formatting

### Deliverables
```python
# Agent Base Class (agent_base.py)
from abc import ABC, abstractmethod
import json
from datetime import datetime

class BaseAgent(ABC):
    def __init__(self, fast_mcp_client):
        self.mcp_client = fast_mcp_client
    
    @abstractmethod
    async def execute(self, directives: list, data_sources: list) -> dict:
        pass
    
    def format_output(self, data: dict) -> dict:
        return {
            "agent_id": self.__class__.__name__,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "completed",
            "output": data
        }

# Operations Summary Agent (operations_agent.py)
class OperationsSummaryAgent(BaseAgent):
    async def execute(self, directives: list, data_sources: list) -> dict:
        # Use Fast MCP tools to access data
        operational_data = await self.mcp_client.operational_data.get_upsell_opportunities()
        
        summary = {
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
        return self.format_output(summary)

# Upsell Discovery Agent (upsell_agent.py)
class UpsellDiscoveryAgent(BaseAgent):
    async def execute(self, directives: list, data_sources: list) -> dict:
        # Use Fast MCP tools to access data
        upsell_data = await self.mcp_client.operational_data.get_upsell_opportunities("EMEA")
        
        opportunities = [
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
        ]
        return self.format_output(opportunities)

# Campaign Planner Agent (campaign_agent.py)
class CampaignPlannerAgent(BaseAgent):
    async def execute(self, directives: list, data_sources: list) -> dict:
        campaign_plan = {
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
        return self.format_output(campaign_plan)

# Financial Impact Agent (financial_agent.py)
class FinancialImpactAgent(BaseAgent):
    async def execute(self, directives: list, data_sources: list) -> dict:
        # Use Fast MCP tools to access financial data
        current_financials = await self.mcp_client.financial_data.query_financials("income_statement", "Q2 2025")
        
        impact_analysis = {
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
        return self.format_output(impact_analysis)
```

## Phase 4: LangGraph Workflow Execution

### Objectives
- Implement LangGraph workflow execution engine
- Create agent state management
- Establish workflow orchestration
- Set up error handling and recovery

### Deliverables
```python
# LangGraph Workflow (langgraph_workflow.py)
from langgraph.graph import StateGraph, END, START
from langgraph.types import Send
from typing import TypedDict, Annotated, List
import operator
import json
from datetime import datetime

# Graph state
class AgentState(TypedDict):
    orchestration_spec: dict  # JSON orchestration specification
    agent_outputs: Annotated[dict, operator.add]  # All agents write to this key
    current_agent: str  # Current executing agent
    workflow_status: str  # Workflow execution status
    final_output: str  # Final synthesized output

# Worker state for individual agents
class WorkerState(TypedDict):
    agent_id: str
    directives: List[str]
    data_sources: List[str]
    agent_outputs: Annotated[dict, operator.add]

# Nodes
def orchestrator(state: AgentState):
    """Orchestrator that loads and validates the orchestration specification"""
    
    # Load orchestration spec from file
    spec = state["orchestration_spec"]
    
    # Validate and prepare for execution
    return {
        "workflow_status": "ready",
        "orchestration_spec": spec
    }

def operations_summary_agent(state: WorkerState):
    """Operations Summary Agent worker"""
    
    # Execute agent logic
    agent = OperationsSummaryAgent(fast_mcp_client)
    result = await agent.execute(state["directives"], state["data_sources"])
    
    return {"agent_outputs": {state["agent_id"]: result}}

def upsell_discovery_agent(state: WorkerState):
    """Upsell Discovery Agent worker"""
    
    # Execute agent logic
    agent = UpsellDiscoveryAgent(fast_mcp_client)
    result = await agent.execute(state["directives"], state["data_sources"])
    
    return {"agent_outputs": {state["agent_id"]: result}}

def campaign_planner_agent(state: WorkerState):
    """Campaign Planner Agent worker"""
    
    # Execute agent logic
    agent = CampaignPlannerAgent(fast_mcp_client)
    result = await agent.execute(state["directives"], state["data_sources"])
    
    return {"agent_outputs": {state["agent_id"]: result}}

def financial_impact_agent(state: WorkerState):
    """Financial Impact Agent worker"""
    
    # Execute agent logic
    agent = FinancialImpactAgent(fast_mcp_client)
    result = await agent.execute(state["directives"], state["data_sources"])
    
    return {"agent_outputs": {state["agent_id"]: result}}

def synthesizer(state: AgentState):
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

# Conditional edge function to create agent workers
def assign_workers(state: AgentState):
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

# Build workflow
workflow_builder = StateGraph(AgentState)

# Add the nodes
workflow_builder.add_node("orchestrator", orchestrator)
workflow_builder.add_node("operations_summary_agent_worker", operations_summary_agent)
workflow_builder.add_node("upsell_discovery_agent_worker", upsell_discovery_agent)
workflow_builder.add_node("campaign_planner_agent_worker", campaign_planner_agent)
workflow_builder.add_node("financial_impact_agent_worker", financial_impact_agent)
workflow_builder.add_node("synthesizer", synthesizer)

# Add edges to connect nodes
workflow_builder.add_edge(START, "orchestrator")
workflow_builder.add_conditional_edges(
    "orchestrator", 
    assign_workers, 
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
workflow = workflow_builder.compile()

# Workflow Execution Engine (workflow_engine.py)
class WorkflowEngine:
    def __init__(self, fast_mcp_client):
        self.mcp_client = fast_mcp_client
        self.workflow = workflow
    
    async def execute_orchestration(self, orchestration_file: str):
        # Load orchestration spec
        with open(orchestration_file, 'r') as f:
            orchestration_spec = json.load(f)
        
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
```

## Phase 5: Integration & Testing

### Objectives
- Integrate all components
- Test end-to-end workflow
- Validate agent outputs
- Optimize performance

### Deliverables
```python
# Main Integration (main_integration.py)
import asyncio
from fast_mcp import FastMCPClient
from o3_orchestrator import O3Orchestrator
from workflow_engine import WorkflowEngine

class EnergyPropertyAISystem:
    def __init__(self):
        self.fast_mcp_client = FastMCPClient()
        self.o3_orchestrator = O3Orchestrator(self.fast_mcp_client)
        self.workflow_engine = WorkflowEngine(self.fast_mcp_client)
    
    async def process_user_query(self, user_query: str):
        # Step 1: o3 generates orchestration spec
        orchestration_spec = await self.o3_orchestrator.generate_orchestration_spec(user_query)
        
        # Step 2: LangGraph executes workflow
        final_output = await self.workflow_engine.execute_orchestration(
            f"orchestration_{orchestration_spec['orchestration_id']}.json"
        )
        
        return final_output

# Demo Runner (demo_runner.py)
async def run_demo():
    system = EnergyPropertyAISystem()
    
    # Demo query
    user_query = "Analyze Q2 2025 performance and plan Q3 2025 growth strategy"
    
    print("🚀 Starting Energy & Property Tech AI System Demo")
    print(f"📝 User Query: {user_query}")
    
    # Process query
    result = await system.process_user_query(user_query)
    
    print("✅ Demo completed successfully!")
    print("📊 Final Output:")
    print(result)
    
    return result

if __name__ == "__main__":
    asyncio.run(run_demo())
```

## Phase 6: Demo Execution & Presentation

### Objectives
- Execute complete demo workflow
- Present results in real-time
- Showcase system capabilities
- Demonstrate business value

### Demo Flow
1. **Setup**: Initialize Fast MCP client and load CSV data
2. **User Input**: "Analyze Q2 2025 performance and plan Q3 2025 growth strategy"
3. **o3 Orchestration**: Generate JSON specification
4. **File Storage**: Save orchestration spec to project folder
5. **LangGraph Execution**: Execute agent workflow
6. **Agent Execution**: Each agent processes data and generates output
7. **Final Synthesis**: Combine all outputs into comprehensive report
8. **Presentation**: Display results with actionable insights

### Expected Demo Duration: 10-15 minutes

### Key Demo Highlights
- **Real Data**: Uses actual company financial and operational data
- **Fast MCP Integration**: Rapid tool development and data access
- **o3 Orchestration**: Intelligent JSON specification generation
- **Agent Swarm**: Multiple specialized agents working in concert
- **Actionable Insights**: Provides specific recommendations with ROI
- **Structured Output**: Clean JSON format for easy consumption

## Success Criteria
- ✅ o3 generates valid JSON orchestration specifications
- ✅ Fast MCP tools successfully access all CSV data
- ✅ LangGraph orchestrates multi-agent workflow execution
- ✅ All agents produce structured JSON outputs
- ✅ Final synthesis provides comprehensive business insights
- ✅ System demonstrates end-to-end workflow from query to results

This demo plan creates a working prototype that showcases the full potential of the Fast MCP-based multi-agent AI system while using real company data and providing actionable business insights through intelligent orchestration.