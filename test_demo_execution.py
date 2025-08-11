#!/usr/bin/env python3
"""
Test Demo Execution - Verify Main Integration System
===================================================

This script tests the main integration system to ensure it can:
1. Initialize properly
2. Process user queries
3. Show real-time execution flow
4. Generate results

Run this to verify everything is working before using the demo launcher.
"""

import asyncio
import json
import time
from pathlib import Path
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_system_initialization():
    """Test if the system can initialize properly"""
    print("🔧 Testing system initialization...")
    
    try:
        from main_integration_v2 import EnergyPropertyAISystemV2
        print("✅ Successfully imported main integration system")
        
        system = EnergyPropertyAISystemV2()
        print("✅ Successfully created system instance")
        
        initialized = await system.initialize_system()
        if initialized:
            print("✅ System initialization successful!")
            return system
        else:
            print("❌ System initialization failed!")
            return None
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return None
    except Exception as e:
        print(f"❌ System initialization error: {e}")
        return None

async def test_query_execution(system):
    """Test if the system can process a simple query"""
    print("\n🎯 Testing query execution...")
    
    test_query = "What's the best region to make the highest margins and to launch the quickest campaigns with the shortest return time and with the highest impact?"
    
    print(f"📝 Test query: {test_query[:80]}...")
    
    try:
        start_time = time.time()
        result = await system.process_user_query(test_query)
        execution_time = time.time() - start_time
        
        print(f"✅ Query execution completed in {execution_time:.2f} seconds")
        
        if "error" in result:
            print(f"❌ Query execution failed: {result['error']}")
            return False
        
        # Show key results
        print(f"📊 Orchestration ID: {result.get('orchestration_id', 'N/A')}")
        print(f"⏱️ Execution time: {result.get('execution_time', 'N/A')}")
        print(f"🤖 System version: {result.get('system_version', 'N/A')}")
        
        # Check if workflow result exists
        if 'workflow_result' in result:
            print("✅ Workflow execution successful")
        else:
            print("⚠️ No workflow result found")
        
        # Check performance metrics
        if 'performance_metrics' in result:
            print("✅ Performance metrics collected")
        else:
            print("⚠️ No performance metrics found")
        
        return True
        
    except Exception as e:
        print(f"❌ Query execution error: {e}")
        return False

async def test_system_status(system):
    """Test if the system can provide status information"""
    print("\n📊 Testing system status...")
    
    try:
        status = system.get_system_status()
        print(f"✅ System status retrieved: {status.get('status', 'N/A')}")
        print(f"🏥 System health: {status.get('system_health', 'N/A')}")
        
        if 'components' in status:
            components = status['components']
            print(f"🔧 Components status:")
            for component, comp_status in components.items():
                print(f"  - {component}: {comp_status}")
        
        return True
        
    except Exception as e:
        print(f"❌ System status error: {e}")
        return False

async def test_performance_benchmark(system):
    """Test if the system can run performance benchmarks"""
    print("\n📈 Testing performance benchmark...")
    
    try:
        # Simple test queries
        test_queries = [
            "Which region has the highest gross margin?",
            "What are our top 3 revenue products?",
            "Show me our lead funnel performance"
        ]
        
        print(f"🧪 Running benchmark with {len(test_queries)} test queries...")
        
        benchmark_result = await system.run_performance_benchmark(test_queries)
        
        if benchmark_result['status'] == 'completed':
            print("✅ Performance benchmark completed successfully!")
            print(f"📊 Success rate: {benchmark_result['success_rate']:.1f}%")
            print(f"⏱️ Average execution time: {benchmark_result['average_execution_time']:.2f}s")
        else:
            print(f"⚠️ Performance benchmark status: {benchmark_result['status']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance benchmark error: {e}")
        return False

async def main():
    """Main test function"""
    print("🚀 Energy & Property Tech Inc - Demo Execution Test")
    print("=" * 60)
    
    # Test 1: System initialization
    system = await test_system_initialization()
    if not system:
        print("\n❌ System initialization failed. Cannot proceed with tests.")
        return
    
    # Test 2: System status
    await test_system_status(system)
    
    # Test 3: Query execution
    query_success = await test_query_execution(system)
    
    # Test 4: Performance benchmark (only if query execution succeeded)
    if query_success:
        await test_performance_benchmark(system)
    
    print("\n" + "=" * 60)
    if query_success:
        print("🎉 Demo execution test completed successfully!")
        print("✅ Your system is ready for demo execution")
        print("\n📱 Next steps:")
        print("1. Run the demo launcher: streamlit run demo_launcher.py")
        print("2. Select a demo query and click 'Execute AI Analysis'")
        print("3. Watch the real-time execution in the tabs")
    else:
        print("❌ Demo execution test failed!")
        print("🔧 Please check your system configuration and try again")
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main()) 