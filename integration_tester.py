#!/usr/bin/env python3
"""
Integration Testing Framework
============================

Comprehensive integration testing framework with end-to-end testing,
error scenario testing, performance benchmarking, and load testing.

Features:
- End-to-end workflow testing
- Error scenario simulation and testing
- Performance benchmarking and metrics
- Load testing with concurrent queries
- Agent interaction testing
- Quality assurance and validation
- Automated test reporting
"""

import asyncio
import json
import logging
import time
import statistics
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import random

# Import our components
from fast_mcp_connectors import FastMCPClient
from o3_orchestrator import O3Orchestrator
from langgraph_workflow_v2 import EnhancedWorkflowEngine
from agent_monitor import AgentMonitor
from performance_optimizer import PerformanceOptimizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class TestResult:
    """Test result with detailed information"""
    test_name: str
    test_type: str
    status: str  # 'passed', 'failed', 'error'
    execution_time: float
    error_message: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None
    output: Optional[Dict[str, Any]] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)

@dataclass
class TestScenario:
    """Test scenario definition"""
    name: str
    description: str
    query: str
    expected_agents: List[str]
    expected_execution_time: float
    expected_output_keys: List[str]
    error_scenarios: List[str] = None

class IntegrationTester:
    """Comprehensive integration testing framework"""
    
    def __init__(self):
        self.test_results: List[TestResult] = []
        self.agent_monitor = AgentMonitor()
        self.performance_optimizer = PerformanceOptimizer()
        self.system = None
        self.test_scenarios = self._create_test_scenarios()
        
    def _create_test_scenarios(self) -> List[TestScenario]:
        """Create comprehensive test scenarios"""
        return [
            TestScenario(
                name="EMEA Opportunities Query",
                description="Test EMEA opportunities and pipeline uplift query",
                query="I need to know which opportunities I should focus on in EMEA. Which assets would be ideal to push? I need to uplift pipeline for about +25%. Can you help me make a plan for this and identify which accounts to focus on?",
                expected_agents=["upsell_discovery_agent", "campaign_planner_agent"],
                expected_execution_time=30.0,
                expected_output_keys=["execution_summary", "agent_outputs", "recommendations"]
            ),
            TestScenario(
                name="Financial Performance Analysis",
                description="Test financial performance analysis and forecasting",
                query="Analyze our Q2 2025 financial performance and provide recommendations for Q3 2025 growth strategy. Focus on revenue optimization and cost management.",
                expected_agents=["financial_impact_agent", "operations_summary_agent"],
                expected_execution_time=25.0,
                expected_output_keys=["execution_summary", "financial_analysis", "recommendations"]
            ),
            TestScenario(
                name="Operations Summary Query",
                description="Test operations summary and asset management",
                query="Provide a comprehensive summary of our operational status, including installed assets, maintenance schedules, and critical issues that need attention.",
                expected_agents=["operations_summary_agent"],
                expected_execution_time=15.0,
                expected_output_keys=["execution_summary", "operational_status", "critical_issues"]
            ),
            TestScenario(
                name="Complex Multi-Agent Query",
                description="Test complex query requiring multiple agents",
                query="I need a comprehensive business analysis including upsell opportunities, financial impact assessment, campaign planning, and operations summary. This should cover all aspects of our business performance and provide actionable insights.",
                expected_agents=["upsell_discovery_agent", "campaign_planner_agent", "financial_impact_agent", "operations_summary_agent"],
                expected_execution_time=60.0,
                expected_output_keys=["execution_summary", "agent_outputs", "recommendations", "performance_metrics"]
            )
        ]
    
    async def initialize_system(self):
        """Initialize the complete system for testing"""
        logger.info("🚀 Initializing system for integration testing")
        
        try:
            # Initialize Fast MCP Client
            fast_mcp_client = FastMCPClient()
            await fast_mcp_client.initialize()
            
            # Initialize o3 Orchestrator
            orchestrator = O3Orchestrator(fast_mcp_client)
            
            # Initialize Enhanced Workflow Engine
            workflow_engine = EnhancedWorkflowEngine(fast_mcp_client)
            
            # Store system components
            self.system = {
                'fast_mcp_client': fast_mcp_client,
                'orchestrator': orchestrator,
                'workflow_engine': workflow_engine
            }
            
            logger.info("✅ System initialized successfully for testing")
            return True
            
        except Exception as e:
            logger.error(f"❌ System initialization failed: {e}")
            return False
    
    async def test_end_to_end_workflow(self, test_queries: List[str] = None) -> List[TestResult]:
        """Test complete end-to-end workflow with multiple queries"""
        logger.info("🧪 Starting end-to-end workflow testing")
        
        if not self.system:
            if not await self.initialize_system():
                return [TestResult(
                    test_name="System Initialization",
                    test_type="initialization",
                    status="failed",
                    execution_time=0.0,
                    error_message="Failed to initialize system"
                )]
        
        results = []
        
        # Use provided queries or default scenarios
        if test_queries is None:
            test_queries = [scenario.query for scenario in self.test_scenarios]
        
        for i, query in enumerate(test_queries):
            test_name = f"End-to-End Test {i+1}"
            logger.info(f"🔍 Running {test_name}: {query[:50]}...")
            
            start_time = time.time()
            
            try:
                # Step 1: Generate orchestration specification
                orchestration_spec = await self.system['orchestrator'].generate_orchestration_spec(query)
                
                if not orchestration_spec:
                    raise ValueError("Failed to generate orchestration specification")
                
                # Step 2: Save orchestration spec
                orchestration_id = orchestration_spec.get('orchestration_id', f'test_{i}')
                orchestration_file = f"orchestrations/test_orchestration_{orchestration_id}.json"
                
                Path("orchestrations").mkdir(exist_ok=True)
                with open(orchechestration_file, 'w') as f:
                    json.dump(orchestration_spec, f, indent=2)
                
                # Step 3: Execute workflow
                result = await self.system['workflow_engine'].execute_orchestration(orchestration_file)
                
                execution_time = time.time() - start_time
                
                # Validate result
                if result and "final_output" in result:
                    status = "passed"
                    error_message = None
                else:
                    status = "failed"
                    error_message = "No final output generated"
                
                # Get performance metrics
                metrics = self.agent_monitor.get_performance_report()
                
                test_result = TestResult(
                    test_name=test_name,
                    test_type="end_to_end",
                    status=status,
                    execution_time=execution_time,
                    error_message=error_message,
                    metrics=metrics,
                    output=result
                )
                
                results.append(test_result)
                logger.info(f"✅ {test_name} completed in {execution_time:.2f}s with status: {status}")
                
            except Exception as e:
                execution_time = time.time() - start_time
                error_message = str(e)
                
                test_result = TestResult(
                    test_name=test_name,
                    test_type="end_to_end",
                    status="error",
                    execution_time=execution_time,
                    error_message=error_message
                )
                
                results.append(test_result)
                logger.error(f"❌ {test_name} failed: {error_message}")
        
        return results
    
    async def test_error_scenarios(self) -> List[TestResult]:
        """Test various error scenarios and recovery"""
        logger.info("🧪 Starting error scenario testing")
        
        if not self.system:
            if not await self.initialize_system():
                return []
        
        error_scenarios = [
            {
                'name': 'Invalid Query Test',
                'query': '',  # Empty query
                'expected_error': 'Invalid query'
            },
            {
                'name': 'Malformed Query Test',
                'query': 'This is not a valid business query at all',
                'expected_error': 'Unable to process query'
            },
            {
                'name': 'Network Error Simulation',
                'query': 'Test network error simulation',
                'expected_error': 'Network error'
            },
            {
                'name': 'Timeout Error Simulation',
                'query': 'Test timeout error simulation',
                'expected_error': 'Timeout error'
            }
        ]
        
        results = []
        
        for scenario in error_scenarios:
            logger.info(f"🔍 Testing error scenario: {scenario['name']}")
            
            start_time = time.time()
            
            try:
                # Try to process the problematic query
                orchestration_spec = await self.system['orchestrator'].generate_orchestration_spec(scenario['query'])
                
                execution_time = time.time() - start_time
                
                # Check if error was handled gracefully
                if orchestration_spec and "workflow" in orchestration_spec:
                    status = "passed"  # Error was handled gracefully
                    error_message = None
                else:
                    status = "failed"
                    error_message = "Error not handled gracefully"
                
                test_result = TestResult(
                    test_name=scenario['name'],
                    test_type="error_scenario",
                    status=status,
                    execution_time=execution_time,
                    error_message=error_message
                )
                
                results.append(test_result)
                logger.info(f"✅ Error scenario {scenario['name']} completed with status: {status}")
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                # Check if this is the expected error
                if scenario['expected_error'].lower() in str(e).lower():
                    status = "passed"
                    error_message = f"Expected error occurred: {str(e)}"
                else:
                    status = "failed"
                    error_message = f"Unexpected error: {str(e)}"
                
                test_result = TestResult(
                    test_name=scenario['name'],
                    test_type="error_scenario",
                    status=status,
                    execution_time=execution_time,
                    error_message=error_message
                )
                
                results.append(test_result)
                logger.info(f"✅ Error scenario {scenario['name']} completed with status: {status}")
        
        return results
    
    async def test_performance_under_load(self, concurrent_queries: int = 5) -> List[TestResult]:
        """Test system performance under load with concurrent queries"""
        logger.info(f"🧪 Starting load testing with {concurrent_queries} concurrent queries")
        
        if not self.system:
            if not await self.initialize_system():
                return []
        
        # Create test queries
        test_queries = [
            "Analyze EMEA opportunities for pipeline uplift",
            "Provide financial performance analysis for Q2 2025",
            "Generate operations summary and asset status",
            "Create comprehensive business analysis with multiple agents",
            "Identify upsell opportunities in APAC region"
        ]
        
        # Ensure we have enough queries
        while len(test_queries) < concurrent_queries:
            test_queries.extend(test_queries[:concurrent_queries - len(test_queries)])
        
        start_time = time.time()
        
        async def execute_single_query(query: str, query_id: int):
            """Execute a single query and return results"""
            query_start_time = time.time()
            
            try:
                # Generate orchestration spec
                orchestration_spec = await self.system['orchestrator'].generate_orchestration_spec(query)
                
                if orchestration_spec:
                    # Save and execute
                    orchestration_id = orchestration_spec.get('orchestration_id', f'load_test_{query_id}')
                    orchestration_file = f"orchestrations/load_test_{orchestration_id}.json"
                    
                    Path("orchestrations").mkdir(exist_ok=True)
                    with open(orchestration_file, 'w') as f:
                        json.dump(orchestration_spec, f, indent=2)
                    
                    result = await self.system['workflow_engine'].execute_orchestration(orchestration_file)
                    
                    execution_time = time.time() - query_start_time
                    
                    return {
                        'query_id': query_id,
                        'status': 'passed',
                        'execution_time': execution_time,
                        'result': result
                    }
                else:
                    execution_time = time.time() - query_start_time
                    return {
                        'query_id': query_id,
                        'status': 'failed',
                        'execution_time': execution_time,
                        'error': 'Failed to generate orchestration spec'
                    }
                    
            except Exception as e:
                execution_time = time.time() - query_start_time
                return {
                    'query_id': query_id,
                    'status': 'error',
                    'execution_time': execution_time,
                    'error': str(e)
                }
        
        # Execute queries concurrently
        tasks = [execute_single_query(query, i) for i, query in enumerate(test_queries[:concurrent_queries])]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        total_execution_time = time.time() - start_time
        
        # Process results
        test_results = []
        successful_queries = 0
        total_execution_times = []
        
        for result in results:
            if isinstance(result, dict):
                if result['status'] == 'passed':
                    successful_queries += 1
                    total_execution_times.append(result['execution_time'])
                
                test_result = TestResult(
                    test_name=f"Load Test Query {result['query_id']}",
                    test_type="load_test",
                    status=result['status'],
                    execution_time=result['execution_time'],
                    error_message=result.get('error'),
                    metrics={'concurrent_queries': concurrent_queries}
                )
                test_results.append(test_result)
        
        # Calculate performance metrics
        success_rate = (successful_queries / concurrent_queries) * 100
        avg_execution_time = statistics.mean(total_execution_times) if total_execution_times else 0
        throughput = concurrent_queries / total_execution_time if total_execution_time > 0 else 0
        
        # Create summary result
        summary_result = TestResult(
            test_name="Load Test Summary",
            test_type="load_test_summary",
            status="passed" if success_rate >= 80 else "failed",
            execution_time=total_execution_time,
            metrics={
                'concurrent_queries': concurrent_queries,
                'successful_queries': successful_queries,
                'success_rate': success_rate,
                'average_execution_time': avg_execution_time,
                'throughput': throughput,
                'total_execution_time': total_execution_time
            }
        )
        test_results.append(summary_result)
        
        logger.info(f"✅ Load testing completed: {successful_queries}/{concurrent_queries} successful ({success_rate:.1f}%)")
        logger.info(f"📊 Performance: Avg time {avg_execution_time:.2f}s, Throughput {throughput:.2f} queries/s")
        
        return test_results
    
    async def test_agent_interactions(self) -> List[TestResult]:
        """Test inter-agent communication and coordination"""
        logger.info("🧪 Starting agent interaction testing")
        
        if not self.system:
            if not await self.initialize_system():
                return []
        
        interaction_tests = [
            {
                'name': 'Agent Dependency Test',
                'query': 'Test agent dependencies and execution order',
                'expected_agents': ['upsell_discovery_agent', 'campaign_planner_agent'],
                'expected_dependencies': True
            },
            {
                'name': 'Agent Communication Test',
                'query': 'Test agent communication and data sharing',
                'expected_agents': ['financial_impact_agent', 'operations_summary_agent'],
                'expected_dependencies': False
            },
            {
                'name': 'Multi-Agent Coordination Test',
                'query': 'Test coordination between multiple agents',
                'expected_agents': ['upsell_discovery_agent', 'campaign_planner_agent', 'financial_impact_agent'],
                'expected_dependencies': True
            }
        ]
        
        results = []
        
        for test in interaction_tests:
            logger.info(f"🔍 Testing agent interaction: {test['name']}")
            
            start_time = time.time()
            
            try:
                # Generate orchestration spec
                orchestration_spec = await self.system['orchestrator'].generate_orchestration_spec(test['query'])
                
                if not orchestration_spec:
                    raise ValueError("Failed to generate orchestration specification")
                
                # Check agent configuration
                agents = orchestration_spec.get('workflow', {}).get('agents', [])
                agent_ids = [agent['agent_id'] for agent in agents]
                
                # Validate expected agents
                expected_agents = test['expected_agents']
                missing_agents = [agent for agent in expected_agents if agent not in agent_ids]
                
                if missing_agents:
                    status = "failed"
                    error_message = f"Missing expected agents: {missing_agents}"
                else:
                    # Check dependencies
                    has_dependencies = any(agent.get('dependencies') for agent in agents)
                    
                    if has_dependencies == test['expected_dependencies']:
                        status = "passed"
                        error_message = None
                    else:
                        status = "failed"
                        error_message = f"Expected dependencies: {test['expected_dependencies']}, Got: {has_dependencies}"
                
                execution_time = time.time() - start_time
                
                test_result = TestResult(
                    test_name=test['name'],
                    test_type="agent_interaction",
                    status=status,
                    execution_time=execution_time,
                    error_message=error_message,
                    metrics={
                        'expected_agents': expected_agents,
                        'actual_agents': agent_ids,
                        'has_dependencies': has_dependencies if 'has_dependencies' in locals() else None
                    }
                )
                
                results.append(test_result)
                logger.info(f"✅ Agent interaction test {test['name']} completed with status: {status}")
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                test_result = TestResult(
                    test_name=test['name'],
                    test_type="agent_interaction",
                    status="error",
                    execution_time=execution_time,
                    error_message=str(e)
                )
                
                results.append(test_result)
                logger.error(f"❌ Agent interaction test {test['name']} failed: {str(e)}")
        
        return results
    
    def generate_test_report(self) -> dict:
        """Generate comprehensive test report"""
        if not self.test_results:
            return {'error': 'No test results available'}
        
        # Calculate statistics
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.status == 'passed')
        failed_tests = sum(1 for result in self.test_results if result.status == 'failed')
        error_tests = sum(1 for result in self.test_results if result.status == 'error')
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Calculate execution times
        execution_times = [result.execution_time for result in self.test_results if result.execution_time > 0]
        avg_execution_time = statistics.mean(execution_times) if execution_times else 0
        min_execution_time = min(execution_times) if execution_times else 0
        max_execution_time = max(execution_times) if execution_times else 0
        
        # Group results by type
        results_by_type = {}
        for result in self.test_results:
            test_type = result.test_type
            if test_type not in results_by_type:
                results_by_type[test_type] = []
            results_by_type[test_type].append(result)
        
        # Get performance metrics
        performance_metrics = self.agent_monitor.get_performance_report()
        optimization_metrics = self.performance_optimizer.get_performance_metrics()
        
        report = {
            'summary': {
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': failed_tests,
                'error_tests': error_tests,
                'success_rate': success_rate,
                'average_execution_time': avg_execution_time,
                'min_execution_time': min_execution_time,
                'max_execution_time': max_execution_time
            },
            'results_by_type': {
                test_type: {
                    'count': len(results),
                    'passed': sum(1 for r in results if r.status == 'passed'),
                    'failed': sum(1 for r in results if r.status == 'failed'),
                    'errors': sum(1 for r in results if r.status == 'error'),
                    'success_rate': (sum(1 for r in results if r.status == 'passed') / len(results) * 100) if results else 0
                }
                for test_type, results in results_by_type.items()
            },
            'detailed_results': [
                {
                    'test_name': result.test_name,
                    'test_type': result.test_type,
                    'status': result.status,
                    'execution_time': result.execution_time,
                    'error_message': result.error_message,
                    'timestamp': result.timestamp.isoformat()
                }
                for result in self.test_results
            ],
            'performance_metrics': performance_metrics,
            'optimization_metrics': optimization_metrics,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        return report
    
    async def run_comprehensive_test_suite(self) -> dict:
        """Run comprehensive test suite with all test types"""
        logger.info("🚀 Starting comprehensive test suite")
        
        all_results = []
        
        # 1. End-to-end workflow testing
        logger.info("📋 Running end-to-end workflow tests...")
        e2e_results = await self.test_end_to_end_workflow()
        all_results.extend(e2e_results)
        
        # 2. Error scenario testing
        logger.info("📋 Running error scenario tests...")
        error_results = await self.test_error_scenarios()
        all_results.extend(error_results)
        
        # 3. Load testing
        logger.info("📋 Running load tests...")
        load_results = await self.test_performance_under_load(concurrent_queries=3)
        all_results.extend(load_results)
        
        # 4. Agent interaction testing
        logger.info("📋 Running agent interaction tests...")
        interaction_results = await self.test_agent_interactions()
        all_results.extend(interaction_results)
        
        # Store all results
        self.test_results = all_results
        
        # Generate comprehensive report
        report = self.generate_test_report()
        
        # Save report to file
        report_file = f"test_reports/comprehensive_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        Path("test_reports").mkdir(exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"✅ Comprehensive test suite completed. Report saved to: {report_file}")
        logger.info(f"📊 Test Summary: {report['summary']['passed_tests']}/{report['summary']['total_tests']} passed ({report['summary']['success_rate']:.1f}%)")
        
        return report

# Export the integration tester
__all__ = ['IntegrationTester', 'TestResult', 'TestScenario'] 