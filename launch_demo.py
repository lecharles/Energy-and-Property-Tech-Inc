#!/usr/bin/env python3
"""
Demo Launch Script for Energy & Property Tech Inc AI System
Easy access to Performance Dashboard and Demo Launcher
"""

import subprocess
import sys
import os
from pathlib import Path

def print_banner():
    """Print the system banner"""
    print("=" * 80)
    print("🚀 ENERGY & PROPERTY TECH INC - AI SYSTEM DEMO LAUNCHER")
    print("=" * 80)
    print("Phase 5: Demo-Ready Production System")
    print("✅ Step 1: Model Optimization - COMPLETED")
    print("✅ Step 2: Performance Dashboard - COMPLETED")
    print("⏳ Step 3: Security & Caching - IN PROGRESS")
    print("⏳ Step 4: Concurrent Users - PENDING")
    print("=" * 80)

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import streamlit
        import plotly
        import psutil
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please run: pip install streamlit plotly psutil")
        return False

def launch_dashboard():
    """Launch the performance dashboard"""
    print("\n📊 Launching Performance Dashboard...")
    print("Dashboard will open in your browser at: http://localhost:8501")
    print("Press Ctrl+C to stop the dashboard")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "performance_dashboard.py",
            "--server.port", "8501",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")

def launch_demo_interface():
    """Launch the demo launcher interface"""
    print("\n🎯 Launching Demo Interface...")
    print("Demo interface will open in your browser at: http://localhost:8502")
    print("Press Ctrl+C to stop the demo interface")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "demo_launcher.py",
            "--server.port", "8502",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Demo interface stopped by user")
    except Exception as e:
        print(f"❌ Error launching demo interface: {e}")

def show_system_status():
    """Show current system status"""
    print("\n📋 System Status:")
    
    # Check if test results exist
    test_results = Path("test_results")
    if test_results.exists():
        result_files = list(test_results.glob("*.json"))
        print(f"   📁 Test Results: {len(result_files)} files available")
    
    # Check if orchestrations exist
    orchestrations = Path("orchestrations")
    if orchestrations.exists():
        orchestration_files = list(orchestrations.glob("*.json"))
        print(f"   🔄 Orchestrations: {len(orchestration_files)} files available")
    
    # Check if performance reports exist
    performance_reports = Path("performance_reports")
    if performance_reports.exists():
        report_files = list(performance_reports.glob("*.json"))
        print(f"   📊 Performance Reports: {len(report_files)} files available")
    
    print(f"   🤖 AI Models: OpenAI o3 + Claude 3.5 Sonnet")
    print(f"   🔧 Workflow Engine: LangGraph")
    print(f"   📊 Data Sources: 6 business data sources")

def main():
    """Main launch function"""
    print_banner()
    
    if not check_dependencies():
        return
    
    show_system_status()
    
    while True:
        print("\n🎯 Choose an option:")
        print("1. 📊 Launch Performance Dashboard")
        print("2. 🎯 Launch Demo Interface")
        print("3. 📋 Show System Status")
        print("4. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            launch_dashboard()
        elif choice == "2":
            launch_demo_interface()
        elif choice == "3":
            show_system_status()
        elif choice == "4":
            print("\n👋 Thank you for using the AI System Demo!")
            print("For more information, check the plans/ directory")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main() 