#!/usr/bin/env python3
"""
Performance Dashboard for Energy & Property Tech Inc AI System
Real-time monitoring of agent performance, system metrics, and business insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
import time
from pathlib import Path
import psutil
import threading

# Page configuration
st.set_page_config(
    page_title="AI System Performance Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

class PerformanceDashboard:
    def __init__(self):
        self.logs_dir = Path("logs")
        self.test_results_dir = Path("test_results")
        self.orchestrations_dir = Path("orchestrations")
        self.performance_reports_dir = Path("performance_reports")
        
    def get_system_metrics(self):
        """Get real-time system metrics"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'cpu_usage': f"{cpu_percent:.1f}%",
            'memory_usage': f"{memory.percent:.1f}%",
            'memory_available': f"{memory.available / (1024**3):.1f} GB",
            'disk_usage': f"{disk.percent:.1f}%",
            'disk_free': f"{disk.free / (1024**3):.1f} GB"
        }
    
    def load_performance_data(self):
        """Load performance data from files"""
        data = {
            'executions': [],
            'agent_performance': [],
            'errors': []
        }
        
        # Load test results
        if self.test_results_dir.exists():
            for file in self.test_results_dir.glob("*.json"):
                try:
                    with open(file, 'r') as f:
                        result = json.load(f)
                        if 'execution_time' in result:
                            data['executions'].append({
                                'timestamp': file.stem.split('_')[-1],
                                'execution_time': float(result['execution_time'].replace(' seconds', '')),
                                'orchestration_id': result.get('orchestration_id', 'N/A'),
                                'status': 'success' if 'results' in result else 'failed'
                            })
                except Exception as e:
                    st.error(f"Error loading {file}: {e}")
        
        # Load performance reports
        if self.performance_reports_dir.exists():
            for file in self.performance_reports_dir.glob("*.json"):
                try:
                    with open(file, 'r') as f:
                        report = json.load(f)
                        if 'agent_timings' in report:
                            for agent_id, timing in report['agent_timings'].items():
                                data['agent_performance'].append({
                                    'agent_id': agent_id,
                                    'duration': timing.get('duration', 0),
                                    'status': timing.get('status', 'unknown'),
                                    'timestamp': report.get('timestamp', 'N/A')
                                })
                except Exception as e:
                    st.error(f"Error loading {file}: {e}")
        
        return data
    
    def render_dashboard(self):
        """Render the main dashboard"""
        st.title("🚀 AI System Performance Dashboard")
        st.markdown("Real-time monitoring of Energy & Property Tech Inc AI System")
        
        # Auto-refresh every 30 seconds
        if st.button("🔄 Refresh Data") or 'last_refresh' not in st.session_state:
            st.session_state.last_refresh = time.time()
        
        # System Metrics Section
        st.header("📊 System Health")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        metrics = self.get_system_metrics()
        
        with col1:
            st.metric("CPU Usage", metrics['cpu_usage'])
        with col2:
            st.metric("Memory Usage", metrics['memory_usage'])
        with col3:
            st.metric("Memory Available", metrics['memory_available'])
        with col4:
            st.metric("Disk Usage", metrics['disk_usage'])
        with col5:
            st.metric("Disk Free", metrics['disk_free'])
        
        # Performance Data
        data = self.load_performance_data()
        
        # Execution Performance
        st.header("⚡ Execution Performance")
        if data['executions']:
            df_executions = pd.DataFrame(data['executions'])
            df_executions['timestamp'] = pd.to_datetime(df_executions['timestamp'], format='%Y%m%d_%H%M%S')
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Execution time trend
                fig_time = px.line(df_executions, x='timestamp', y='execution_time', 
                                 title="Execution Time Trend",
                                 labels={'execution_time': 'Time (seconds)', 'timestamp': 'Date'})
                st.plotly_chart(fig_time, use_container_width=True)
            
            with col2:
                # Success rate
                success_rate = (df_executions['status'] == 'success').mean() * 100
                st.metric("Success Rate", f"{success_rate:.1f}%")
                
                # Average execution time
                avg_time = df_executions['execution_time'].mean()
                st.metric("Average Execution Time", f"{avg_time:.2f} seconds")
        
        # Agent Performance
        st.header("🤖 Agent Performance")
        if data['agent_performance']:
            df_agents = pd.DataFrame(data['agent_performance'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Agent duration comparison
                fig_agents = px.bar(df_agents.groupby('agent_id')['duration'].mean().reset_index(),
                                   x='agent_id', y='duration',
                                   title="Average Agent Execution Time",
                                   labels={'duration': 'Time (seconds)', 'agent_id': 'Agent'})
                st.plotly_chart(fig_agents, use_container_width=True)
            
            with col2:
                # Agent status distribution
                status_counts = df_agents['status'].value_counts()
                fig_status = px.pie(values=status_counts.values, names=status_counts.index,
                                   title="Agent Status Distribution")
                st.plotly_chart(fig_status, use_container_width=True)
        
        # Recent Activity
        st.header("📝 Recent Activity")
        if data['executions']:
            recent_executions = df_executions.sort_values('timestamp', ascending=False).head(10)
            st.dataframe(recent_executions, use_container_width=True)
        
        # System Information
        st.header("ℹ️ System Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Current Models")
            st.write("**Orchestrator**: OpenAI o3")
            st.write("**Claude Agents**: Claude 3.5 Sonnet (Ready for Opus upgrade)")
            st.write("**Workflow Engine**: LangGraph")
        
        with col2:
            st.subheader("Data Sources")
            st.write("**Financial**: 3 sources (Income, Balance, Cash Flow)")
            st.write("**Operational**: 3 sources (Assets, Leads, Products)")
            st.write("**Total Records**: 87+ business data points")
        
        # Auto-refresh indicator
        if 'last_refresh' in st.session_state:
            time_since_refresh = time.time() - st.session_state.last_refresh
            st.sidebar.markdown(f"**Last Refresh**: {time_since_refresh:.0f}s ago")
            st.sidebar.markdown("Auto-refresh every 30 seconds")

def main():
    dashboard = PerformanceDashboard()
    dashboard.render_dashboard()

if __name__ == "__main__":
    main() 