#!/usr/bin/env python3
"""
Comprehensive Test Script for Energy Property AI System
======================================================

This script tests the core system functionality with a specific business query
to verify that the orchestration, agents, and monitoring are working properly.

Test Query: Comprehensive business analysis for most profitable region
"""

import asyncio
import json
import time
from pathlib import Path
from main_integration_v2 import EnergyPropertyAISystemV2

async def comprehensive_test():
    """Run comprehensive test of the AI system"""
    
    print("🚀 Energy Property AI System - Comprehensive Test")
    print("=" * 80)
    
    # Initialize system
    print("\n🔧 Initializing system...")
    system = EnergyPropertyAISystemV2()
    await system.initialize_system()
    print("✅ System initialized successfully")
    
    # Define the comprehensive business query
    query = """I need to know:
- What is the most profitable region
- Why do we believe that is the case
- Which upsell opportunity is it the one that we are going to exploit there
- What is the potential growth for that region
- What is the potential business impact that we will get
- Which products do we have to sell over there
- If you can help me prepare a campaign and for which channel we can do it in detail and explain why that would be great"""
    
    print(f"\n📝 Testing Query:")
    print("-" * 50)
    print(query)
    print("-" * 50)
    
    # Execute query
    print("\n🎯 Executing query...")
    start_time = time.time()
    
    try:
        result = await system.process_user_query(query)
        execution_time = time.time() - start_time
        
        print(f"\n✅ Query completed in {execution_time:.2f} seconds")
        
        # Display result summary
        print("\n📊 Result Summary:")
        print(f"Status: {result.get('status', 'Unknown')}")
        print(f"Execution Time: {execution_time:.2f} seconds")
        
        if 'orchestration_id' in result:
            orchestration_id = result['orchestration_id']
            print(f"Orchestration ID: {orchestration_id}")
            
            # Check generated files
            print("\n📁 Generated Files:")
            
            # Check orchestration file
            orchestration_file = Path(f"orchestrations/phase4_orchestration_{orchestration_id}.json")
            if orchestration_file.exists():
                print(f"✅ Orchestration: {orchestration_file}")
                
                # Read and display orchestration details
                with open(orchestration_file, 'r') as f:
                    orchestration_data = json.load(f)
                
                print(f"\n🔍 Orchestration Details:")
                print(f"  - Agents: {len(orchestration_data.get('workflow', {}).get('agents', []))}")
                print(f"  - AI Generated: {orchestration_data.get('ai_generated', False)}")
                print(f"  - Valid: {orchestration_data.get('validation', {}).get('is_valid', False)}")
                
                if orchestration_data.get('validation', {}).get('issues'):
                    print(f"  - Issues: {len(orchestration_data['validation']['issues'])}")
                    for issue in orchestration_data['validation']['issues'][:3]:  # Show first 3
                        print(f"    • {issue[:80]}...")
            else:
                print(f"❌ Orchestration file not found: {orchestration_file}")
            
            # Check performance reports
            performance_dir = Path("performance_reports")
            if performance_dir.exists():
                latest_report = max(performance_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, default=None)
                if latest_report:
                    print(f"✅ Performance Report: {latest_report}")
                    
                    # Read and display performance summary
                    with open(latest_report, 'r') as f:
                        perf_data = json.load(f)
                    
                    print(f"\n📈 Performance Summary:")
                    print(f"  - Total Queries: {perf_data.get('total_queries', 0)}")
                    print(f"  - Success Rate: {perf_data.get('success_rate', 0)}%")
                    print(f"  - Avg Execution Time: {perf_data.get('average_execution_time', 0):.2f}s")
            
            # Check logs
            log_file = Path("logs/energy_property_ai.log")
            if log_file.exists() and log_file.stat().st_size > 0:
                print(f"✅ Log File: {log_file}")
                
                # Show last few log lines
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        print(f"\n📋 Recent Log Entries:")
                        for line in lines[-5:]:  # Last 5 lines
                            print(f"  {line.strip()}")
            else:
                print(f"⚠️  Log File: {log_file} (empty or not found)")
            
            # Check cache
            cache_dir = Path("cache")
            if cache_dir.exists():
                cache_files = list(cache_dir.glob("*"))
                if cache_files:
                    print(f"\n💾 Cache Files: {len(cache_files)}")
                    for cache_file in cache_files[:3]:  # Show first 3
                        print(f"  - {cache_file.name}")
                else:
                    print(f"\n💾 Cache: Empty")
            
            # Check test results
            test_results_dir = Path("test_results")
            if test_results_dir.exists():
                result_files = list(test_results_dir.glob("*.json"))
                if result_files:
                    print(f"\n🧪 Test Results: {len(result_files)} files")
                    
                    # Find the most recent comprehensive result
                    comprehensive_results = [f for f in result_files if "comprehensive" in f.name]
                    if comprehensive_results:
                        latest_comprehensive = max(comprehensive_results, key=lambda x: x.stat().st_mtime)
                        print(f"  - Latest Comprehensive: {latest_comprehensive.name}")
                        
                        # Show result summary
                        with open(latest_comprehensive, 'r') as f:
                            comp_data = json.load(f)
                        
                        print(f"    • Query: {comp_data.get('query', 'Unknown')[:100]}...")
                        print(f"    • Execution Time: {comp_data.get('execution_time', 'Unknown')}")
                        print(f"    • System Version: {comp_data.get('system_version', 'Unknown')}")
            
            print(f"\n🎉 Test completed successfully!")
            print(f"\n📋 Next Steps:")
            print(f"1. Review orchestration file: {orchestration_file}")
            print(f"2. Check performance reports in: performance_reports/")
            print(f"3. Review logs in: logs/")
            print(f"4. Examine test results in: test_results/")
            
        else:
            print("❌ No orchestration ID found in result")
            print(f"Full result: {json.dumps(result, indent=2)}")
            
    except Exception as e:
        print(f"\n❌ Error during query execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(comprehensive_test())
