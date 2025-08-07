#!/usr/bin/env python3
"""
Main Integration v2.0 - Phase 4 Complete System
===============================================

Complete integration of all Phase 4 components with enhanced workflow execution,
real-time monitoring, performance optimization, and comprehensive testing.

Features:
- Enhanced LangGraph workflow with advanced state management
- Real-time agent monitoring and performance tracking
- Performance optimization with caching and parallel execution
- Comprehensive error handling and recovery
- Integration testing framework
- Production-ready logging and monitoring
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional

# Import all Phase 4 components
from fast_mcp_connectors import FastMCPClient
from o3_orchestrator import O3Orchestrator
from langgraph_workflow_v2 import EnhancedWorkflowEngine
from agent_monitor import AgentMonitor
from performance_optimizer import PerformanceOptimizer
from integration_tester import IntegrationTester

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/energy_property_ai.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EnergyPropertyAISystemV2:
    """Complete Phase 4 AI system with all advanced features"""
    
    def __init__(self):
        self.fast_mcp_client = None
        self.orchestrator = None
        self.workflow_engine = None
        self.agent_monitor = AgentMonitor()
        self.performance_optimizer = PerformanceOptimizer()
        self.integration_tester = IntegrationTester()
        self.system_initialized = False
        
        # Create necessary directories
        self._create_directories()
        
        logger.info("🚀 Energy Property AI System v2.0 initialized")
    
    def _create_directories(self):
        """Create necessary directories for the system"""
        directories = [
            'logs',
            'orchestrations',
            'test_reports',
            'performance_reports',
            'cache'
        ]
        
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)
    
    async def initialize_system(self) -> bool:
        """Initialize all system components"""
        logger.info("🔧 Initializing Phase 4 system components...")
        
        try:
            # Initialize Fast MCP Client
            logger.info("📊 Initializing Fast MCP Client...")
            self.fast_mcp_client = FastMCPClient()
            await self.fast_mcp_client.initialize()
            logger.info("✅ Fast MCP Client initialized")
            
            # Initialize o3 Orchestrator
            logger.info("🤖 Initializing o3 Orchestrator...")
            self.orchestrator = O3Orchestrator(self.fast_mcp_client)
            logger.info("✅ o3 Orchestrator initialized")
            
            # Initialize Enhanced Workflow Engine
            logger.info("🔄 Initializing Enhanced Workflow Engine...")
            self.workflow_engine = EnhancedWorkflowEngine(self.fast_mcp_client)
            logger.info("✅ Enhanced Workflow Engine initialized")
            
            # Configure performance optimization
            logger.info("⚡ Configuring performance optimization...")
            self._configure_performance_optimization()
            logger.info("✅ Performance optimization configured")
            
            # Initialize integration tester
            logger.info("🧪 Initializing integration tester...")
            await self.integration_tester.initialize_system()
            logger.info("✅ Integration tester initialized")
            
            self.system_initialized = True
            logger.info("🎉 Phase 4 system initialization completed successfully!")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ System initialization failed: {e}")
            return False
    
    def _configure_performance_optimization(self):
        """Configure performance optimization settings"""
        # Enable parallel execution for compatible agents
        parallel_agents = [
            'operations_summary_agent',
            'financial_impact_agent'
        ]
        self.performance_optimizer.enable_parallel_execution(parallel_agents)
        
        # Configure cache settings
        from performance_optimizer import CacheStrategy, ExecutionMode
        self.performance_optimizer.cache_strategy = CacheStrategy.LRU
        self.performance_optimizer.execution_mode = ExecutionMode.HYBRID
        
        logger.info(f"⚡ Performance optimization configured for {len(parallel_agents)} parallel agents")
    
    async def process_user_query(self, user_query: str) -> Dict[str, Any]:
        """Process user query with full Phase 4 capabilities"""
        if not self.system_initialized:
            logger.error("❌ System not initialized. Please call initialize_system() first.")
            return {"error": "System not initialized"}
        
        logger.info(f"🎯 Processing user query: {user_query[:100]}...")
        
        start_time = time.time()
        
        try:
            # Step 1: Generate orchestration specification with optimization
            logger.info("🤖 Step 1: Generating AI-powered orchestration...")
            orchestration_spec = await self.orchestrator.generate_orchestration_spec(user_query)
            
            if not orchestration_spec:
                raise ValueError("Failed to generate orchestration specification")
            
            # Step 2: Optimize workflow order
            logger.info("🔧 Step 2: Optimizing workflow execution order...")
            optimized_spec = self.performance_optimizer.optimize_workflow_order(orchestration_spec)
            
            # Step 3: Save orchestration specification
            orchestration_id = optimized_spec.get('orchestration_id', 'phase4_query')
            orchestration_file = f"orchestrations/phase4_orchestration_{orchestration_id}.json"
            
            with open(orchestration_file, 'w') as f:
                json.dump(optimized_spec, f, indent=2)
            
            logger.info(f"💾 Saved optimized orchestration to: {orchestration_file}")
            
            # Step 4: Execute enhanced workflow
            logger.info("🔄 Step 3: Executing enhanced workflow with monitoring...")
            result = await self.workflow_engine.execute_orchestration(orchestration_file)
            
            # Step 5: Get comprehensive metrics
            logger.info("📊 Step 4: Collecting performance metrics...")
            performance_metrics = self.agent_monitor.get_performance_report()
            optimization_metrics = self.performance_optimizer.get_performance_metrics()
            
            # Step 6: Generate comprehensive response
            execution_time = time.time() - start_time
            
            comprehensive_result = {
                "query": user_query,
                "orchestration_id": orchestration_id,
                "execution_time": execution_time,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "system_version": "Phase 4 v2.0",
                "workflow_result": result,
                "performance_metrics": performance_metrics,
                "optimization_metrics": optimization_metrics,
                "system_status": "completed"
            }
            
            logger.info(f"✅ Query processing completed in {execution_time:.2f}s")
            
            return comprehensive_result
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"❌ Query processing failed: {e}")
            
            # Log error with monitoring
            self.agent_monitor.log_error("main_system", e, {"query": user_query})
            
            return {
                "error": str(e),
                "execution_time": execution_time,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "system_status": "error"
            }
    
    async def run_comprehensive_testing(self) -> Dict[str, Any]:
        """Run comprehensive testing suite"""
        logger.info("🧪 Starting comprehensive testing suite...")
        
        try:
            test_report = await self.integration_tester.run_comprehensive_test_suite()
            
            # Save test report
            report_file = f"test_reports/phase4_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w') as f:
                json.dump(test_report, f, indent=2)
            
            logger.info(f"✅ Comprehensive testing completed. Report saved to: {report_file}")
            
            return {
                "status": "completed",
                "report_file": report_file,
                "test_report": test_report
            }
            
        except Exception as e:
            logger.error(f"❌ Comprehensive testing failed: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        if not self.system_initialized:
            return {"status": "not_initialized"}
        
        try:
            # Get monitoring metrics
            monitoring_status = self.agent_monitor.get_performance_report()
            
            # Get optimization metrics
            optimization_status = self.performance_optimizer.get_performance_metrics()
            
            # Get system health
            system_health = {
                "fast_mcp_client": self.fast_mcp_client is not None,
                "orchestrator": self.orchestrator is not None,
                "workflow_engine": self.workflow_engine is not None,
                "agent_monitor": True,
                "performance_optimizer": True
            }
            
            return {
                "status": "healthy" if all(system_health.values()) else "degraded",
                "system_health": system_health,
                "monitoring_metrics": monitoring_status,
                "optimization_metrics": optimization_status,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting system status: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def run_performance_benchmark(self, queries: list = None) -> Dict[str, Any]:
        """Run performance benchmarking"""
        logger.info("📊 Starting performance benchmarking...")
        
        if queries is None:
            queries = [
                "Analyze EMEA opportunities for pipeline uplift",
                "Provide financial performance analysis for Q2 2025",
                "Generate operations summary and asset status",
                "Create comprehensive business analysis with multiple agents"
            ]
        
        benchmark_results = []
        
        for i, query in enumerate(queries):
            logger.info(f"🔍 Benchmarking query {i+1}/{len(queries)}: {query[:50]}...")
            
            start_time = time.time()
            result = await self.process_user_query(query)
            execution_time = time.time() - start_time
            
            benchmark_results.append({
                "query": query,
                "execution_time": execution_time,
                "status": "success" if "error" not in result else "failed",
                "result_size": len(str(result))
            })
        
        # Calculate benchmark statistics
        successful_results = [r for r in benchmark_results if r["status"] == "success"]
        execution_times = [r["execution_time"] for r in successful_results]
        
        benchmark_summary = {
            "total_queries": len(queries),
            "successful_queries": len(successful_results),
            "success_rate": (len(successful_results) / len(queries)) * 100,
            "average_execution_time": sum(execution_times) / len(execution_times) if execution_times else 0,
            "min_execution_time": min(execution_times) if execution_times else 0,
            "max_execution_time": max(execution_times) if execution_times else 0,
            "detailed_results": benchmark_results
        }
        
        # Save benchmark report
        benchmark_file = f"performance_reports/benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(benchmark_file, 'w') as f:
            json.dump(benchmark_summary, f, indent=2)
        
        logger.info(f"✅ Performance benchmarking completed. Report saved to: {benchmark_file}")
        
        return benchmark_summary

# Demo runner for Phase 4
async def run_phase4_demo():
    """Run comprehensive Phase 4 demo"""
    print("🚀 Energy & Property Tech Inc. - Phase 4 Demo")
    print("=" * 60)
    
    # Initialize system
    system = EnergyPropertyAISystemV2()
    
    print("🔧 Initializing Phase 4 system...")
    if not await system.initialize_system():
        print("❌ System initialization failed!")
        return
    
    print("✅ Phase 4 system initialized successfully!")
    
    # Get system status
    print("\n📊 System Status:")
    status = system.get_system_status()
    print(f"Status: {status['status']}")
    print(f"System Health: {status['system_health']}")
    
    # Run comprehensive testing
    print("\n🧪 Running comprehensive testing...")
    test_result = await system.run_comprehensive_testing()
    if test_result['status'] == 'completed':
        summary = test_result['test_report']['summary']
        print(f"✅ Testing completed: {summary['passed_tests']}/{summary['total_tests']} passed ({summary['success_rate']:.1f}%)")
    
    # Process demo query
    print("\n🎯 Processing demo query...")
    demo_query = "I need to know which opportunities I should focus on in EMEA. Which assets would be ideal to push? I need to uplift pipeline for about +25%. Can you help me make a plan for this and identify which accounts to focus on?"
    
    result = await system.process_user_query(demo_query)
    
    if "error" not in result:
        print("✅ Demo query processed successfully!")
        print(f"📊 Execution time: {result['execution_time']:.2f}s")
        print(f"🤖 Orchestration ID: {result['orchestration_id']}")
        
        # Show performance metrics
        if 'performance_metrics' in result:
            metrics = result['performance_metrics']
            if 'overall_metrics' in metrics:
                overall = metrics['overall_metrics']
                print(f"📈 Success rate: {overall.get('success_rate', 0):.1f}%")
                print(f"⏱️ Average execution time: {overall.get('average_execution_time', 0):.2f}s")
    else:
        print(f"❌ Demo query failed: {result['error']}")
    
    # Run performance benchmark
    print("\n📊 Running performance benchmark...")
    benchmark_result = await system.run_performance_benchmark()
    print(f"✅ Benchmark completed: {benchmark_result['successful_queries']}/{benchmark_result['total_queries']} successful")
    print(f"📈 Average execution time: {benchmark_result['average_execution_time']:.2f}s")
    
    print("\n🎉 Phase 4 Demo Completed Successfully!")
    print("=" * 60)

# Main execution
if __name__ == "__main__":
    asyncio.run(run_phase4_demo()) 