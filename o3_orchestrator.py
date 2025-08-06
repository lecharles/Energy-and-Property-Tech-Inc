"""
o3 Orchestrator for Energy & Property Tech Inc.
Phase 1: Foundation Setup - o3 Orchestration System
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import asyncio

class O3Orchestrator:
    """o3 Orchestrator for JSON specification generation"""
    
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
        self.orchestration_dir = Path("orchestrations")
        self.orchestration_dir.mkdir(exist_ok=True)
    
    async def generate_orchestration_spec(self, user_query: str) -> Dict[str, Any]:
        """o3 analyzes the query and generates JSON specification"""
        
        # Analyze the user query to determine required agents
        required_agents = await self._analyze_query(user_query)
        
        orchestration_spec = {
            "orchestration_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "user_query": user_query,
            "workflow": {
                "agents": required_agents,
                "execution_order": [agent["agent_id"] for agent in required_agents],
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
    
    async def _analyze_query(self, user_query: str) -> List[Dict[str, Any]]:
        """Analyze user query to determine required agents and their directives"""
        
        query_lower = user_query.lower()
        agents = []
        
        # Check for performance analysis keywords
        if any(keyword in query_lower for keyword in ["performance", "analyze", "quarter", "q2", "q3"]):
            agents.append({
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
            })
        
        # Check for growth strategy keywords
        if any(keyword in query_lower for keyword in ["growth", "strategy", "plan", "upsell", "opportunity"]):
            agents.append({
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
            })
        
        # Check for campaign planning keywords
        if any(keyword in query_lower for keyword in ["campaign", "marketing", "sales", "target"]):
            agents.append({
                "agent_id": "campaign_planner_agent",
                "activation_trigger": "after_upsell_discovery",
                "directives": [
                    "Create targeted marketing campaign",
                    "Define campaign timeline and channels",
                    "Estimate conversion rates and revenue"
                ],
                "data_sources": ["lead_funnel", "products"],
                "output_format": "json",
                "dependencies": ["upsell_discovery_agent"]
            })
        
        # Check for financial impact keywords
        if any(keyword in query_lower for keyword in ["financial", "revenue", "roi", "impact", "forecast"]):
            agents.append({
                "agent_id": "financial_impact_agent",
                "activation_trigger": "after_campaign_planning",
                "directives": [
                    "Calculate financial impact of recommendations",
                    "Provide ROI analysis",
                    "Generate quarterly forecasts"
                ],
                "data_sources": ["income_statement", "balance_sheet", "cash_flow"],
                "output_format": "json",
                "dependencies": ["campaign_planner_agent"]
            })
        
        # If no specific agents identified, add default operations summary
        if not agents:
            agents.append({
                "agent_id": "operations_summary_agent",
                "activation_trigger": "always",
                "directives": [
                    "Generate comprehensive operations summary",
                    "Identify key performance indicators",
                    "Provide actionable insights"
                ],
                "data_sources": ["installed_assets", "lead_funnel"],
                "output_format": "json",
                "dependencies": []
            })
        
        return agents
    
    async def save_orchestration_spec(self, spec: Dict[str, Any]) -> str:
        """Save orchestration specification to file"""
        filename = f"orchestration_{spec['orchestration_id']}.json"
        filepath = self.orchestration_dir / filename
        
        with open(filepath, 'w') as file:
            json.dump(spec, file, indent=2)
        
        print(f"💾 Saved orchestration spec to: {filepath}")
        return str(filepath)
    
    async def load_orchestration_spec(self, orchestration_id: str) -> Dict[str, Any]:
        """Load orchestration specification from file"""
        filename = f"orchestration_{orchestration_id}.json"
        filepath = self.orchestration_dir / filename
        
        if not filepath.exists():
            return {"error": f"Orchestration spec not found: {filename}"}
        
        with open(filepath, 'r') as file:
            return json.load(file)
    
    async def list_orchestrations(self) -> List[Dict[str, Any]]:
        """List all orchestration specifications"""
        orchestrations = []
        
        for filepath in self.orchestration_dir.glob("orchestration_*.json"):
            try:
                with open(filepath, 'r') as file:
                    spec = json.load(file)
                    orchestrations.append({
                        "orchestration_id": spec["orchestration_id"],
                        "timestamp": spec["timestamp"],
                        "user_query": spec["user_query"],
                        "agents_count": len(spec["workflow"]["agents"])
                    })
            except Exception as error:
                print(f"❌ Error reading {filepath}: {error}")
        
        return orchestrations
    
    async def validate_orchestration_spec(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Validate orchestration specification"""
        errors = []
        warnings = []
        
        # Check required fields
        required_fields = ["orchestration_id", "timestamp", "user_query", "workflow"]
        for field in required_fields:
            if field not in spec:
                errors.append(f"Missing required field: {field}")
        
        # Check workflow structure
        if "workflow" in spec:
            workflow = spec["workflow"]
            if "agents" not in workflow:
                errors.append("Missing agents in workflow")
            elif not workflow["agents"]:
                warnings.append("No agents defined in workflow")
            
            if "execution_order" not in workflow:
                errors.append("Missing execution_order in workflow")
            
            if "final_synthesis" not in workflow:
                warnings.append("Missing final_synthesis in workflow")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }

# Demo function for o3 orchestrator testing
async def test_o3_orchestrator():
    """Test o3 orchestrator functionality"""
    print("🧪 Testing o3 Orchestrator")
    
    # Create a real Fast MCP client for testing
    from fast_mcp_connectors import FastMCPClient
    fast_mcp_client = FastMCPClient()
    
    orchestrator = O3Orchestrator(fast_mcp_client)
    
    # Test query analysis
    test_queries = [
        "Analyze Q2 2025 performance and plan Q3 2025 growth strategy",
        "Find upsell opportunities in EMEA region",
        "Create marketing campaign for new products",
        "Calculate financial impact of expansion plans"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Testing query {i}: {query}")
        spec = await orchestrator.generate_orchestration_spec(query)
        
        # Validate the spec
        validation = await orchestrator.validate_orchestration_spec(spec)
        print(f"✅ Valid: {validation['valid']}")
        if validation['errors']:
            print(f"❌ Errors: {validation['errors']}")
        if validation['warnings']:
            print(f"⚠️ Warnings: {validation['warnings']}")
        
        print(f"🤖 Agents: {len(spec['workflow']['agents'])}")
        for agent in spec['workflow']['agents']:
            print(f"  - {agent['agent_id']}")
    
    # List orchestrations
    orchestrations = await orchestrator.list_orchestrations()
    print(f"\n📋 Total orchestrations: {len(orchestrations)}")
    
    print("✅ o3 Orchestrator testing completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_o3_orchestrator()) 