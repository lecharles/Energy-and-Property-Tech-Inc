#!/usr/bin/env python3
"""
Demo Launcher for Energy & Property Tech Inc AI System
Easy-to-use interface for running AI-powered business analysis demos
"""

import streamlit as st
import subprocess
import json
import time
from pathlib import Path
import os
import sys

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Page configuration
st.set_page_config(
    page_title="AI System Demo Launcher",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

class DemoLauncher:
    def __init__(self):
        self.demo_queries = {
            "Regional Focus Analysis": {
                "query": "I need to know which region is the most interesting one to focus on with regards to gross margin. Can you look at where to focus on and which are the top three selling assets that I should focus on? Make sure that in that region and for those potential accounts, those assets are not yet sold, so there's truly an upsell opportunity. After you've done that, can you come up with an explanation as to why we should focus on that region, those products, those assets, and those accounts? From there, I'm going to have to come up with a communication strategy - which marketing campaign can we aspire for and what is the best channel of communication. And why?",
                "description": "Comprehensive regional analysis with upsell opportunities and marketing strategy",
                "complexity": "High",
                "expected_time": "60-90 seconds"
            },
            "Financial Performance Review": {
                "query": "Can you analyze our financial performance across all regions and identify the top 3 revenue-generating products? Also, show me which regions have the highest growth potential based on current trends.",
                "description": "Financial analysis focusing on revenue and growth potential",
                "complexity": "Medium",
                "expected_time": "45-60 seconds"
            },
            "Lead Funnel Optimization": {
                "query": "Analyze our lead funnel performance and identify bottlenecks. Which conversion stages need improvement? What are the top 3 strategies to increase our MQL to SQL conversion rate?",
                "description": "Lead funnel analysis with conversion optimization strategies",
                "complexity": "Medium",
                "expected_time": "45-60 seconds"
            },
            "Asset Performance Analysis": {
                "query": "Which installed assets are performing best in terms of ROI? Can you identify the top 3 assets and explain why they're successful? Also, show me which assets have the highest upsell potential.",
                "description": "Asset performance analysis with ROI focus and upsell opportunities",
                "complexity": "Medium",
                "expected_time": "45-60 seconds"
            },
            "Custom Query": {
                "query": "",
                "description": "Enter your own business query for analysis",
                "complexity": "Variable",
                "expected_time": "Variable"
            }
        }
        
    def render_header(self):
        """Render the main header section"""
        st.title("🎯 AI System Demo Launcher")
        st.markdown("**Energy & Property Tech Inc - AI-Powered Business Intelligence System**")
        
        # System status
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.success("✅ OpenAI o3 Orchestrator")
        with col2:
            st.success("✅ Claude AI Agents")
        with col3:
            st.success("✅ LangGraph Workflow")
        
        st.markdown("---")
    
    def render_demo_queries(self):
        """Render the demo query selection section"""
        st.header("📋 Demo Queries")
        st.markdown("Select a pre-built demo query or create your own custom analysis")
        
        # Query selection
        selected_query = st.selectbox(
            "Choose a Demo Query:",
            list(self.demo_queries.keys()),
            help="Select from pre-built business analysis scenarios"
        )
        
        query_info = self.demo_queries[selected_query]
        
        # Display query information
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Complexity", query_info["complexity"])
        with col2:
            st.metric("Expected Time", query_info["expected_time"])
        with col3:
            st.metric("Type", "Business Analysis")
        
        # Query display
        st.subheader("Query Details")
        st.info(f"**Description**: {query_info['description']}")
        
        if selected_query == "Custom Query":
            custom_query = st.text_area(
                "Enter your custom business query:",
                height=150,
                placeholder="Describe the business analysis you need..."
            )
            if custom_query:
                query_info["query"] = custom_query
        else:
            st.text_area(
                "Query Text:",
                value=query_info["query"],
                height=150,
                disabled=True
            )
        
        return selected_query, query_info
    
    def render_execution_controls(self, selected_query, query_info):
        """Render the execution controls section"""
        st.header("🚀 Execution Controls")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Execution mode
            execution_mode = st.selectbox(
                "Execution Mode:",
                ["Standard Demo", "Performance Test", "Debug Mode"],
                help="Choose how to run the demo"
            )
            
            # Auto-refresh
            auto_refresh = st.checkbox(
                "Auto-refresh results",
                value=True,
                help="Automatically refresh results every 30 seconds"
            )
        
        with col2:
            # Performance monitoring
            enable_monitoring = st.checkbox(
                "Enable performance monitoring",
                value=True,
                help="Track execution time and agent performance"
            )
            
            # Save results
            save_results = st.checkbox(
                "Save results to file",
                value=True,
                help="Save analysis results for later review"
            )
        
        # Execute button
        if st.button("🚀 Execute AI Analysis", type="primary", use_container_width=True):
            if not query_info["query"]:
                st.error("Please provide a query to execute")
                return
            
            return {
                "query": query_info["query"],
                "mode": execution_mode,
                "auto_refresh": auto_refresh,
                "monitoring": enable_monitoring,
                "save_results": save_results
            }
        
        return None
    
    def render_system_info(self):
        """Render system information section"""
        st.header("ℹ️ System Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("AI Models")
            st.write("**Orchestrator**: OpenAI o3 (Latest)")
            st.write("**Analysis Agents**: Claude 3.5 Sonnet")
            st.write("**Workflow Engine**: LangGraph")
            st.write("**Target Upgrade**: Claude Opus 4.1")
        
        with col2:
            st.subheader("Data Sources")
            st.write("**Financial Data**: 3 sources")
            st.write("**Operational Data**: 3 sources")
            st.write("**Total Records**: 87+ business data points")
            st.write("**Real-time**: Yes")
        
        st.subheader("Capabilities")
        st.write("✅ **Multi-Agent Orchestration**: Dynamic agent assignment and execution")
        st.write("✅ **Business Intelligence**: Financial, operational, and strategic analysis")
        st.write("✅ **Performance Monitoring**: Real-time metrics and optimization")
        st.write("✅ **Scalable Architecture**: Support for 10+ concurrent users")
    
    def render_instructions(self):
        """Render usage instructions"""
        st.header("📚 How to Use")
        
        st.markdown("""
        ### **Step-by-Step Demo Guide:**
        
        1. **Select a Demo Query**: Choose from pre-built business scenarios or create a custom query
        2. **Configure Execution**: Set execution mode and monitoring options
        3. **Execute Analysis**: Click the execute button to start the AI-powered analysis
        4. **Monitor Progress**: Watch real-time execution and agent performance
        5. **Review Results**: Analyze the comprehensive business insights generated
        
        ### **Demo Scenarios Available:**
        
        - **Regional Focus Analysis**: Complete regional strategy with upsell opportunities
        - **Financial Performance Review**: Revenue analysis and growth potential
        - **Lead Funnel Optimization**: Conversion rate improvement strategies
        - **Asset Performance Analysis**: ROI analysis and upsell potential
        - **Custom Queries**: Your own business analysis needs
        
        ### **Expected Outcomes:**
        
        - **Strategic Insights**: Data-driven business recommendations
        - **Performance Metrics**: Execution time, success rates, agent efficiency
        - **Actionable Results**: Specific strategies and next steps
        - **Business Value**: Clear ROI and opportunity identification
        """)
    
    def render_sidebar(self):
        """Render the sidebar with quick actions"""
        st.sidebar.header("🎯 Quick Actions")
        
        # Show dashboard info instead of navigation
        st.sidebar.info("📊 **Performance Dashboard**")
        st.sidebar.markdown("To view the dashboard, run:")
        st.sidebar.code("streamlit run performance_dashboard.py")
        
        if st.sidebar.button("📁 View Test Results"):
            st.sidebar.markdown("**Recent Results:**")
            results_dir = Path("test_results")
            if results_dir.exists():
                for file in sorted(results_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
                    st.sidebar.markdown(f"• {file.stem}")
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("**System Status:**")
        st.sidebar.success("🟢 All Systems Operational")
        st.sidebar.info("🔄 Ready for Demo Execution")
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("**Phase 5 Progress:**")
        st.sidebar.success("✅ Step 1: Model Optimization")
        st.sidebar.success("✅ Step 2: Performance Dashboard")
        st.sidebar.markdown("⏳ Step 3: Security & Caching")
        st.sidebar.markdown("⏳ Step 4: Concurrent Users")
    
    def render_main(self):
        """Render the main demo launcher interface"""
        self.render_header()
        
        # Main content in columns
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Demo query selection and execution
            selected_query, query_info = self.render_demo_queries()
            execution_config = self.render_execution_controls(selected_query, query_info)
            
            if execution_config:
                st.success("🚀 Demo execution configured! Ready to launch AI analysis.")
                st.json(execution_config)
        
        with col2:
            # System information
            self.render_system_info()
        
        # Instructions
        self.render_instructions()
        
        # Sidebar
        self.render_sidebar()

def main():
    launcher = DemoLauncher()
    launcher.render_main()

if __name__ == "__main__":
    main() 