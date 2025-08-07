"""
Claude Agents for Phase 3: Real Agent Implementations
=====================================================

This module implements real, intelligent Claude-powered agents that replace
the mock agents from Phase 2. Each agent uses Claude's reasoning capabilities
to analyze data and generate meaningful business insights.

Architecture:
- BaseClaudeAgent: Abstract base class for all Claude agents
- OperationsSummaryAgent: Analyzes operational data and performance
- UpsellDiscoveryAgent: Finds and prioritizes upsell opportunities  
- CampaignPlannerAgent: Creates targeted marketing campaigns
- FinancialImpactAgent: Calculates financial impact and ROI
- SynthesisAgent: Combines all agent outputs into executive summary

Each agent integrates with Fast MCP data sources and uses Claude's
intelligence to provide real business analysis and recommendations.
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
import anthropic
from dotenv import load_dotenv
import pandas as pd
import numpy as np

# Load environment variables
load_dotenv()

# Import our Fast MCP connectors
from fast_mcp_connectors import FastMCPClient

class BaseClaudeAgent(ABC):
    """
    Abstract base class for all Claude-powered agents
    
    This class provides the foundation for intelligent agents that use
    Claude's reasoning capabilities to analyze data and generate insights.
    Each agent specializes in a specific business domain and can access
    Fast MCP data sources for real-time analysis.
    """
    
    def __init__(self, agent_id: str, fast_mcp_client: FastMCPClient):
        """
        Initialize the base Claude agent
        
        Args:
            agent_id: Unique identifier for the agent
            fast_mcp_client: Fast MCP client for data access
        """
        self.agent_id = agent_id
        self.fast_mcp_client = fast_mcp_client
        
        # Initialize Claude client
        load_dotenv()  # Load environment variables
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.anthropic_api_key or self.anthropic_api_key == 'your_anthropic_api_key_here':
            raise ValueError("Anthropic API key not configured. Please set ANTHROPIC_API_KEY in your .env file.")
        
        self.claude_client = anthropic.Anthropic(api_key=self.anthropic_api_key)
        self.model = "claude-3-5-sonnet-20241022"  # Using Claude 3.5 Sonnet for analysis
        
        print(f"🤖 {self.agent_id} initialized with Claude {self.model}")
    
    def _convert_to_json_serializable(self, obj: Any) -> Any:
        """
        Convert pandas/numpy objects to JSON-serializable formats
        
        Args:
            obj: Object to convert
            
        Returns:
            JSON-serializable object
        """
        if isinstance(obj, pd.DataFrame):
            return obj.to_dict('records')
        elif isinstance(obj, pd.Series):
            return obj.to_dict()
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: self._convert_to_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_json_serializable(item) for item in obj]
        else:
            return obj
    
    @abstractmethod
    async def execute(self, directives: List[str], data_sources: List[str]) -> Dict[str, Any]:
        """
        Execute the agent's analysis using Claude's intelligence
        
        Args:
            directives: List of specific instructions for the agent
            data_sources: List of data sources to analyze
            
        Returns:
            Dictionary containing the agent's analysis results
        """
        pass
    
    async def _call_claude(self, prompt: str) -> str:
        """
        Make a call to Claude API for intelligent analysis
        
        Args:
            prompt: The prompt to send to Claude
            
        Returns:
            Claude's response as a string
        """
        try:
            response = self.claude_client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.3,  # Conservative temperature for business analysis
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            return response.content[0].text
            
        except Exception as error:
            print(f"❌ Claude API call failed: {error}")
            raise error
    
    async def _get_data_from_sources(self, data_sources: List[str]) -> Dict[str, Any]:
        """
        Retrieve data from Fast MCP data sources
        
        Args:
            data_sources: List of data source names to retrieve
            
        Returns:
            Dictionary containing data from all sources
        """
        data = {}
        
        try:
            for source in data_sources:
                if source == "installed_assets":
                    # Get installed assets data from operational summary
                    operational_summary = await self.fast_mcp_client.operational_data.get_operational_summary()
                    data[source] = operational_summary.get("installed_assets", {})
                elif source == "lead_funnel":
                    # Get lead funnel data from operational summary
                    operational_summary = await self.fast_mcp_client.operational_data.get_operational_summary()
                    data[source] = operational_summary.get("lead_funnel", {})
                elif source == "products":
                    # Get products data from operational summary
                    operational_summary = await self.fast_mcp_client.operational_data.get_operational_summary()
                    data[source] = operational_summary.get("products", {})
                elif source == "income_statement":
                    # Get income statement data from financial summary
                    financial_summary = await self.fast_mcp_client.financial_data.get_financial_summary()
                    data[source] = financial_summary.get("income_statement", {})
                elif source == "balance_sheet":
                    # Get balance sheet data from financial summary
                    financial_summary = await self.fast_mcp_client.financial_data.get_financial_summary()
                    data[source] = financial_summary.get("balance_sheet", {})
                elif source == "cash_flow":
                    # Get cash flow data from financial summary
                    financial_summary = await self.fast_mcp_client.financial_data.get_financial_summary()
                    data[source] = financial_summary.get("cash_flow", {})
                else:
                    print(f"⚠️ Unknown data source: {source}")
            
            # Convert data to JSON-serializable format
            serializable_data = self._convert_to_json_serializable(data)
            return serializable_data
            
        except Exception as error:
            print(f"❌ Error retrieving data: {error}")
            return {}
    
    def format_output(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format the agent's output with metadata
        
        Args:
            analysis_result: The agent's analysis results
            
        Returns:
            Formatted output with metadata
        """
        return {
            "agent_id": self.agent_id,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "completed",
            "model_used": self.model,
            "analysis": analysis_result
        }

class OperationsSummaryAgent(BaseClaudeAgent):
    """
    Claude-powered agent for operational data analysis
    
    This agent analyzes operational data including installed assets,
    lead funnel, and performance metrics to provide comprehensive
    operational insights and identify critical issues.
    """
    
    def __init__(self, fast_mcp_client: FastMCPClient):
        super().__init__("operations_summary_agent", fast_mcp_client)
    
    async def execute(self, directives: List[str], data_sources: List[str]) -> Dict[str, Any]:
        """
        Execute operations analysis using Claude's intelligence
        
        Args:
            directives: List of specific instructions for operations analysis
            data_sources: List of operational data sources to analyze
            
        Returns:
            Dictionary containing operational analysis results
        """
        print(f"🏭 {self.agent_id} executing with {len(directives)} directives...")
        
        try:
            # Retrieve operational data
            data = await self._get_data_from_sources(data_sources)
            
            # Create analysis prompt for Claude
            prompt = self._create_operations_prompt(directives, data)
            
            # Get Claude's analysis
            claude_response = await self._call_claude(prompt)
            
            # Parse Claude's response
            analysis_result = self._parse_operations_analysis(claude_response)
            
            print(f"✅ {self.agent_id} completed analysis")
            return self.format_output(analysis_result)
            
        except Exception as error:
            print(f"❌ {self.agent_id} execution failed: {error}")
            return self.format_output({
                "error": str(error),
                "status": "failed"
            })
    
    def _create_operations_prompt(self, directives: List[str], data: Dict[str, Any]) -> str:
        """Create Claude prompt for operations analysis"""
        return f"""
You are an expert operations analyst for Energy & Property Tech Inc. Analyze the following operational data and provide comprehensive insights.

DIRECTIVES:
{chr(10).join(f"- {directive}" for directive in directives)}

OPERATIONAL DATA:
{json.dumps(data, indent=2)}

Please provide a comprehensive analysis including:
1. Operational Performance Summary
2. Key Performance Indicators (KPIs)
3. Critical Issues and Risks
4. Regional Performance Breakdown
5. Asset Utilization Analysis
6. Operational Efficiency Metrics
7. Recommendations for Improvement

CRITICAL REQUIREMENTS FOR ALL NUMERICAL VALUES:

1. CURRENCY VALUES - Always include currency symbol:
   - Revenue: "$15,000" or "€15,000"
   - Costs: "$5,000" or "€5,000"
   - Budget: "$50,000" or "€50,000"

2. PERCENTAGES - Always include % symbol:
   - Performance scores: "85%"
   - Utilization rates: "75%"
   - Efficiency metrics: "90%"

3. COUNTS/QUANTITIES - Always specify what is being counted:
   - Total Assets: "150 assets"
   - Customer Count: "500 customers"
   - Regional Count: "5 regions"

4. TIME VALUES - Use readable format:
   - Processing Time: "2.5 hours"
   - Response Time: "45 minutes"
   - Timeline: "2025-03-01 to 2025-12-31"

5. ACRONYM DEFINITIONS - Always explain acronyms:
   - KPI = Key Performance Indicator
   - ROI = Return on Investment
   - SLA = Service Level Agreement
   - MTTR = Mean Time to Repair
   - MTBF = Mean Time Between Failures

6. SYSTEM METRICS - Include units:
   - Memory Usage: "50%" (not 0.5)
   - CPU Usage: "75%"
   - Performance Score: "85%"

7. DATES - Use current year (2025) and future dates:
   - Analysis Date: "2025-08-07"
   - Target Date: "2025-12-31"
   - Milestone Date: "2025-06-15"

FORMAT YOUR OUTPUT AS JSON WITH THESE REQUIREMENTS:
- All monetary values must include currency symbol
- All percentages must include % symbol
- All counts must specify what is being counted
- All acronyms must be defined in the output
- All timestamps must be in readable datetime format
- All system metrics must be in percentage format

EXAMPLE FORMAT:
{{
  "performance_summary": {{
    "overall_score": "85%",
    "total_revenue": "$15M",
    "asset_utilization": "75%"
  }},
  "regional_breakdown": {{
    "north_america": {{
      "revenue": "$8M",
      "performance": "90%",
      "asset_count": "75 assets"
    }}
  }},
  "kpis": {{
    "roi": "250% (Return on Investment)",
    "efficiency": "85%",
    "customer_satisfaction": "92%"
  }}
}}
"""
    
    def _parse_operations_analysis(self, claude_response: str) -> Dict[str, Any]:
        """Parse Claude's operations analysis response"""
        try:
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', claude_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback: create structured response from text
                return {
                    "operational_summary": {
                        "analysis": claude_response,
                        "status": "text_analysis"
                    },
                    "key_insights": ["Analysis completed via text parsing"],
                    "recommendations": ["Review full analysis for detailed recommendations"]
                }
        except Exception as error:
            print(f"❌ Error parsing operations analysis: {error}")
            return {
                "error": f"Failed to parse analysis: {error}",
                "raw_response": claude_response
            }

class UpsellDiscoveryAgent(BaseClaudeAgent):
    """
    Claude-powered agent for upsell opportunity discovery
    
    This agent analyzes customer data, installed assets, and product
    information to identify and prioritize upsell opportunities.
    """
    
    def __init__(self, fast_mcp_client: FastMCPClient):
        super().__init__("upsell_discovery_agent", fast_mcp_client)
    
    async def execute(self, directives: List[str], data_sources: List[str]) -> Dict[str, Any]:
        """
        Execute upsell discovery analysis using Claude's intelligence
        
        Args:
            directives: List of specific instructions for upsell analysis
            data_sources: List of data sources to analyze for opportunities
            
        Returns:
            Dictionary containing upsell opportunity analysis
        """
        print(f"💰 {self.agent_id} executing with {len(directives)} directives...")
        
        try:
            # Retrieve customer and product data
            data = await self._get_data_from_sources(data_sources)
            
            # Create analysis prompt for Claude
            prompt = self._create_upsell_prompt(directives, data)
            
            # Get Claude's analysis
            claude_response = await self._call_claude(prompt)
            
            # Parse Claude's response
            analysis_result = self._parse_upsell_analysis(claude_response)
            
            print(f"✅ {self.agent_id} completed analysis")
            return self.format_output(analysis_result)
            
        except Exception as error:
            print(f"❌ {self.agent_id} execution failed: {error}")
            return self.format_output({
                "error": str(error),
                "status": "failed"
            })
    
    def _create_upsell_prompt(self, directives: List[str], data: Dict[str, Any]) -> str:
        """Create Claude prompt for upsell analysis"""
        return f"""
You are an expert sales analyst for Energy & Property Tech Inc. Analyze the following data to identify and prioritize upsell opportunities.

DIRECTIVES:
{chr(10).join(f"- {directive}" for directive in directives)}

CUSTOMER AND PRODUCT DATA:
{json.dumps(data, indent=2)}

Please provide a comprehensive upsell analysis including:
1. Customer Segmentation Analysis
2. Upsell Opportunity Identification
3. Revenue Potential Calculation
4. Customer Prioritization
5. Product Recommendation Strategy
6. Regional Opportunity Analysis
7. Implementation Recommendations

CRITICAL REQUIREMENTS FOR ALL NUMERICAL VALUES:

1. CURRENCY VALUES - Always include currency symbol:
   - Revenue: "$15,000" or "€15,000"
   - Potential Revenue: "$50,000" or "€50,000"
   - Customer Value: "$25,000" or "€25,000"

2. PERCENTAGES - Always include % symbol:
   - Conversion rates: "15%"
   - Confidence scores: "85%"
   - Success rates: "75%"

3. COUNTS/QUANTITIES - Always specify what is being counted:
   - Total Opportunities: "12 opportunities"
   - Customer Count: "150 customers"
   - Product Count: "25 products"

4. TIME VALUES - Use readable format:
   - Implementation Time: "3 months"
   - Sales Cycle: "45 days"
   - Timeline: "2025-03-01 to 2025-12-31"

5. ACRONYM DEFINITIONS - Always explain acronyms:
   - LTV = Lifetime Value
   - ARR = Annual Recurring Revenue
   - MRR = Monthly Recurring Revenue
   - CAC = Customer Acquisition Cost
   - CLV = Customer Lifetime Value

6. SYSTEM METRICS - Include units:
   - Memory Usage: "50%" (not 0.5)
   - CPU Usage: "75%"
   - Performance Score: "85%"

7. DATES - Use current year (2025) and future dates:
   - Implementation Date: "2025-03-01"
   - Target Date: "2025-12-31"
   - Milestone Date: "2025-06-15"

FORMAT YOUR OUTPUT AS JSON WITH THESE REQUIREMENTS:
- All monetary values must include currency symbol
- All percentages must include % symbol
- All counts must specify what is being counted
- All acronyms must be defined in the output
- All timestamps must be in readable datetime format
- All system metrics must be in percentage format

EXAMPLE FORMAT:
{{
  "total_opportunities": "12 opportunities",
  "potential_revenue": "$2.5M",
  "confidence_score": "85%",
  "implementation_timeline": "3 months",
  "customer_segments": {{
    "enterprise": "150 customers",
    "mid_market": "75 customers"
  }},
  "revenue_breakdown": {{
    "product_a": "$500,000",
    "product_b": "$750,000"
  }}
}}
"""
    
    def _parse_upsell_analysis(self, claude_response: str) -> Dict[str, Any]:
        """Parse Claude's upsell analysis response"""
        try:
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', claude_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback: create structured response from text
                return {
                    "upsell_opportunities": [],
                    "total_upsell_potential": 0,
                    "analysis": claude_response,
                    "status": "text_analysis"
                }
        except Exception as error:
            print(f"❌ Error parsing upsell analysis: {error}")
            return {
                "error": f"Failed to parse analysis: {error}",
                "raw_response": claude_response
            }

class CampaignPlannerAgent(BaseClaudeAgent):
    """
    Claude-powered agent for marketing campaign planning
    
    This agent creates targeted marketing campaigns based on customer
    data, product information, and market analysis.
    """
    
    def __init__(self, fast_mcp_client: FastMCPClient):
        super().__init__("campaign_planner_agent", fast_mcp_client)
    
    async def execute(self, directives: List[str], data_sources: List[str]) -> Dict[str, Any]:
        """
        Execute campaign planning using Claude's intelligence
        
        Args:
            directives: List of specific instructions for campaign planning
            data_sources: List of data sources for campaign analysis
            
        Returns:
            Dictionary containing campaign plan
        """
        print(f"📢 {self.agent_id} executing with {len(directives)} directives...")
        
        try:
            # Retrieve campaign data
            data = await self._get_data_from_sources(data_sources)
            
            # Create analysis prompt for Claude
            prompt = self._create_campaign_prompt(directives, data)
            
            # Get Claude's analysis
            claude_response = await self._call_claude(prompt)
            
            # Parse Claude's response
            analysis_result = self._parse_campaign_analysis(claude_response)
            
            print(f"✅ {self.agent_id} completed analysis")
            return self.format_output(analysis_result)
            
        except Exception as error:
            print(f"❌ {self.agent_id} execution failed: {error}")
            return self.format_output({
                "error": str(error),
                "status": "failed"
            })
    
    def _create_campaign_prompt(self, directives: List[str], data: Dict[str, Any]) -> str:
        """Create Claude prompt for campaign planning"""
        return f"""
You are an expert marketing strategist for Energy & Property Tech Inc. Create a comprehensive marketing campaign plan based on the following data.

DIRECTIVES:
{chr(10).join(f"- {directive}" for directive in directives)}

CAMPAIGN DATA:
{json.dumps(data, indent=2)}

Please create a comprehensive campaign plan including:
1. Target Audience Segmentation
2. Campaign Strategy and Messaging
3. Channel Selection and Distribution
4. Timeline and Milestones
5. Budget Allocation
6. Success Metrics and KPIs
7. Risk Assessment and Mitigation

CRITICAL REQUIREMENTS FOR ALL NUMERICAL VALUES:

1. CURRENCY VALUES - Always include currency symbol:
   - Revenue: "$15,000" or "€15,000"
   - Budget: "$50,000" or "€50,000"
   - Total Addressable Market: "$2.5M" or "€2.5M"

2. PERCENTAGES - Always include % symbol:
   - Conversion rates: "15%"
   - ROI: "250%"
   - Confidence scores: "85%"

3. COUNTS/QUANTITIES - Always specify what is being counted:
   - MQL Target: "2,500 leads" (Marketing Qualified Leads)
   - SQL Target: "500 leads" (Sales Qualified Leads)
   - Expected Reach: "150,000 companies" or "150,000 potential customers"
   - Total Opportunities: "12 opportunities"

4. TIME VALUES - Use readable format:
   - Start Time: "2025-03-01 09:00:00"
   - End Time: "2025-12-31 17:00:00"
   - Duration: "45 minutes" or "2.5 hours"

5. ACRONYM DEFINITIONS - Always explain acronyms:
   - MQL = Marketing Qualified Lead
   - SQL = Sales Qualified Lead
   - CAC = Customer Acquisition Cost
   - ROMI = Return on Marketing Investment
   - LTV = Lifetime Value
   - CTR = Click-Through Rate

6. SYSTEM METRICS - Include units:
   - Memory Usage: "50%" (not 0.5)
   - CPU Usage: "75%"
   - Performance Score: "85%"

7. DATES - Use current year (2025) and future dates:
   - Campaign Start: "2025-03-01"
   - Campaign End: "2025-12-31"
   - Milestone Date: "2025-06-15"

FORMAT YOUR OUTPUT AS JSON WITH THESE REQUIREMENTS:
- All monetary values must include currency symbol
- All percentages must include % symbol
- All counts must specify what is being counted
- All acronyms must be defined in the output
- All timestamps must be in readable datetime format
- All system metrics must be in percentage format

EXAMPLE FORMAT:
{{
  "campaign_name": "EnergyTech Innovation Summit 2025",
  "total_addressable_market": "$2.5M",
  "expected_reach": "150,000 potential customers",
  "mql_target": "2,500 leads (Marketing Qualified Leads)",
  "sql_target": "500 leads (Sales Qualified Leads)",
  "cac_target": "$150 per lead (Customer Acquisition Cost)",
  "romi_target": "300% (Return on Marketing Investment)",
  "start_time": "2025-03-01 09:00:00",
  "end_time": "2025-12-31 17:00:00",
  "budget_allocation": {{
    "digital_marketing": "$400,000",
    "events": "$300,000",
    "content_creation": "$200,000"
  }}
}}
"""
    
    def _parse_campaign_analysis(self, claude_response: str) -> Dict[str, Any]:
        """Parse Claude's campaign analysis response"""
        try:
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', claude_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback: create structured response from text
                return {
                    "campaign_plan": {
                        "analysis": claude_response,
                        "status": "text_analysis"
                    },
                    "projected_results": {},
                    "recommendations": ["Review full analysis for detailed plan"]
                }
        except Exception as error:
            print(f"❌ Error parsing campaign analysis: {error}")
            return {
                "error": f"Failed to parse analysis: {error}",
                "raw_response": claude_response
            }

class FinancialImpactAgent(BaseClaudeAgent):
    """
    Claude-powered agent for financial impact analysis
    
    This agent analyzes financial data to calculate ROI, projections,
    and financial impact of business decisions.
    """
    
    def __init__(self, fast_mcp_client: FastMCPClient):
        super().__init__("financial_impact_agent", fast_mcp_client)
    
    async def execute(self, directives: List[str], data_sources: List[str]) -> Dict[str, Any]:
        """
        Execute financial impact analysis using Claude's intelligence
        
        Args:
            directives: List of specific instructions for financial analysis
            data_sources: List of financial data sources to analyze
            
        Returns:
            Dictionary containing financial impact analysis
        """
        print(f"💰 {self.agent_id} executing with {len(directives)} directives...")
        
        try:
            # Retrieve financial data
            data = await self._get_data_from_sources(data_sources)
            
            # Create analysis prompt for Claude
            prompt = self._create_financial_prompt(directives, data)
            
            # Get Claude's analysis
            claude_response = await self._call_claude(prompt)
            
            # Parse Claude's response
            analysis_result = self._parse_financial_analysis(claude_response)
            
            print(f"✅ {self.agent_id} completed analysis")
            return self.format_output(analysis_result)
            
        except Exception as error:
            print(f"❌ {self.agent_id} execution failed: {error}")
            return self.format_output({
                "error": str(error),
                "status": "failed"
            })
    
    def _create_financial_prompt(self, directives: List[str], data: Dict[str, Any]) -> str:
        """Create Claude prompt for financial analysis"""
        return f"""
You are an expert financial analyst for Energy & Property Tech Inc. Analyze the following financial data to calculate impact, ROI, and projections.

DIRECTIVES:
{chr(10).join(f"- {directive}" for directive in directives)}

FINANCIAL DATA:
{json.dumps(data, indent=2)}

Please provide a comprehensive financial analysis including:
1. Current Financial Performance
2. ROI Analysis and Calculations
3. Revenue Projections
4. Cost-Benefit Analysis
5. Risk Assessment
6. Financial Recommendations
7. Quarterly Forecasts

CRITICAL REQUIREMENTS FOR ALL NUMERICAL VALUES:

1. CURRENCY VALUES - Always include currency symbol:
   - Revenue: "$15,000" or "€15,000"
   - Costs: "$5,000" or "€5,000"
   - Budget: "$50,000" or "€50,000"
   - NPV: "$100,000" or "€100,000"

2. PERCENTAGES - Always include % symbol:
   - ROI: "250%"
   - Growth rate: "15%"
   - Profit margin: "25%"
   - IRR: "18%"

3. COUNTS/QUANTITIES - Always specify what is being counted:
   - Payback period: "2.5 years"
   - Project duration: "12 months"
   - Customer count: "500 customers"

4. TIME VALUES - Use readable format:
   - Payback period: "2.5 years"
   - Project timeline: "12 months"
   - Forecast period: "2025-2026"

5. ACRONYM DEFINITIONS - Always explain acronyms:
   - ROI = Return on Investment
   - NPV = Net Present Value
   - IRR = Internal Rate of Return
   - EBITDA = Earnings Before Interest, Taxes, Depreciation, and Amortization
   - ARR = Annual Recurring Revenue

6. SYSTEM METRICS - Include units:
   - Memory Usage: "50%" (not 0.5)
   - CPU Usage: "75%"
   - Performance Score: "85%"

7. DATES - Use current year (2025) and future dates:
   - Analysis Date: "2025-08-07"
   - Forecast Period: "2025-2026"
   - Project Start: "2025-03-01"

FORMAT YOUR OUTPUT AS JSON WITH THESE REQUIREMENTS:
- All monetary values must include currency symbol
- All percentages must include % symbol
- All counts must specify what is being counted
- All acronyms must be defined in the output
- All timestamps must be in readable datetime format
- All system metrics must be in percentage format

EXAMPLE FORMAT:
{{
  "financial_performance": {{
    "current_revenue": "$15M",
    "profit_margin": "25%",
    "growth_rate": "15%"
  }},
  "roi_analysis": {{
    "total_roi": "250% (Return on Investment)",
    "payback_period": "2.5 years",
    "npv": "$100,000 (Net Present Value)",
    "irr": "18% (Internal Rate of Return)"
  }},
  "projections": {{
    "q1_2025": {{
      "revenue": "$4M",
      "growth": "12%"
    }}
  }}
}}
"""
    
    def _parse_financial_analysis(self, claude_response: str) -> Dict[str, Any]:
        """Parse Claude's financial analysis response"""
        try:
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', claude_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback: create structured response from text
                return {
                    "financial_performance": {
                        "analysis": claude_response,
                        "status": "text_analysis"
                    },
                    "roi_analysis": {},
                    "projections": {},
                    "recommendations": ["Review full analysis for detailed financial insights"]
                }
        except Exception as error:
            print(f"❌ Error parsing financial analysis: {error}")
            return {
                "error": f"Failed to parse analysis: {error}",
                "raw_response": claude_response
            }

class SynthesisAgent(BaseClaudeAgent):
    """
    Claude-powered agent for synthesizing all agent outputs
    
    This agent combines the outputs from all other agents to create
    a comprehensive executive summary with actionable recommendations.
    """
    
    def __init__(self, fast_mcp_client: FastMCPClient):
        super().__init__("synthesis_agent", fast_mcp_client)
    
    async def execute(self, agent_results: Dict[str, Any], user_query: str) -> Dict[str, Any]:
        """
        Execute synthesis of all agent outputs using Claude's intelligence
        
        Args:
            agent_results: Dictionary containing results from all agents
            user_query: Original user query for context
            
        Returns:
            Dictionary containing synthesized executive summary
        """
        print(f"🎯 {self.agent_id} synthesizing {len(agent_results)} agent outputs...")
        
        try:
            # Create synthesis prompt for Claude
            prompt = self._create_synthesis_prompt(agent_results, user_query)
            
            # Get Claude's synthesis
            claude_response = await self._call_claude(prompt)
            
            # Parse Claude's response
            synthesis_result = self._parse_synthesis(claude_response)
            
            print(f"✅ {self.agent_id} completed synthesis")
            return self.format_output(synthesis_result)
            
        except Exception as error:
            print(f"❌ {self.agent_id} synthesis failed: {error}")
            return self.format_output({
                "error": str(error),
                "status": "failed"
            })
    
    def _create_synthesis_prompt(self, agent_results: Dict[str, Any], user_query: str) -> str:
        """Create Claude prompt for synthesis"""
        return f"""
You are an expert business strategist for Energy & Property Tech Inc. Synthesize the following agent analyses into a comprehensive executive summary.

ORIGINAL USER QUERY:
{user_query}

AGENT ANALYSES:
{json.dumps(agent_results, indent=2)}

Please create a comprehensive executive summary including:
1. Executive Summary
2. Key Insights from All Analyses
3. Strategic Recommendations
4. Risk Assessment
5. Implementation Roadmap
6. Success Metrics
7. Next Steps

Format your response as a JSON object with the following structure:
{{
    "executive_summary": {{
        "overview": "string",
        "key_findings": ["list of findings"],
        "strategic_implications": "string"
    }},
    "key_insights": [
        "list of insights from all analyses"
    ],
    "strategic_recommendations": [
        "list of high-level recommendations"
    ],
    "implementation_roadmap": {{
        "phase_1": "object",
        "phase_2": "object",
        "phase_3": "object"
    }},
    "risk_assessment": {{
        "overall_risk": "low/medium/high",
        "risk_factors": ["list of factors"],
        "mitigation_strategies": ["list of strategies"]
    }},
    "success_metrics": {{
        "kpis": ["list of KPIs"],
        "targets": "object",
        "timeline": "string"
    }},
    "next_steps": [
        "list of immediate next steps"
    ]
}}
"""
    
    def _parse_synthesis(self, claude_response: str) -> Dict[str, Any]:
        """Parse Claude's synthesis response"""
        try:
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', claude_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback: create structured response from text
                return {
                    "executive_summary": {
                        "synthesis": claude_response,
                        "status": "text_synthesis"
                    },
                    "key_insights": ["Review full synthesis for comprehensive insights"],
                    "strategic_recommendations": ["Review full synthesis for detailed recommendations"]
                }
        except Exception as error:
            print(f"❌ Error parsing synthesis: {error}")
            return {
                "error": f"Failed to parse synthesis: {error}",
                "raw_response": claude_response
            }

# Agent factory for creating agents
class ClaudeAgentFactory:
    """Factory for creating Claude-powered agents"""
    
    @staticmethod
    def create_agent(agent_id: str, fast_mcp_client: FastMCPClient) -> BaseClaudeAgent:
        """
        Create a Claude agent based on agent ID
        
        Args:
            agent_id: The type of agent to create
            fast_mcp_client: Fast MCP client for data access
            
        Returns:
            Instance of the specified agent type
        """
        if agent_id == "operations_summary_agent":
            return OperationsSummaryAgent(fast_mcp_client)
        elif agent_id == "upsell_discovery_agent":
            return UpsellDiscoveryAgent(fast_mcp_client)
        elif agent_id == "campaign_planner_agent":
            return CampaignPlannerAgent(fast_mcp_client)
        elif agent_id == "financial_impact_agent":
            return FinancialImpactAgent(fast_mcp_client)
        elif agent_id == "synthesis_agent":
            return SynthesisAgent(fast_mcp_client)
        else:
            raise ValueError(f"Unknown agent type: {agent_id}") 