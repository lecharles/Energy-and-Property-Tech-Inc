#!/usr/bin/env python3
"""
Enhanced LangGraph Workflow v2.0
================================

Advanced LangGraph workflow with multi-agent orchestration, comprehensive error handling,
performance optimization, and real-time monitoring capabilities.

Features:
- Advanced state management with error tracking
- Dynamic agent routing and execution
- Real-time performance monitoring
- Comprehensive error handling and recovery
- Parallel execution support
- Caching mechanisms
- Quality validation and output assurance
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timezone
from typing import TypedDict, Annotated, List, Dict, Any, Optional
from pathlib import Path

from langgraph.graph import StateGraph, END, START
from langgraph.types import Send
import operator

# Import our existing components
from fast_mcp_connectors import FastMCPClient
from claude_agents import ClaudeAgentFactory
from ai_service import AIService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Enhanced state management with comprehensive tracking
class AdvancedAgentState(TypedDict):
    orchestration_spec: dict
    agent_outputs: Annotated[dict, operator.add]
    current_agent: str
    workflow_status: str
    final_output: str
    error_log: List[dict]
    performance_metrics: Dict[str, Any]
    execution_trace: List[str]
    cache: Dict[str, Any]
    parallel_execution: Dict[str, bool]

# Performance monitoring and metrics tracking
class PerformanceMonitor:
    def __init__(self):
        self.start_time = None
        self.agent_timings = {}
        self.overall_metrics = {}
        self.error_counts = {}
    
    def start_execution(self):
        """Start monitoring overall execution"""
        self.start_time = time.time()
        logger.info("🚀 Performance monitoring started")
    
    def start_agent_timing(self, agent_id: str):
        """Start timing for specific agent"""
        self.agent_timings[agent_id] = {
            'start_time': time.time(),
            'status': 'running'
        }
        logger.info(f"⏱️ Agent {agent_id} timing started")
    
    def end_agent_timing(self, agent_id: str, success: bool = True):
        """End timing for specific agent"""
        if agent_id in self.agent_timings:
            end_time = time.time()
            start_time = self.agent_timings[agent_id]['start_time']
            duration = end_time - start_time
            
            self.agent_timings[agent_id].update({
                'end_time': end_time,
                'duration': duration,
                'status': 'completed' if success else 'failed'
            })
            
            logger.info(f"✅ Agent {agent_id} completed in {duration:.2f}s")
    
    def record_error(self, agent_id: str, error: Exception):
        """Record error for specific agent"""
        if agent_id not in self.error_counts:
            self.error_counts[agent_id] = 0
        self.error_counts[agent_id] += 1
        logger.error(f"❌ Error in agent {agent_id}: {str(error)}")
    
    def get_performance_report(self) -> dict:
        """Generate comprehensive performance report"""
        if not self.start_time:
            return {}
        
        total_duration = time.time() - self.start_time
        total_agents = len(self.agent_timings)
        successful_agents = sum(1 for timing in self.agent_timings.values() 
                              if timing.get('status') == 'completed')
        
        return {
            'total_execution_time': total_duration,
            'total_agents_executed': total_agents,
            'successful_agents': successful_agents,
            'success_rate': (successful_agents / total_agents * 100) if total_agents > 0 else 0,
            'agent_timings': self.agent_timings,
            'error_counts': self.error_counts,
            'average_agent_time': sum(timing.get('duration', 0) for timing in self.agent_timings.values()) / total_agents if total_agents > 0 else 0
        }

# Error handling and recovery system
class WorkflowErrorHandler:
    def __init__(self):
        self.error_strategies = {
            'agent_timeout': self.handle_timeout,
            'agent_failure': self.handle_agent_failure,
            'data_error': self.handle_data_error,
            'network_error': self.handle_network_error,
            'validation_error': self.handle_validation_error
        }
        self.retry_attempts = {}
        self.max_retries = 3
    
    async def handle_timeout(self, agent_id: str, context: dict) -> dict:
        """Handle agent timeout with retry logic"""
        logger.warning(f"⏰ Timeout detected for agent {agent_id}")
        
        if agent_id not in self.retry_attempts:
            self.retry_attempts[agent_id] = 0
        
        if self.retry_attempts[agent_id] < self.max_retries:
            self.retry_attempts[agent_id] += 1
            logger.info(f"🔄 Retrying agent {agent_id} (attempt {self.retry_attempts[agent_id]})")
            return {'retry': True, 'attempt': self.retry_attempts[agent_id]}
        else:
            logger.error(f"❌ Max retries exceeded for agent {agent_id}")
            return {'retry': False, 'error': 'Max retries exceeded'}
    
    async def handle_agent_failure(self, agent_id: str, error: Exception) -> dict:
        """Handle agent failure with recovery options"""
        logger.error(f"💥 Agent {agent_id} failed: {str(error)}")
        
        # Try to recover with fallback strategy
        if hasattr(error, 'recoverable') and error.recoverable:
            logger.info(f"🔄 Attempting recovery for agent {agent_id}")
            return {'retry': True, 'recovery_attempt': True}
        else:
            logger.error(f"❌ Non-recoverable error for agent {agent_id}")
            return {'retry': False, 'error': str(error)}
    
    async def handle_data_error(self, data_source: str, error: Exception) -> dict:
        """Handle data access errors"""
        logger.error(f"📊 Data error for {data_source}: {str(error)}")
        
        # Try alternative data source or cached data
        return {
            'retry': True,
            'fallback_data': True,
            'error': str(error)
        }
    
    async def handle_network_error(self, error: Exception) -> dict:
        """Handle network connectivity issues"""
        logger.error(f"🌐 Network error: {str(error)}")
        
        # Wait and retry for network issues
        await asyncio.sleep(2)
        return {'retry': True, 'network_retry': True}
    
    async def handle_validation_error(self, agent_id: str, output: dict) -> dict:
        """Handle agent output validation errors"""
        logger.warning(f"🔍 Validation error for agent {agent_id}")
        
        # Try to fix validation issues
        return {
            'retry': True,
            'validation_fix': True,
            'output': output
        }

# Enhanced workflow nodes with comprehensive functionality
class EnhancedWorkflowNodes:
    def __init__(self, fast_mcp_client: FastMCPClient, performance_monitor: PerformanceMonitor, error_handler: WorkflowErrorHandler):
        self.fast_mcp_client = fast_mcp_client
        self.performance_monitor = performance_monitor
        self.error_handler = error_handler
        self.agent_factory = ClaudeAgentFactory()
        self.cache = {}
    
    def enhanced_orchestrator(self, state: AdvancedAgentState) -> AdvancedAgentState:
        """Enhanced orchestrator with validation and preparation"""
        logger.info("🎯 Enhanced orchestrator: Preparing workflow execution")
        
        try:
            # Validate orchestration specification
            spec = state["orchestration_spec"]
            if not spec or "workflow" not in spec:
                raise ValueError("Invalid orchestration specification")
            
            # Initialize performance monitoring
            self.performance_monitor.start_execution()
            
            # Prepare execution trace
            execution_trace = state.get("execution_trace", [])
            execution_trace.append(f"Orchestrator started at {datetime.now().isoformat()}")
            
            # Initialize cache if not present
            if "cache" not in state:
                state["cache"] = {}
            
            # Initialize parallel execution config
            if "parallel_execution" not in state:
                state["parallel_execution"] = {}
            
            logger.info(f"✅ Orchestrator prepared workflow with {len(spec['workflow']['agents'])} agents")
            
            return {
                **state,
                "workflow_status": "ready",
                "execution_trace": execution_trace,
                "performance_metrics": self.performance_monitor.get_performance_report()
            }
            
        except Exception as e:
            logger.error(f"❌ Orchestrator error: {str(e)}")
            error_log = state.get("error_log", [])
            error_log.append({
                "timestamp": datetime.now().isoformat(),
                "component": "orchestrator",
                "error": str(e),
                "type": "orchestrator_error"
            })
            
            return {
                **state,
                "workflow_status": "error",
                "error_log": error_log
            }
    
    def dynamic_agent_router(self, state: AdvancedAgentState) -> List[Send]:
        """Dynamic agent routing based on orchestration spec"""
        logger.info("🔄 Dynamic agent router: Analyzing agent requirements")
        
        try:
            spec = state["orchestration_spec"]
            agents = spec["workflow"]["agents"]
            
            # Determine which agents can run in parallel
            parallel_agents = []
            sequential_agents = []
            
            for agent in agents:
                agent_id = agent["agent_id"]
                dependencies = agent.get("dependencies", [])
                
                if not dependencies:
                    # No dependencies, can run in parallel
                    parallel_agents.append(agent_id)
                    state["parallel_execution"][agent_id] = True
                else:
                    # Has dependencies, must run sequentially
                    sequential_agents.append(agent_id)
                    state["parallel_execution"][agent_id] = False
            
            logger.info(f"📊 Agent routing: {len(parallel_agents)} parallel, {len(sequential_agents)} sequential")
            
            # Create worker assignments
            worker_assignments = []
            for agent in agents:
                agent_id = agent["agent_id"]
                
                # Check cache for existing results
                cache_key = f"{agent_id}_{hash(json.dumps(agent.get('directives', [])))}"
                if cache_key in state.get("cache", {}):
                    logger.info(f"💾 Using cached result for agent {agent_id}")
                    continue
                
                worker_assignments.append(
                    Send(
                        f"{agent_id}_worker",
                        {
                            "agent_id": agent_id,
                            "directives": agent["directives"],
                            "data_sources": agent["data_sources"],
                            "parallel_execution": state["parallel_execution"].get(agent_id, False)
                        }
                    )
                )
            
            logger.info(f"✅ Router created {len(worker_assignments)} worker assignments")
            return worker_assignments
            
        except Exception as e:
            logger.error(f"❌ Router error: {str(e)}")
            error_log = state.get("error_log", [])
            error_log.append({
                "timestamp": datetime.now().isoformat(),
                "component": "dynamic_router",
                "error": str(e),
                "type": "routing_error"
            })
            
            return []
    
    def create_agent_executor(self, agent_id: str):
        """Create generic agent executor with monitoring"""
        
        async def agent_executor(state: AdvancedAgentState) -> AdvancedAgentState:
            logger.info(f"🤖 Agent executor: Executing {agent_id}")
            
            try:
                # Start performance monitoring
                self.performance_monitor.start_agent_timing(agent_id)
                
                # Update execution trace
                execution_trace = state.get("execution_trace", [])
                execution_trace.append(f"Agent {agent_id} started at {datetime.now().isoformat()}")
                
                # Get agent configuration
                agent_config = state.get("agent_configs", {}).get(agent_id, {})
                directives = agent_config.get("directives", [])
                data_sources = agent_config.get("data_sources", [])
                
                # Create and execute agent
                agent = self.agent_factory.create_agent(agent_id, self.fast_mcp_client)
                result = await agent.execute(directives, data_sources)
                
                # Validate output
                if not result or "output" not in result:
                    raise ValueError(f"Invalid output from agent {agent_id}")
                
                # Cache the result
                cache_key = f"{agent_id}_{hash(json.dumps(directives))}"
                state["cache"][cache_key] = result
                
                # End performance monitoring
                self.performance_monitor.end_agent_timing(agent_id, success=True)
                
                # Update execution trace
                execution_trace.append(f"Agent {agent_id} completed successfully at {datetime.now().isoformat()}")
                
                logger.info(f"✅ Agent {agent_id} completed successfully")
                
                return {
                    **state,
                    "agent_outputs": {agent_id: result},
                    "current_agent": agent_id,
                    "execution_trace": execution_trace,
                    "performance_metrics": self.performance_monitor.get_performance_report()
                }
                
            except Exception as e:
                logger.error(f"❌ Agent {agent_id} error: {str(e)}")
                
                # Record error
                self.performance_monitor.record_error(agent_id, e)
                self.performance_monitor.end_agent_timing(agent_id, success=False)
                
                # Handle error with recovery strategies
                error_result = await self.error_handler.handle_agent_failure(agent_id, e)
                
                error_log = state.get("error_log", [])
                error_log.append({
                    "timestamp": datetime.now().isoformat(),
                    "component": agent_id,
                    "error": str(e),
                    "type": "agent_error",
                    "recovery_attempted": error_result.get("retry", False)
                })
                
                execution_trace = state.get("execution_trace", [])
                execution_trace.append(f"Agent {agent_id} failed at {datetime.now().isoformat()}: {str(e)}")
                
                return {
                    **state,
                    "current_agent": agent_id,
                    "error_log": error_log,
                    "execution_trace": execution_trace,
                    "performance_metrics": self.performance_monitor.get_performance_report()
                }
        
        return agent_executor
    
    def enhanced_synthesizer(self, state: AdvancedAgentState) -> AdvancedAgentState:
        """Enhanced synthesis with quality validation"""
        logger.info("🎯 Enhanced synthesizer: Combining agent outputs")
        
        try:
            # Get all agent outputs
            agent_outputs = state.get("agent_outputs", {})
            
            if not agent_outputs:
                raise ValueError("No agent outputs to synthesize")
            
            # Validate outputs
            valid_outputs = {}
            for agent_id, output in agent_outputs.items():
                if output and isinstance(output, dict):
                    valid_outputs[agent_id] = output
                else:
                    logger.warning(f"⚠️ Invalid output from agent {agent_id}")
            
            # Create comprehensive synthesis
            synthesis_result = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "orchestration_id": state["orchestration_spec"].get("orchestration_id", "unknown"),
                "user_query": state["orchestration_spec"].get("user_query", ""),
                "execution_summary": {
                    "total_agents": len(agent_outputs),
                    "successful_agents": len(valid_outputs),
                    "success_rate": (len(valid_outputs) / len(agent_outputs) * 100) if agent_outputs else 0,
                    "execution_time": state.get("performance_metrics", {}).get("total_execution_time", 0)
                },
                "agent_outputs": valid_outputs,
                "performance_metrics": state.get("performance_metrics", {}),
                "error_summary": {
                    "total_errors": len(state.get("error_log", [])),
                    "error_types": self._categorize_errors(state.get("error_log", []))
                },
                "recommendations": self._generate_recommendations(valid_outputs),
                "execution_trace": state.get("execution_trace", [])
            }
            
            # Update execution trace
            execution_trace = state.get("execution_trace", [])
            execution_trace.append(f"Synthesis completed at {datetime.now().isoformat()}")
            
            logger.info(f"✅ Synthesis completed with {len(valid_outputs)} valid outputs")
            
            return {
                **state,
                "final_output": json.dumps(synthesis_result, indent=2),
                "workflow_status": "completed",
                "execution_trace": execution_trace
            }
            
        except Exception as e:
            logger.error(f"❌ Synthesis error: {str(e)}")
            
            error_log = state.get("error_log", [])
            error_log.append({
                "timestamp": datetime.now().isoformat(),
                "component": "synthesizer",
                "error": str(e),
                "type": "synthesis_error"
            })
            
            return {
                **state,
                "workflow_status": "error",
                "error_log": error_log
            }
    
    def _categorize_errors(self, error_log: List[dict]) -> Dict[str, int]:
        """Categorize errors by type"""
        error_types = {}
        for error in error_log:
            error_type = error.get("type", "unknown")
            error_types[error_type] = error_types.get(error_type, 0) + 1
        return error_types
    
    def _generate_recommendations(self, agent_outputs: Dict[str, dict]) -> List[str]:
        """Generate recommendations based on agent outputs"""
        recommendations = []
        
        for agent_id, output in agent_outputs.items():
            if agent_id == "upsell_discovery_agent":
                # Extract upsell recommendations
                if "output" in output and "recommendations" in output["output"]:
                    recommendations.extend(output["output"]["recommendations"])
            
            elif agent_id == "campaign_planner_agent":
                # Extract campaign recommendations
                if "output" in output and "campaign_plan" in output["output"]:
                    plan = output["output"]["campaign_plan"]
                    if "recommendations" in plan:
                        recommendations.extend(plan["recommendations"])
        
        return recommendations[:5]  # Limit to top 5 recommendations

# Enhanced workflow engine with all advanced features
class EnhancedWorkflowEngine:
    def __init__(self, fast_mcp_client: FastMCPClient):
        self.fast_mcp_client = fast_mcp_client
        self.performance_monitor = PerformanceMonitor()
        self.error_handler = WorkflowErrorHandler()
        self.workflow_nodes = EnhancedWorkflowNodes(fast_mcp_client, self.performance_monitor, self.error_handler)
        self.workflow_graph = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the enhanced LangGraph workflow"""
        logger.info("🔨 Building enhanced LangGraph workflow")
        
        # Create workflow builder
        workflow_builder = StateGraph(AdvancedAgentState)
        
        # Add nodes
        workflow_builder.add_node("enhanced_orchestrator", self.workflow_nodes.enhanced_orchestrator)
        workflow_builder.add_node("dynamic_router", self.workflow_nodes.dynamic_agent_router)
        workflow_builder.add_node("enhanced_synthesizer", self.workflow_nodes.enhanced_synthesizer)
        
        # Add agent executor nodes for each agent type
        agent_types = [
            "upsell_discovery_agent",
            "campaign_planner_agent", 
            "financial_impact_agent",
            "operations_summary_agent",
            "synthesis_agent"
        ]
        
        for agent_type in agent_types:
            workflow_builder.add_node(
                f"{agent_type}_worker",
                self.workflow_nodes.create_agent_executor(agent_type)
            )
        
        # Add edges
        workflow_builder.add_edge(START, "enhanced_orchestrator")
        workflow_builder.add_conditional_edges(
            "enhanced_orchestrator",
            lambda state: "dynamic_router",
            ["dynamic_router"]
        )
        workflow_builder.add_conditional_edges(
            "dynamic_router",
            self.workflow_nodes.dynamic_agent_router,
            [f"{agent_type}_worker" for agent_type in agent_types]
        )
        
        # Connect all agent workers to synthesizer
        for agent_type in agent_types:
            workflow_builder.add_edge(f"{agent_type}_worker", "enhanced_synthesizer")
        
        workflow_builder.add_edge("enhanced_synthesizer", END)
        
        # Compile workflow
        workflow = workflow_builder.compile()
        logger.info("✅ Enhanced workflow built successfully")
        
        return workflow
    
    async def execute_orchestration(self, orchestration_file: str) -> dict:
        """Execute orchestration with enhanced features"""
        logger.info(f"🚀 Enhanced workflow execution: {orchestration_file}")
        
        try:
            # Load orchestration specification
            with open(orchestration_file, 'r') as f:
                orchestration_spec = json.load(f)
            
            # Initialize enhanced state
            initial_state = AdvancedAgentState(
                orchestration_spec=orchestration_spec,
                agent_outputs={},
                current_agent="",
                workflow_status="initialized",
                final_output="",
                error_log=[],
                performance_metrics={},
                execution_trace=[],
                cache={},
                parallel_execution={}
            )
            
            # Execute workflow
            logger.info("🔄 Starting enhanced workflow execution")
            result = await self.workflow_graph.ainvoke(initial_state)
            
            # Generate final performance report
            performance_report = self.performance_monitor.get_performance_report()
            logger.info(f"📊 Performance report: {performance_report}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Enhanced workflow execution error: {str(e)}")
            return {
                "error": str(e),
                "workflow_status": "error",
                "performance_metrics": self.performance_monitor.get_performance_report()
            }

# Export the enhanced workflow engine
__all__ = ['EnhancedWorkflowEngine', 'PerformanceMonitor', 'WorkflowErrorHandler'] 