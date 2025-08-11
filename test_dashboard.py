#!/usr/bin/env python3
"""
Test script for Performance Dashboard functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_dashboard_components():
    """Test dashboard components without Streamlit"""
    try:
        from performance_dashboard import PerformanceDashboard
        print("✅ Performance Dashboard class imported successfully")
        
        # Test dashboard initialization
        dashboard = PerformanceDashboard()
        print("✅ Dashboard instance created successfully")
        
        # Test system metrics
        metrics = dashboard.get_system_metrics()
        print("✅ System metrics retrieved successfully")
        print(f"   CPU: {metrics['cpu_usage']}")
        print(f"   Memory: {metrics['memory_usage']}")
        print(f"   Disk: {metrics['disk_usage']}")
        
        # Test data loading
        data = dashboard.load_performance_data()
        print("✅ Performance data loaded successfully")
        print(f"   Executions: {len(data['executions'])}")
        print(f"   Agent Performance: {len(data['agent_performance'])}")
        
        print("\n🎉 All dashboard components working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing dashboard: {e}")
        return False

def test_demo_launcher():
    """Test demo launcher components without Streamlit"""
    try:
        from demo_launcher import DemoLauncher
        print("✅ Demo Launcher class imported successfully")
        
        # Test launcher initialization
        launcher = DemoLauncher()
        print("✅ Demo Launcher instance created successfully")
        
        # Test demo queries
        print(f"✅ Demo queries loaded: {len(launcher.demo_queries)}")
        for name, info in launcher.demo_queries.items():
            print(f"   - {name}: {info['description']}")
        
        print("\n🎉 All demo launcher components working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing demo launcher: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Dashboard Components")
    print("=" * 50)
    
    dashboard_ok = test_dashboard_components()
    print("\n" + "=" * 50)
    
    print("🧪 Testing Demo Launcher Components")
    print("=" * 50)
    
    launcher_ok = test_demo_launcher()
    print("\n" + "=" * 50)
    
    if dashboard_ok and launcher_ok:
        print("🎉 ALL TESTS PASSED! Dashboard and Demo Launcher ready for use.")
        print("\n📱 To launch the dashboard:")
        print("   streamlit run performance_dashboard.py")
        print("\n🎯 To launch the demo interface:")
        print("   streamlit run demo_launcher.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 