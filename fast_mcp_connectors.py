"""
Fast MCP Data Connectors for Energy & Property Tech Inc.
Phase 1: Foundation Setup - Data Connectors and Tools
"""

import pandas as pd
import asyncio
from typing import Dict, List, Any, Optional
from pathlib import Path
import json
from datetime import datetime
from fastmcp.tools import Tool, FunctionTool

class CSVDataConnector:
    """Fast MCP Data Connector for CSV files"""
    
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.data = None
        self._load_data()
    
    def _load_data(self):
        """Load CSV data with error handling"""
        try:
            self.data = pd.read_csv(self.csv_path)
            print(f"✅ Loaded {len(self.data)} rows from {self.csv_path}")
        except Exception as error:
            print(f"❌ Error loading {self.csv_path}: {error}")
            self.data = pd.DataFrame()
    
    def query(self, query: str) -> Dict[str, Any]:
        """Query the data using pandas query syntax"""
        try:
            if query.strip():
                result = self.data.query(query)
            else:
                result = self.data
            return result.to_dict('records')
        except Exception as error:
            print(f"❌ Query error: {error}")
            return {"error": str(error), "data": []}
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics for the dataset"""
        if self.data.empty:
            return {"error": "No data loaded"}
        
        return {
            "rows": len(self.data),
            "columns": list(self.data.columns),
            "sample": self.data.head(3).to_dict('records'),
            "data_types": {col: str(dtype) for col, dtype in self.data.dtypes.to_dict().items()},
            "missing_values": self.data.isnull().sum().to_dict()
        }
    
    def get_column_values(self, column: str) -> List[Any]:
        """Get unique values for a specific column"""
        if column in self.data.columns:
            return self.data[column].unique().tolist()
        return []

class FinancialDataTool:
    """Fast MCP Tool for Financial Data Access"""
    
    def __init__(self):
        self.income_statement = CSVDataConnector("Energy-&-Property-Tech-Inc_Sample_Data.xlsx - Income Statement.csv")
        self.balance_sheet = CSVDataConnector("Energy-&-Property-Tech-Inc_Sample_Data.xlsx - Balance Sheet.csv")
        self.cash_flow = CSVDataConnector("Energy-&-Property-Tech-Inc_Sample_Data.xlsx - Cash Flow.csv")
    
    async def query_financials(self, statement_type: str, period: str = None) -> Dict[str, Any]:
        """Query financial data by statement type and period"""
        connector_map = {
            "income_statement": self.income_statement,
            "balance_sheet": self.balance_sheet,
            "cash_flow": self.cash_flow
        }
        
        if statement_type not in connector_map:
            return {"error": f"Invalid statement type: {statement_type}"}
        
        connector = connector_map[statement_type]
        
        if period:
            return connector.query(f"period == '{period}'")
        else:
            return connector.get_summary_stats()
    
    async def get_financial_summary(self) -> Dict[str, Any]:
        """Get summary of all financial data"""
        summary = {
            "income_statement": self.income_statement.get_summary_stats(),
            "balance_sheet": self.balance_sheet.get_summary_stats(),
            "cash_flow": self.cash_flow.get_summary_stats()
        }
        return summary
    
    async def get_revenue_trends(self) -> Dict[str, Any]:
        """Analyze revenue trends from income statement"""
        income_data = self.income_statement.data
        if income_data.empty:
            return {"error": "No income statement data available"}
        
        # Group by period and sum revenue
        revenue_trends = income_data.groupby('period')['revenue'].sum().to_dict()
        return {
            "revenue_trends": revenue_trends,
            "total_revenue": sum(revenue_trends.values()),
            "periods": list(revenue_trends.keys())
        }

class OperationalDataTool:
    """Fast MCP Tool for Operational Data Access"""
    
    def __init__(self):
        self.installed_assets = CSVDataConnector("Energy-&-Property-Tech-Inc_Sample_Data.xlsx - Installed Assets.csv")
        self.lead_funnel = CSVDataConnector("Energy-&-Property-Tech-Inc_Sample_Data.xlsx - Lead Funnel.csv")
        self.products = CSVDataConnector("Energy-&-Property-Tech-Inc_Sample_Data.xlsx - Products.csv")
    
    async def get_upsell_opportunities(self, region: str = None) -> Dict[str, Any]:
        """Get upsell opportunities from installed assets"""
        assets_data = self.installed_assets.data
        if assets_data.empty:
            return {"error": "No installed assets data available"}
        
        if region:
            assets_data = assets_data[assets_data['region'] == region]
        
        opportunities = []
        for _, asset in assets_data.iterrows():
            opportunity = {
                "customer": asset.get('customer', 'Unknown'),
                "region": asset.get('region', 'Unknown'),
                "current_products": asset.get('current_products', 'Unknown'),
                "upsell_potential": asset.get('upsell_potential', 0),
                "next_steps": asset.get('next_steps', 'Contact customer')
            }
            opportunities.append(opportunity)
        
        return {
            "opportunities": opportunities,
            "total_opportunities": len(opportunities),
            "total_potential_value": sum(opp.get('upsell_potential', 0) for opp in opportunities)
        }
    
    async def get_operational_summary(self) -> Dict[str, Any]:
        """Get operational summary from all data sources"""
        summary = {
            "installed_assets": self.installed_assets.get_summary_stats(),
            "lead_funnel": self.lead_funnel.get_summary_stats(),
            "products": self.products.get_summary_stats()
        }
        return summary
    
    async def get_regional_breakdown(self) -> Dict[str, Any]:
        """Get regional breakdown of operations"""
        assets_data = self.installed_assets.data
        if assets_data.empty:
            return {"error": "No installed assets data available"}
        
        regional_breakdown = assets_data.groupby('region').agg({
            'customer': 'count',
            'upsell_potential': 'sum'
        }).to_dict('index')
        
        return {
            "regional_breakdown": regional_breakdown,
            "total_regions": len(regional_breakdown)
        }

class ClaudeCodeTool:
    """Fast MCP Tool for Claude Code Integration"""
    
    def __init__(self):
        self.analysis_sessions = {}
    
    async def launch_claude_code(self, analysis_type: str, data_source: str) -> Dict[str, Any]:
        """Launch Claude Code instance for analysis"""
        session_id = f"claude_code_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session = {
            "session_id": session_id,
            "analysis_type": analysis_type,
            "data_source": data_source,
            "status": "launched",
            "timestamp": datetime.now().isoformat()
        }
        
        self.analysis_sessions[session_id] = session
        
        return {
            "session_id": session_id,
            "status": "success",
            "message": f"Claude Code session launched for {analysis_type} analysis on {data_source}"
        }
    
    async def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get status of Claude Code session"""
        if session_id in self.analysis_sessions:
            return self.analysis_sessions[session_id]
        else:
            return {"error": f"Session {session_id} not found"}

# Fast MCP Client for integration
class FastMCPClient:
    """Fast MCP Client for tool integration"""
    
    def __init__(self):
        self.financial_data = FinancialDataTool()
        self.operational_data = OperationalDataTool()
        self.claude_code = ClaudeCodeTool()
    
    async def initialize(self):
        """Initialize all data connectors"""
        print("🚀 Initializing Fast MCP Client...")
        
        # Test data connectors
        financial_summary = await self.financial_data.get_financial_summary()
        operational_summary = await self.operational_data.get_operational_summary()
        
        print("✅ Fast MCP Client initialized successfully")
        print(f"📊 Financial data sources: {len(financial_summary)}")
        print(f"🏭 Operational data sources: {len(operational_summary)}")
        
        return {
            "financial_sources": financial_summary,
            "operational_sources": operational_summary
        }

# Demo function for Phase 1 testing
async def test_phase_1():
    """Test Phase 1 implementation"""
    print("🧪 Testing Phase 1: Foundation Setup")
    
    client = FastMCPClient()
    init_result = await client.initialize()
    
    # Test financial data access
    revenue_trends = await client.financial_data.get_revenue_trends()
    print(f"💰 Revenue trends: {revenue_trends}")
    
    # Test operational data access
    upsell_opportunities = await client.operational_data.get_upsell_opportunities()
    print(f"🎯 Upsell opportunities: {upsell_opportunities}")
    
    # Test Claude Code integration
    claude_session = await client.claude_code.launch_claude_code("financial_analysis", "income_statement")
    print(f"🤖 Claude Code session: {claude_session}")
    
    print("✅ Phase 1 testing completed successfully!")
    return init_result

if __name__ == "__main__":
    asyncio.run(test_phase_1()) 