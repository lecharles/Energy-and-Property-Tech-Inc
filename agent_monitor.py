#!/usr/bin/env python3
"""
Agent Monitoring System
=======================

Real-time agent monitoring and performance tracking with comprehensive
error logging, quality assurance, and performance optimization.

Features:
- Real-time agent performance tracking
- Comprehensive error logging and analysis
- Quality validation and output assurance
- Performance metrics and benchmarking
- Agent health monitoring
- Resource usage tracking
- Alert system for critical issues
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import statistics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    """Agent execution status enumeration"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    RETRYING = "retrying"

class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class AgentMetrics:
    """Agent performance metrics"""
    agent_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    status: AgentStatus = AgentStatus.IDLE
    error_count: int = 0
    retry_count: int = 0
    output_quality_score: Optional[float] = None
    memory_usage: Optional[float] = None
    cpu_usage: Optional[float] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    cost_estimate: Optional[float] = None

@dataclass
class ErrorRecord:
    """Error record with detailed information"""
    timestamp: datetime
    agent_id: str
    error_type: str
    error_message: str
    severity: ErrorSeverity
    context: Dict[str, Any]
    stack_trace: Optional[str] = None
    recoverable: bool = True

@dataclass
class PerformanceAlert:
    """Performance alert for critical issues"""
    timestamp: datetime
    alert_type: str
    agent_id: str
    message: str
    severity: ErrorSeverity
    metrics: Dict[str, Any]

class AgentMonitor:
    """Real-time agent monitoring and performance tracking"""
    
    def __init__(self):
        self.agent_metrics: Dict[str, AgentMetrics] = {}
        self.error_log: List[ErrorRecord] = []
        self.performance_alerts: List[PerformanceAlert] = []
        self.execution_trace: List[str] = []
        self.overall_metrics = {
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'total_execution_time': 0.0,
            'average_execution_time': 0.0,
            'total_errors': 0,
            'total_retries': 0
        }
        self.quality_thresholds = {
            'min_output_length': 50,
            'max_execution_time': 300,  # 5 minutes
            'max_error_rate': 0.1,  # 10%
            'min_quality_score': 0.7
        }
        self.alert_thresholds = {
            'execution_time_threshold': 60,  # 1 minute
            'error_rate_threshold': 0.2,  # 20%
            'memory_usage_threshold': 0.8,  # 80%
            'cpu_usage_threshold': 0.9  # 90%
        }
    
    def track_agent_execution(self, agent_id: str, start_time: datetime = None) -> str:
        """Track agent execution start"""
        if start_time is None:
            start_time = datetime.now(timezone.utc)
        
        # Create or update agent metrics
        if agent_id not in self.agent_metrics:
            self.agent_metrics[agent_id] = AgentMetrics(
                agent_id=agent_id,
                start_time=start_time,
                status=AgentStatus.RUNNING
            )
        else:
            self.agent_metrics[agent_id].start_time = start_time
            self.agent_metrics[agent_id].status = AgentStatus.RUNNING
        
        # Update execution trace
        self.execution_trace.append(
            f"{start_time.isoformat()} - Agent {agent_id} started execution"
        )
        
        # Update overall metrics
        self.overall_metrics['total_executions'] += 1
        
        logger.info(f"⏱️ Agent {agent_id} execution tracking started")
        return agent_id
    
    def record_agent_completion(self, agent_id: str, end_time: datetime = None, 
                               output: Dict[str, Any] = None, success: bool = True) -> Dict[str, Any]:
        """Record agent completion and performance metrics"""
        if end_time is None:
            end_time = datetime.now(timezone.utc)
        
        if agent_id not in self.agent_metrics:
            logger.warning(f"⚠️ Agent {agent_id} not found in metrics, creating new record")
            self.track_agent_execution(agent_id)
        
        metrics = self.agent_metrics[agent_id]
        metrics.end_time = end_time
        metrics.duration = (end_time - metrics.start_time).total_seconds()
        metrics.status = AgentStatus.COMPLETED if success else AgentStatus.FAILED
        
        # Calculate quality score if output provided
        if output:
            metrics.output_quality_score = self._calculate_quality_score(output)
        
        # Update overall metrics
        if success:
            self.overall_metrics['successful_executions'] += 1
        else:
            self.overall_metrics['failed_executions'] += 1
        
        self.overall_metrics['total_execution_time'] += metrics.duration
        
        # Update average execution time
        total_executions = self.overall_metrics['successful_executions'] + self.overall_metrics['failed_executions']
        if total_executions > 0:
            self.overall_metrics['average_execution_time'] = (
                self.overall_metrics['total_execution_time'] / total_executions
            )
        
        # Check for performance alerts
        self._check_performance_alerts(agent_id, metrics)
        
        # Update execution trace
        status_text = "completed successfully" if success else "failed"
        self.execution_trace.append(
            f"{end_time.isoformat()} - Agent {agent_id} {status_text} in {metrics.duration:.2f}s"
        )
        
        logger.info(f"✅ Agent {agent_id} {status_text} in {metrics.duration:.2f}s")
        
        return asdict(metrics)
    
    def log_error(self, agent_id: str, error: Exception, context: Dict[str, Any] = None) -> ErrorRecord:
        """Log agent errors with detailed context"""
        if context is None:
            context = {}
        
        # Determine error severity
        severity = self._determine_error_severity(error, context)
        
        # Create error record
        error_record = ErrorRecord(
            timestamp=datetime.now(timezone.utc),
            agent_id=agent_id,
            error_type=type(error).__name__,
            error_message=str(error),
            severity=severity,
            context=context,
            stack_trace=self._get_stack_trace(error),
            recoverable=self._is_error_recoverable(error)
        )
        
        # Add to error log
        self.error_log.append(error_record)
        
        # Update agent metrics
        if agent_id in self.agent_metrics:
            self.agent_metrics[agent_id].error_count += 1
        
        # Update overall metrics
        self.overall_metrics['total_errors'] += 1
        
        # Check for critical alerts
        if severity == ErrorSeverity.CRITICAL:
            self._create_critical_alert(agent_id, error_record)
        
        logger.error(f"❌ Error in agent {agent_id}: {str(error)} (Severity: {severity.value})")
        
        return error_record
    
    def record_retry_attempt(self, agent_id: str, attempt_number: int, reason: str) -> None:
        """Record agent retry attempts"""
        if agent_id in self.agent_metrics:
            self.agent_metrics[agent_id].retry_count += 1
        
        self.overall_metrics['total_retries'] += 1
        
        self.execution_trace.append(
            f"{datetime.now(timezone.utc).isoformat()} - Agent {agent_id} retry attempt {attempt_number}: {reason}"
        )
        
        logger.info(f"🔄 Agent {agent_id} retry attempt {attempt_number}: {reason}")
    
    def track_resource_usage(self, agent_id: str, memory_usage: float = None, 
                           cpu_usage: float = None) -> None:
        """Track agent resource usage"""
        if agent_id in self.agent_metrics:
            if memory_usage is not None:
                self.agent_metrics[agent_id].memory_usage = memory_usage
            if cpu_usage is not None:
                self.agent_metrics[agent_id].cpu_usage = cpu_usage
            
            # Check for resource alerts
            self._check_resource_alerts(agent_id)
    
    def track_token_usage(self, agent_id: str, input_tokens: int = None, 
                         output_tokens: int = None, cost_estimate: float = None) -> None:
        """Track token usage and cost estimates"""
        if agent_id in self.agent_metrics:
            if input_tokens is not None:
                self.agent_metrics[agent_id].input_tokens = input_tokens
            if output_tokens is not None:
                self.agent_metrics[agent_id].output_tokens = output_tokens
            if cost_estimate is not None:
                self.agent_metrics[agent_id].cost_estimate = cost_estimate
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        # Calculate success rate
        total_executions = self.overall_metrics['total_executions']
        success_rate = (
            (self.overall_metrics['successful_executions'] / total_executions * 100)
            if total_executions > 0 else 0
        )
        
        # Calculate error rate
        error_rate = (
            (self.overall_metrics['total_errors'] / total_executions)
            if total_executions > 0 else 0
        )
        
        # Get agent-specific metrics
        agent_performance = {}
        for agent_id, metrics in self.agent_metrics.items():
            agent_performance[agent_id] = {
                'total_executions': 1,  # Each agent appears once in metrics
                'success_rate': 100 if metrics.status == AgentStatus.COMPLETED else 0,
                'average_execution_time': metrics.duration or 0,
                'error_count': metrics.error_count,
                'retry_count': metrics.retry_count,
                'quality_score': metrics.output_quality_score,
                'status': metrics.status.value
            }
        
        # Get recent errors
        recent_errors = self.error_log[-10:] if self.error_log else []
        
        # Get active alerts
        active_alerts = [alert for alert in self.performance_alerts 
                        if (datetime.now(timezone.utc) - alert.timestamp).total_seconds() < 3600]
        
        return {
            'overall_metrics': {
                **self.overall_metrics,
                'success_rate': success_rate,
                'error_rate': error_rate
            },
            'agent_performance': agent_performance,
            'recent_errors': [asdict(error) for error in recent_errors],
            'active_alerts': [asdict(alert) for alert in active_alerts],
            'execution_trace': self.execution_trace[-20:],  # Last 20 entries
            'quality_thresholds': self.quality_thresholds,
            'alert_thresholds': self.alert_thresholds,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
    
    def get_agent_health_status(self, agent_id: str) -> Dict[str, Any]:
        """Get health status for specific agent"""
        if agent_id not in self.agent_metrics:
            return {'status': 'unknown', 'message': 'Agent not found in metrics'}
        
        metrics = self.agent_metrics[agent_id]
        
        # Determine health status
        health_status = 'healthy'
        issues = []
        
        # Check execution time
        if metrics.duration and metrics.duration > self.alert_thresholds['execution_time_threshold']:
            health_status = 'warning'
            issues.append(f"Slow execution time: {metrics.duration:.2f}s")
        
        # Check error count
        if metrics.error_count > 0:
            health_status = 'warning' if health_status == 'healthy' else 'critical'
            issues.append(f"Error count: {metrics.error_count}")
        
        # Check quality score
        if metrics.output_quality_score and metrics.output_quality_score < self.quality_thresholds['min_quality_score']:
            health_status = 'warning' if health_status == 'healthy' else 'critical'
            issues.append(f"Low quality score: {metrics.output_quality_score:.2f}")
        
        # Check resource usage
        if metrics.memory_usage and metrics.memory_usage > self.alert_thresholds['memory_usage_threshold']:
            health_status = 'warning' if health_status == 'healthy' else 'critical'
            issues.append(f"High memory usage: {metrics.memory_usage:.1%}")
        
        if metrics.cpu_usage and metrics.cpu_usage > self.alert_thresholds['cpu_usage_threshold']:
            health_status = 'warning' if health_status == 'healthy' else 'critical'
            issues.append(f"High CPU usage: {metrics.cpu_usage:.1%}")
        
        return {
            'agent_id': agent_id,
            'health_status': health_status,
            'status': metrics.status.value,
            'execution_time': metrics.duration,
            'error_count': metrics.error_count,
            'retry_count': metrics.retry_count,
            'quality_score': metrics.output_quality_score,
            'issues': issues,
            'last_updated': metrics.end_time.isoformat() if metrics.end_time else None
        }
    
    def _calculate_quality_score(self, output: Dict[str, Any]) -> float:
        """Calculate quality score for agent output"""
        score = 0.0
        total_checks = 0
        
        # Check output structure
        if isinstance(output, dict):
            score += 0.2
            total_checks += 1
            
            # Check for required fields
            required_fields = ['agent_id', 'timestamp', 'status', 'output']
            present_fields = sum(1 for field in required_fields if field in output)
            score += (present_fields / len(required_fields)) * 0.3
            total_checks += 1
            
            # Check output content
            if 'output' in output and output['output']:
                content = str(output['output'])
                if len(content) >= self.quality_thresholds['min_output_length']:
                    score += 0.3
                else:
                    score += 0.1  # Partial credit for short content
                total_checks += 1
                
                # Check for structured data
                if isinstance(output['output'], dict):
                    score += 0.2
                    total_checks += 1
        
        return score / total_checks if total_checks > 0 else 0.0
    
    def _determine_error_severity(self, error: Exception, context: Dict[str, Any]) -> ErrorSeverity:
        """Determine error severity based on error type and context"""
        error_type = type(error).__name__
        
        # Critical errors
        if error_type in ['ConnectionError', 'TimeoutError', 'AuthenticationError']:
            return ErrorSeverity.CRITICAL
        
        # High severity errors
        if error_type in ['ValueError', 'KeyError', 'TypeError']:
            return ErrorSeverity.HIGH
        
        # Medium severity errors
        if error_type in ['RuntimeError', 'ImportError']:
            return ErrorSeverity.MEDIUM
        
        # Low severity errors (default)
        return ErrorSeverity.LOW
    
    def _is_error_recoverable(self, error: Exception) -> bool:
        """Determine if error is recoverable"""
        error_type = type(error).__name__
        
        # Non-recoverable errors
        if error_type in ['AuthenticationError', 'ImportError']:
            return False
        
        # Recoverable errors
        if error_type in ['ConnectionError', 'TimeoutError', 'ValueError', 'KeyError']:
            return True
        
        # Default to recoverable
        return True
    
    def _get_stack_trace(self, error: Exception) -> Optional[str]:
        """Get stack trace for error"""
        try:
            import traceback
            return ''.join(traceback.format_exception(type(error), error, error.__traceback__))
        except:
            return None
    
    def _check_performance_alerts(self, agent_id: str, metrics: AgentMetrics) -> None:
        """Check for performance alerts"""
        alerts = []
        
        # Check execution time
        if metrics.duration and metrics.duration > self.alert_thresholds['execution_time_threshold']:
            alerts.append(PerformanceAlert(
                timestamp=datetime.now(timezone.utc),
                alert_type='slow_execution',
                agent_id=agent_id,
                message=f"Agent {agent_id} took {metrics.duration:.2f}s to execute",
                severity=ErrorSeverity.MEDIUM,
                metrics={'execution_time': metrics.duration}
            ))
        
        # Check error count
        if metrics.error_count > 0:
            alerts.append(PerformanceAlert(
                timestamp=datetime.now(timezone.utc),
                alert_type='high_error_count',
                agent_id=agent_id,
                message=f"Agent {agent_id} has {metrics.error_count} errors",
                severity=ErrorSeverity.HIGH,
                metrics={'error_count': metrics.error_count}
            ))
        
        # Check quality score
        if metrics.output_quality_score and metrics.output_quality_score < self.quality_thresholds['min_quality_score']:
            alerts.append(PerformanceAlert(
                timestamp=datetime.now(timezone.utc),
                alert_type='low_quality_output',
                agent_id=agent_id,
                message=f"Agent {agent_id} produced low quality output: {metrics.output_quality_score:.2f}",
                severity=ErrorSeverity.MEDIUM,
                metrics={'quality_score': metrics.output_quality_score}
            ))
        
        # Add alerts to list
        self.performance_alerts.extend(alerts)
    
    def _check_resource_alerts(self, agent_id: str) -> None:
        """Check for resource usage alerts"""
        metrics = self.agent_metrics[agent_id]
        alerts = []
        
        # Check memory usage
        if metrics.memory_usage and metrics.memory_usage > self.alert_thresholds['memory_usage_threshold']:
            alerts.append(PerformanceAlert(
                timestamp=datetime.now(timezone.utc),
                alert_type='high_memory_usage',
                agent_id=agent_id,
                message=f"Agent {agent_id} using {metrics.memory_usage:.1%} memory",
                severity=ErrorSeverity.MEDIUM,
                metrics={'memory_usage': metrics.memory_usage}
            ))
        
        # Check CPU usage
        if metrics.cpu_usage and metrics.cpu_usage > self.alert_thresholds['cpu_usage_threshold']:
            alerts.append(PerformanceAlert(
                timestamp=datetime.now(timezone.utc),
                alert_type='high_cpu_usage',
                agent_id=agent_id,
                message=f"Agent {agent_id} using {metrics.cpu_usage:.1%} CPU",
                severity=ErrorSeverity.MEDIUM,
                metrics={'cpu_usage': metrics.cpu_usage}
            ))
        
        # Add alerts to list
        self.performance_alerts.extend(alerts)
    
    def _create_critical_alert(self, agent_id: str, error_record: ErrorRecord) -> None:
        """Create critical alert for severe errors"""
        alert = PerformanceAlert(
            timestamp=datetime.now(timezone.utc),
            alert_type='critical_error',
            agent_id=agent_id,
            message=f"Critical error in agent {agent_id}: {error_record.error_message}",
            severity=ErrorSeverity.CRITICAL,
            metrics={'error_type': error_record.error_type, 'severity': error_record.severity.value}
        )
        
        self.performance_alerts.append(alert)
        logger.critical(f"🚨 Critical alert: {alert.message}")

# Export the agent monitor
__all__ = ['AgentMonitor', 'AgentStatus', 'ErrorSeverity', 'AgentMetrics', 'ErrorRecord', 'PerformanceAlert'] 