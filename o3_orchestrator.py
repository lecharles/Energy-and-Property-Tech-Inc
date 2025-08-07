"""
o3 Orchestrator for Energy & Property Tech Inc.
Phase 2: Enhanced with AI-powered orchestration generation
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# Import our AI service for intelligent orchestration
from ai_service import AIService

class O3Orchestrator:
    """Enhanced o3 Orchestrator with AI-powered orchestration generation"""
    
    def __init__(self, fast_mcp_client):
        """Initialize the o3 orchestrator with AI service"""
        self.fast_mcp_client = fast_mcp_client
        self.ai_service = AIService()
        
        # Create orchestrations directory if it doesn't exist
        self.orchestrations_dir = Path("orchestrations")
        self.orchestrations_dir.mkdir(exist_ok=True)
        
        print("🎯 Enhanced o3 Orchestrator initialized with AI service")
    
    async def generate_orchestration_spec(self, user_query: str) -> Dict[str, Any]:
        """
        Generate orchestration specification using AI-powered analysis
        
        Args:
            user_query: The user's business query
            
        Returns:
            Complete orchestration specification
        """
        print(f"🤖 Phase 2: AI-powered orchestration generation for: {user_query[:50]}...")
        
        try:
            # Step 1: AI analyzes the query
            print("🧠 Step 1: AI query analysis...")
            analysis_result = await self.ai_service.analyze_query(user_query)
            
            # Step 2: AI generates orchestration specification
            print("🎯 Step 2: AI orchestration generation...")
            orchestration_spec = await self.ai_service.generate_orchestration_spec(
                user_query, analysis_result
            )
            
            # Step 3: AI validates the orchestration
            print("🔍 Step 3: AI orchestration validation...")
            validation_result = await self.ai_service.validate_orchestration(orchestration_spec)
            
            # Add validation results to the specification
            orchestration_spec["validation"] = validation_result
            
            # Step 4: Save the orchestration
            await self.save_orchestration_spec(orchestration_spec)
            
            print(f"✅ AI-powered orchestration completed successfully!")
            print(f"📊 Analysis: {analysis_result.get('analysis', {}).get('query_type', 'unknown')} query")
            print(f"🔍 Validation: {'Valid' if validation_result.get('is_valid', False) else 'Issues found'}")
            print(f"🤖 Agents: {len(orchestration_spec.get('workflow', {}).get('agents', []))}")
            
            return orchestration_spec
            
        except Exception as error:
            print(f"❌ AI orchestration failed: {error}")
            print("🔄 Falling back to basic orchestration...")
            
            # Fallback to basic orchestration
            return await self._generate_basic_orchestration(user_query)
    
    async def _generate_basic_orchestration(self, user_query: str) -> Dict[str, Any]:
        """Generate basic orchestration when AI fails (fallback)"""
        print("🔄 Generating basic orchestration as fallback...")
        
        # Simple keyword-based analysis (Phase 1 approach)
        query_lower = user_query.lower()
        
        # Determine agents based on keywords
        agents = []
        
        if any(word in query_lower for word in ['performance', 'analysis', 'summary', 'report']):
            agents.append({
                "agent_id": "operations_summary_agent",
                "activation_trigger": "always",
                "directives": [
                    "Generate operational summary",
                    "Identify key performance metrics",
                    "Highlight critical issues"
                ],
                "data_sources": ["installed_assets", "lead_funnel"],
                "output_format": "json",
                "dependencies": []
            })
        
        if any(word in query_lower for word in ['upsell', 'opportunity', 'sales', 'revenue']):
            agents.append({
                "agent_id": "upsell_discovery_agent",
                "activation_trigger": "after_operations_summary",
                "directives": [
                    "Find upsell opportunities",
                    "Prioritize by potential value",
                    "Include customer context"
                ],
                "data_sources": ["installed_assets", "products"],
                "output_format": "json",
                "dependencies": ["operations_summary_agent"]
            })
        
        if any(word in query_lower for word in ['campaign', 'marketing', 'strategy']):
            agents.append({
                "agent_id": "campaign_planner_agent",
                "activation_trigger": "after_upsell_discovery",
                "directives": [
                    "Create marketing campaign plan",
                    "Define target audience",
                    "Calculate projected revenue"
                ],
                "data_sources": ["lead_funnel", "products"],
                "output_format": "json",
                "dependencies": ["upsell_discovery_agent"]
            })
        
        if any(word in query_lower for word in ['financial', 'roi', 'revenue', 'profit']):
            agents.append({
                "agent_id": "financial_impact_agent",
                "activation_trigger": "after_campaign_planner",
                "directives": [
                    "Calculate financial impact",
                    "Analyze ROI projections",
                    "Provide quarterly forecasts"
                ],
                "data_sources": ["income_statement", "balance_sheet", "cash_flow"],
                "output_format": "json",
                "dependencies": ["campaign_planner_agent"]
            })
        
        # If no specific agents identified, use default
        if not agents:
            agents = [{
                "agent_id": "operations_summary_agent",
                "activation_trigger": "always",
                "directives": [
                    "Analyze operational data",
                    "Generate summary report",
                    "Identify key insights"
                ],
                "data_sources": ["installed_assets", "lead_funnel"],
                "output_format": "json",
                "dependencies": []
            }]
        
        # Create orchestration specification
        orchestration_spec = {
            "orchestration_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "user_query": user_query,
            "ai_generated": False,
            "fallback_used": True,
            "workflow": {
                "agents": agents,
                "execution_order": [agent["agent_id"] for agent in agents],
                "final_synthesis": {
                    "agent_id": "synthesis_agent",
                    "directives": [
                        "Combine all agent outputs into executive summary",
                        "Provide actionable recommendations",
                        "Format for presentation"
                    ]
                }
            },
            "validation": {
                "is_valid": True,
                "issues": ["Fallback orchestration used"],
                "suggestions": ["Consider using AI-powered orchestration for better results"],
                "confidence_score": 0.6
            }
        }
        
        await self.save_orchestration_spec(orchestration_spec)
        return orchestration_spec
    
    async def save_orchestration_spec(self, spec: Dict[str, Any]) -> str:
        """
        Save orchestration specification to file
        
        Args:
            spec: Orchestration specification to save
            
        Returns:
            Path to saved file
        """
        filename = f"orchestration_{spec['orchestration_id']}.json"
        filepath = self.orchestrations_dir / filename
        
        with open(filepath, 'w') as file:
            json.dump(spec, file, indent=2)
        
        print(f"💾 Saved orchestration spec to: {filepath}")
        return str(filepath)
    
    async def load_orchestration_spec(self, orchestration_id: str) -> Optional[Dict[str, Any]]:
        """
        Load orchestration specification from file
        
        Args:
            orchestration_id: ID of the orchestration to load
            
        Returns:
            Orchestration specification or None if not found
        """
        filename = f"orchestration_{orchestration_id}.json"
        filepath = self.orchestrations_dir / filename
        
        if filepath.exists():
            with open(filepath, 'r') as file:
                return json.load(file)
        else:
            print(f"❌ Orchestration file not found: {filepath}")
            return None
    
    async def list_orchestrations(self) -> List[Dict[str, Any]]:
        """
        List all available orchestrations
        
        Returns:
            List of orchestration metadata
        """
        orchestrations = []
        
        for filepath in self.orchestrations_dir.glob("orchestration_*.json"):
            try:
                with open(filepath, 'r') as file:
                    spec = json.load(file)
                    orchestrations.append({
                        "orchestration_id": spec.get("orchestration_id"),
                        "timestamp": spec.get("timestamp"),
                        "user_query": spec.get("user_query"),
                        "ai_generated": spec.get("ai_generated", False),
                        "fallback_used": spec.get("fallback_used", False),
                        "agent_count": len(spec.get("workflow", {}).get("agents", [])),
                        "validation_score": spec.get("validation", {}).get("confidence_score", 0.0)
                    })
            except Exception as error:
                print(f"❌ Error loading orchestration {filepath}: {error}")
        
        return orchestrations
    
    async def validate_orchestration_spec(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate orchestration specification
        
        Args:
            spec: Orchestration specification to validate
            
        Returns:
            Validation result
        """
        try:
            # Use AI service for validation
            return await self.ai_service.validate_orchestration(spec)
        except Exception as error:
            print(f"❌ Validation failed: {error}")
            return {
                "is_valid": False,
                "issues": [f"Validation error: {error}"],
                "suggestions": ["Check orchestration format"],
                "confidence_score": 0.0
            }
    
    def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get orchestrator status and statistics"""
        try:
            orchestrations = list(self.orchestrations_dir.glob("orchestration_*.json"))
            
            # Count AI-generated vs fallback orchestrations
            ai_generated = 0
            fallback_used = 0
            
            for filepath in orchestrations:
                try:
                    with open(filepath, 'r') as file:
                        spec = json.load(file)
                        if spec.get("ai_generated", False):
                            ai_generated += 1
                        if spec.get("fallback_used", False):
                            fallback_used += 1
                except:
                    pass
            
            return {
                "service": "o3_orchestrator",
                "status": "ready",
                "ai_service_available": True,
                "total_orchestrations": len(orchestrations),
                "ai_generated": ai_generated,
                "fallback_used": fallback_used,
                "success_rate": (ai_generated / len(orchestrations)) if orchestrations else 0.0,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as error:
            return {
                "service": "o3_orchestrator",
                "status": "error",
                "error": str(error),
                "timestamp": datetime.utcnow().isoformat()
            }

# Test function for Phase 2
async def test_enhanced_o3_orchestrator():
    """Test enhanced o3 orchestrator with AI integration"""
    print("🧪 Testing Enhanced o3 Orchestrator (Phase 2)")
    
    from fast_mcp_connectors import FastMCPClient
    
    # Initialize components
    fast_mcp_client = FastMCPClient()
    orchestrator = O3Orchestrator(fast_mcp_client)
    
    # Test queries
    test_queries = [
        "Analyze Q2 2025 performance and plan Q3 2025 growth strategy",
        "Find upsell opportunities in EMEA region",
        "Create marketing campaign for new products"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🧪 Test Query {i}: {query}")
        print("-" * 50)
        
        try:
            # Generate orchestration
            orchestration_spec = await orchestrator.generate_orchestration_spec(query)
            
            print(f"✅ Orchestration generated successfully!")
            print(f"🤖 AI Generated: {orchestration_spec.get('ai_generated', False)}")
            print(f"🔄 Fallback Used: {orchestration_spec.get('fallback_used', False)}")
            print(f"📊 Agents: {len(orchestration_spec.get('workflow', {}).get('agents', []))}")
            print(f"🔍 Validation Score: {orchestration_spec.get('validation', {}).get('confidence_score', 0.0):.2f}")
            
        except Exception as error:
            print(f"❌ Test failed: {error}")
    
    # Get orchestrator status
    status = orchestrator.get_orchestrator_status()
    print(f"\n📊 Orchestrator Status: {status}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_enhanced_o3_orchestrator()) 