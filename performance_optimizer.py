#!/usr/bin/env python3
"""
Performance Optimization System
==============================

Advanced performance optimization with caching, parallel execution,
resource management, and intelligent workload distribution.

Features:
- Intelligent caching with TTL and invalidation
- Parallel execution optimization
- Resource usage monitoring and optimization
- Workload distribution and load balancing
- Performance benchmarking and metrics
- Cost optimization and token management
- Memory and CPU optimization
"""

import asyncio
import json
import logging
import time
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import statistics
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CacheStrategy(Enum):
    """Cache strategy types"""
    LRU = "lru"  # Least Recently Used
    LFU = "lfu"  # Least Frequently Used
    TTL = "ttl"   # Time To Live
    NONE = "none" # No caching

class ExecutionMode(Enum):
    """Execution mode types"""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HYBRID = "hybrid"

@dataclass
class CacheEntry:
    """Cache entry with metadata"""
    key: str
    value: Any
    created_at: datetime
    accessed_at: datetime
    access_count: int = 0
    ttl: Optional[int] = None  # Time to live in seconds
    size: Optional[int] = None  # Size in bytes

@dataclass
class PerformanceMetrics:
    """Performance metrics for optimization"""
    execution_time: float
    memory_usage: float
    cpu_usage: float
    cache_hit_rate: float
    parallel_efficiency: float
    cost_per_execution: float
    throughput: float

class PerformanceOptimizer:
    """Advanced performance optimization system"""
    
    def __init__(self, max_cache_size: int = 1000, max_memory_usage: float = 0.8):
        self.cache: Dict[str, CacheEntry] = {}
        self.max_cache_size = max_cache_size
        self.max_memory_usage = max_memory_usage
        self.parallel_execution_config: Dict[str, bool] = {}
        self.performance_metrics: List[PerformanceMetrics] = []
        self.cache_strategy = CacheStrategy.LRU
        self.execution_mode = ExecutionMode.HYBRID
        self.thread_pool = ThreadPoolExecutor(max_workers=10)
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'size': 0
        }
        self.resource_monitor = ResourceMonitor()
        self.cost_tracker = CostTracker()
        
        # Start background tasks
        self._start_background_tasks()
    
    def _start_background_tasks(self):
        """Start background optimization tasks"""
        # Cache cleanup task
        asyncio.create_task(self._cache_cleanup_task())
        
        # Resource monitoring task
        asyncio.create_task(self._resource_monitoring_task())
        
        # Performance metrics collection task
        asyncio.create_task(self._metrics_collection_task())
    
    async def _cache_cleanup_task(self):
        """Background task for cache cleanup"""
        while True:
            try:
                await self._cleanup_cache()
                await asyncio.sleep(60)  # Run every minute
            except Exception as e:
                logger.error(f"Cache cleanup error: {e}")
                await asyncio.sleep(60)
    
    async def _resource_monitoring_task(self):
        """Background task for resource monitoring"""
        while True:
            try:
                await self.resource_monitor.update_metrics()
                await asyncio.sleep(10)  # Run every 10 seconds
            except Exception as e:
                logger.error(f"Resource monitoring error: {e}")
                await asyncio.sleep(10)
    
    async def _metrics_collection_task(self):
        """Background task for metrics collection"""
        while True:
            try:
                await self._collect_performance_metrics()
                await asyncio.sleep(30)  # Run every 30 seconds
            except Exception as e:
                logger.error(f"Metrics collection error: {e}")
                await asyncio.sleep(30)
    
    def enable_parallel_execution(self, agent_ids: List[str]) -> None:
        """Enable parallel execution for specific agents"""
        for agent_id in agent_ids:
            self.parallel_execution_config[agent_id] = True
        logger.info(f"✅ Parallel execution enabled for {len(agent_ids)} agents")
    
    def disable_parallel_execution(self, agent_ids: List[str]) -> None:
        """Disable parallel execution for specific agents"""
        for agent_id in agent_ids:
            self.parallel_execution_config[agent_id] = False
        logger.info(f"❌ Parallel execution disabled for {len(agent_ids)} agents")
    
    def cache_agent_output(self, agent_id: str, output: dict, ttl: int = 3600) -> str:
        """Cache agent output with TTL"""
        cache_key = self._generate_cache_key(agent_id, output)
        
        # Check if cache is full
        if len(self.cache) >= self.max_cache_size:
            self._evict_cache_entry()
        
        # Create cache entry
        entry = CacheEntry(
            key=cache_key,
            value=output,
            created_at=datetime.now(timezone.utc),
            accessed_at=datetime.now(timezone.utc),
            ttl=ttl,
            size=self._estimate_size(output)
        )
        
        self.cache[cache_key] = entry
        self.cache_stats['size'] = len(self.cache)
        
        logger.info(f"💾 Cached output for agent {agent_id} with key {cache_key}")
        return cache_key
    
    def get_cached_output(self, agent_id: str, output: dict) -> Optional[dict]:
        """Get cached output for agent"""
        cache_key = self._generate_cache_key(agent_id, output)
        
        if cache_key in self.cache:
            entry = self.cache[cache_key]
            
            # Check TTL
            if entry.ttl and (datetime.now(timezone.utc) - entry.created_at).total_seconds() > entry.ttl:
                del self.cache[cache_key]
                self.cache_stats['misses'] += 1
                return None
            
            # Update access statistics
            entry.accessed_at = datetime.now(timezone.utc)
            entry.access_count += 1
            self.cache_stats['hits'] += 1
            
            logger.info(f"🎯 Cache hit for agent {agent_id}")
            return entry.value
        else:
            self.cache_stats['misses'] += 1
            return None
    
    def optimize_workflow_order(self, orchestration_spec: dict) -> dict:
        """Optimize agent execution order for maximum efficiency"""
        agents = orchestration_spec.get("workflow", {}).get("agents", [])
        
        if not agents:
            return orchestration_spec
        
        # Analyze agent dependencies and execution times
        agent_analysis = self._analyze_agents(agents)
        
        # Optimize execution order
        optimized_agents = self._optimize_execution_order(agents, agent_analysis)
        
        # Update orchestration spec
        optimized_spec = orchestration_spec.copy()
        optimized_spec["workflow"]["agents"] = optimized_agents
        optimized_spec["workflow"]["execution_order"] = [agent["agent_id"] for agent in optimized_agents]
        
        logger.info(f"🔧 Optimized workflow order for {len(agents)} agents")
        return optimized_spec
    
    async def execute_parallel_agents(self, agent_tasks: List[Tuple[str, Callable]]) -> Dict[str, Any]:
        """Execute agents in parallel with optimization"""
        if not agent_tasks:
            return {}
        
        # Group tasks by execution mode
        parallel_tasks = []
        sequential_tasks = []
        
        for agent_id, task_func in agent_tasks:
            if self.parallel_execution_config.get(agent_id, False):
                parallel_tasks.append((agent_id, task_func))
            else:
                sequential_tasks.append((agent_id, task_func))
        
        results = {}
        
        # Execute parallel tasks
        if parallel_tasks:
            parallel_results = await self._execute_parallel_tasks(parallel_tasks)
            results.update(parallel_results)
        
        # Execute sequential tasks
        if sequential_tasks:
            sequential_results = await self._execute_sequential_tasks(sequential_tasks)
            results.update(sequential_results)
        
        return results
    
    async def _execute_parallel_tasks(self, tasks: List[Tuple[str, Callable]]) -> Dict[str, Any]:
        """Execute tasks in parallel with resource management"""
        results = {}
        
        # Limit concurrent executions based on resource availability
        max_concurrent = min(len(tasks), self._get_max_concurrent_tasks())
        
        # Create semaphore to limit concurrency
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def execute_task(agent_id: str, task_func: Callable):
            async with semaphore:
                start_time = time.time()
                try:
                    result = await task_func()
                    execution_time = time.time() - start_time
                    
                    # Track performance metrics
                    self._track_execution_metrics(agent_id, execution_time, True)
                    
                    return agent_id, result
                except Exception as e:
                    execution_time = time.time() - start_time
                    self._track_execution_metrics(agent_id, execution_time, False)
                    logger.error(f"❌ Parallel task {agent_id} failed: {e}")
                    return agent_id, None
        
        # Execute tasks concurrently
        task_coroutines = [execute_task(agent_id, task_func) for agent_id, task_func in tasks]
        completed_tasks = await asyncio.gather(*task_coroutines, return_exceptions=True)
        
        # Process results
        for result in completed_tasks:
            if isinstance(result, tuple):
                agent_id, task_result = result
                if task_result is not None:
                    results[agent_id] = task_result
        
        logger.info(f"⚡ Executed {len(tasks)} parallel tasks with {max_concurrent} concurrent")
        return results
    
    async def _execute_sequential_tasks(self, tasks: List[Tuple[str, Callable]]) -> Dict[str, Any]:
        """Execute tasks sequentially"""
        results = {}
        
        for agent_id, task_func in tasks:
            start_time = time.time()
            try:
                result = await task_func()
                execution_time = time.time() - start_time
                
                # Track performance metrics
                self._track_execution_metrics(agent_id, execution_time, True)
                
                results[agent_id] = result
                logger.info(f"✅ Sequential task {agent_id} completed in {execution_time:.2f}s")
                
            except Exception as e:
                execution_time = time.time() - start_time
                self._track_execution_metrics(agent_id, execution_time, False)
                logger.error(f"❌ Sequential task {agent_id} failed: {e}")
        
        return results
    
    def get_performance_metrics(self) -> dict:
        """Get comprehensive performance metrics"""
        # Calculate cache hit rate
        total_requests = self.cache_stats['hits'] + self.cache_stats['misses']
        cache_hit_rate = (self.cache_stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        
        # Calculate average execution time
        if self.performance_metrics:
            avg_execution_time = statistics.mean([m.execution_time for m in self.performance_metrics])
            avg_memory_usage = statistics.mean([m.memory_usage for m in self.performance_metrics])
            avg_cpu_usage = statistics.mean([m.cpu_usage for m in self.performance_metrics])
        else:
            avg_execution_time = avg_memory_usage = avg_cpu_usage = 0
        
        # Get resource usage
        current_memory = self.resource_monitor.get_memory_usage()
        current_cpu = self.resource_monitor.get_cpu_usage()
        
        # Get cost metrics
        cost_metrics = self.cost_tracker.get_cost_metrics()
        
        return {
            'cache_metrics': {
                **self.cache_stats,
                'hit_rate': cache_hit_rate,
                'size': len(self.cache),
                'max_size': self.max_cache_size
            },
            'execution_metrics': {
                'total_executions': len(self.performance_metrics),
                'average_execution_time': avg_execution_time,
                'average_memory_usage': avg_memory_usage,
                'average_cpu_usage': avg_cpu_usage,
                'parallel_efficiency': self._calculate_parallel_efficiency()
            },
            'resource_metrics': {
                'current_memory_usage': current_memory,
                'current_cpu_usage': current_cpu,
                'max_memory_usage': self.max_memory_usage
            },
            'cost_metrics': cost_metrics,
            'optimization_config': {
                'cache_strategy': self.cache_strategy.value,
                'execution_mode': self.execution_mode.value,
                'parallel_agents': sum(1 for enabled in self.parallel_execution_config.values() if enabled)
            },
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
    
    def _generate_cache_key(self, agent_id: str, output: dict) -> str:
        """Generate cache key for agent output"""
        # Create a hash of the agent ID and output content
        content = f"{agent_id}:{json.dumps(output, sort_keys=True)}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _estimate_size(self, obj: Any) -> int:
        """Estimate size of object in bytes"""
        try:
            return len(json.dumps(obj))
        except:
            return 0
    
    def _evict_cache_entry(self) -> None:
        """Evict cache entry based on strategy"""
        if not self.cache:
            return
        
        if self.cache_strategy == CacheStrategy.LRU:
            # Remove least recently used
            oldest_key = min(self.cache.keys(), 
                           key=lambda k: self.cache[k].accessed_at)
        elif self.cache_strategy == CacheStrategy.LFU:
            # Remove least frequently used
            oldest_key = min(self.cache.keys(), 
                           key=lambda k: self.cache[k].access_count)
        elif self.cache_strategy == CacheStrategy.TTL:
            # Remove expired entries first, then oldest
            current_time = datetime.now(timezone.utc)
            expired_keys = [k for k, v in self.cache.items() 
                          if v.ttl and (current_time - v.created_at).total_seconds() > v.ttl]
            
            if expired_keys:
                oldest_key = expired_keys[0]
            else:
                oldest_key = min(self.cache.keys(), 
                               key=lambda k: self.cache[k].created_at)
        else:
            # Random eviction
            oldest_key = list(self.cache.keys())[0]
        
        del self.cache[oldest_key]
        self.cache_stats['evictions'] += 1
        logger.info(f"🗑️ Evicted cache entry: {oldest_key}")
    
    async def _cleanup_cache(self) -> None:
        """Clean up expired cache entries"""
        current_time = datetime.now(timezone.utc)
        expired_keys = []
        
        for key, entry in self.cache.items():
            if entry.ttl and (current_time - entry.created_at).total_seconds() > entry.ttl:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            logger.info(f"🧹 Cleaned up {len(expired_keys)} expired cache entries")
    
    def _analyze_agents(self, agents: List[dict]) -> Dict[str, dict]:
        """Analyze agents for optimization"""
        analysis = {}
        
        for agent in agents:
            agent_id = agent["agent_id"]
            dependencies = agent.get("dependencies", [])
            
            # Estimate execution time based on agent type
            estimated_time = self._estimate_agent_execution_time(agent_id)
            
            # Determine if agent can run in parallel
            can_run_parallel = len(dependencies) == 0
            
            analysis[agent_id] = {
                'dependencies': dependencies,
                'estimated_time': estimated_time,
                'can_run_parallel': can_run_parallel,
                'complexity': self._estimate_agent_complexity(agent)
            }
        
        return analysis
    
    def _optimize_execution_order(self, agents: List[dict], analysis: Dict[str, dict]) -> List[dict]:
        """Optimize agent execution order"""
        # Sort agents by dependencies and estimated time
        sorted_agents = sorted(agents, key=lambda agent: (
            len(analysis[agent["agent_id"]]["dependencies"]),  # Fewer dependencies first
            -analysis[agent["agent_id"]]["estimated_time"]  # Longer tasks first
        ))
        
        return sorted_agents
    
    def _estimate_agent_execution_time(self, agent_id: str) -> float:
        """Estimate execution time for agent"""
        # Base execution times for different agent types
        base_times = {
            'upsell_discovery_agent': 15.0,
            'campaign_planner_agent': 20.0,
            'financial_impact_agent': 25.0,
            'operations_summary_agent': 10.0,
            'synthesis_agent': 5.0
        }
        
        return base_times.get(agent_id, 15.0)
    
    def _estimate_agent_complexity(self, agent: dict) -> str:
        """Estimate agent complexity"""
        directives = agent.get("directives", [])
        data_sources = agent.get("data_sources", [])
        
        complexity_score = len(directives) + len(data_sources)
        
        if complexity_score <= 2:
            return "low"
        elif complexity_score <= 4:
            return "medium"
        else:
            return "high"
    
    def _get_max_concurrent_tasks(self) -> int:
        """Get maximum concurrent tasks based on resource availability"""
        memory_usage = self.resource_monitor.get_memory_usage()
        cpu_usage = self.resource_monitor.get_cpu_usage()
        
        # Base on available resources
        if memory_usage > 0.8 or cpu_usage > 0.9:
            return 2
        elif memory_usage > 0.6 or cpu_usage > 0.7:
            return 4
        else:
            return 6
    
    def _track_execution_metrics(self, agent_id: str, execution_time: float, success: bool):
        """Track execution metrics"""
        metrics = PerformanceMetrics(
            execution_time=execution_time,
            memory_usage=self.resource_monitor.get_memory_usage(),
            cpu_usage=self.resource_monitor.get_cpu_usage(),
            cache_hit_rate=self._get_cache_hit_rate(),
            parallel_efficiency=self._calculate_parallel_efficiency(),
            cost_per_execution=self.cost_tracker.get_cost_per_execution(),
            throughput=1.0 / execution_time if execution_time > 0 else 0
        )
        
        self.performance_metrics.append(metrics)
        
        # Keep only recent metrics
        if len(self.performance_metrics) > 100:
            self.performance_metrics = self.performance_metrics[-50:]
    
    def _get_cache_hit_rate(self) -> float:
        """Get current cache hit rate"""
        total = self.cache_stats['hits'] + self.cache_stats['misses']
        return (self.cache_stats['hits'] / total * 100) if total > 0 else 0
    
    def _calculate_parallel_efficiency(self) -> float:
        """Calculate parallel execution efficiency"""
        if not self.performance_metrics:
            return 0.0
        
        # Calculate efficiency based on execution time vs expected time
        recent_metrics = self.performance_metrics[-10:]
        avg_execution_time = statistics.mean([m.execution_time for m in recent_metrics])
        
        # Assume ideal parallel execution would be 50% faster
        expected_time = avg_execution_time * 0.5
        efficiency = (expected_time / avg_execution_time) if avg_execution_time > 0 else 0
        
        return min(efficiency, 1.0)
    
    async def _collect_performance_metrics(self):
        """Collect and store performance metrics"""
        # This method can be extended to store metrics in a database
        # or send them to a monitoring system
        pass

class ResourceMonitor:
    """Resource usage monitoring"""
    
    def __init__(self):
        self.memory_usage = 0.0
        self.cpu_usage = 0.0
        self.last_update = datetime.now(timezone.utc)
    
    async def update_metrics(self):
        """Update resource metrics"""
        try:
            import psutil
            
            # Get memory usage
            memory = psutil.virtual_memory()
            self.memory_usage = memory.percent / 100.0
            
            # Get CPU usage
            self.cpu_usage = psutil.cpu_percent(interval=1) / 100.0
            
            self.last_update = datetime.now(timezone.utc)
            
        except ImportError:
            # psutil not available, use dummy values
            self.memory_usage = 0.5
            self.cpu_usage = 0.3
    
    def get_memory_usage(self) -> float:
        """Get current memory usage"""
        return self.memory_usage
    
    def get_cpu_usage(self) -> float:
        """Get current CPU usage"""
        return self.cpu_usage

class CostTracker:
    """Cost tracking and optimization"""
    
    def __init__(self):
        self.total_cost = 0.0
        self.execution_count = 0
        self.cost_per_token = 0.0001  # Example cost per token
        self.total_tokens = 0
    
    def track_execution_cost(self, tokens_used: int, cost: float = None):
        """Track execution cost"""
        if cost is None:
            cost = tokens_used * self.cost_per_token
        
        self.total_cost += cost
        self.execution_count += 1
        self.total_tokens += tokens_used
    
    def get_cost_metrics(self) -> dict:
        """Get cost metrics"""
        avg_cost_per_execution = self.total_cost / self.execution_count if self.execution_count > 0 else 0
        
        return {
            'total_cost': self.total_cost,
            'total_executions': self.execution_count,
            'average_cost_per_execution': avg_cost_per_execution,
            'total_tokens': self.total_tokens,
            'cost_per_token': self.cost_per_token
        }
    
    def get_cost_per_execution(self) -> float:
        """Get average cost per execution"""
        return self.total_cost / self.execution_count if self.execution_count > 0 else 0

# Export the performance optimizer
__all__ = ['PerformanceOptimizer', 'CacheStrategy', 'ExecutionMode', 'ResourceMonitor', 'CostTracker'] 