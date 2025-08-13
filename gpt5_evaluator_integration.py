#!/usr/bin/env python3
"""
GPT5 Evaluator Agent Integration

This script integrates the GPT5 Evaluator Agent with the existing
Energy Property AI System to evaluate real agent responses.

Author: Carlos Lozano
Date: August 11, 2025
Phase: 6 - Evaluation Phase
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from gpt5_evaluator_agent import GPT5EvaluatorAgent, EvaluationResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GPT5EvaluatorIntegration:
    """
    Integration layer for GPT5 Evaluator Agent with existing system.
    
    This class provides methods to evaluate agent responses from the
    Energy Property AI System and integrate with existing monitoring.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the integration layer.
        
        Args:
            api_key: OpenAI API key for GPT-5 access
        """
        self.evaluator = GPT5EvaluatorAgent(api_key)
        self.evaluation_history: List[EvaluationResult] = []
        
        logger.info("GPT5 Evaluator Integration initialized")
    
    def evaluate_agent_response(
        self, 
        agent_type: str, 
        query: str, 
        response: str,
        context: Optional[Dict[str, Any]] = None
    ) -> EvaluationResult:
        """
        Evaluate a single agent response.
        
        Args:
            agent_type: Type of agent that provided the response
            query: User query that was asked
            response: Agent response to evaluate
            context: Additional context for evaluation
            
        Returns:
            EvaluationResult with comprehensive assessment
        """
        logger.info(f"Evaluating {agent_type} response")
        
        try:
            # Perform evaluation
            result = self.evaluator.evaluate_response(
                agent_type, query, response, context
            )
            
            # Store in history
            self.evaluation_history.append(result)
            
            logger.info(f"Evaluation completed: {result.total_score}/10")
            return result
            
        except Exception as e:
            logger.error(f"Evaluation failed: {str(e)}")
            raise
    
    def evaluate_orchestration_results(
        self, 
        orchestration_file: str
    ) -> List[EvaluationResult]:
        """
        Evaluate all agent responses from an orchestration file.
        
        Args:
            orchestration_file: Path to orchestration results file
            
        Returns:
            List of EvaluationResult objects
        """
        logger.info(f"Evaluating orchestration results from {orchestration_file}")
        
        try:
            # Load orchestration results
            with open(orchestration_file, 'r') as f:
                orchestration_data = json.load(f)
            
            # Extract agent responses
            agent_responses = self._extract_agent_responses(orchestration_data)
            
            # Evaluate each response
            results = []
            for agent_type, query, response in agent_responses:
                try:
                    result = self.evaluate_agent_response(agent_type, query, response)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Failed to evaluate {agent_type}: {str(e)}")
                    continue
            
            logger.info(f"Orchestration evaluation completed: {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Failed to evaluate orchestration: {str(e)}")
            raise
    
    def _extract_agent_responses(self, orchestration_data: Dict[str, Any]) -> List[tuple]:
        """
        Extract agent responses from orchestration data.
        
        Args:
            orchestration_data: Loaded orchestration data
            
        Returns:
            List of (agent_type, query, response) tuples
        """
        agent_responses = []
        
        try:
            # Extract user query
            user_query = orchestration_data.get('user_query', 'Unknown query')
            
            # Extract agent outputs
            agent_outputs = orchestration_data.get('agent_outputs', {})
            
            for agent_name, output in agent_outputs.items():
                if isinstance(output, dict) and 'response' in output:
                    response = output['response']
                    agent_responses.append((agent_name, user_query, response))
                elif isinstance(output, str):
                    agent_responses.append((agent_name, user_query, output))
            
            logger.info(f"Extracted {len(agent_responses)} agent responses")
            return agent_responses
            
        except Exception as e:
            logger.error(f"Failed to extract agent responses: {str(e)}")
            return []
    
    def evaluate_test_results(
        self, 
        test_results_dir: str = "test_results"
    ) -> List[EvaluationResult]:
        """
        Evaluate all agent responses from test result files.
        
        Args:
            test_results_dir: Directory containing test result files
            
        Returns:
            List of EvaluationResult objects
        """
        logger.info(f"Evaluating test results from {test_results_dir}")
        
        if not os.path.exists(test_results_dir):
            logger.warning(f"Test results directory not found: {test_results_dir}")
            return []
        
        all_results = []
        
        # Process each test result file
        for filename in os.listdir(test_results_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(test_results_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        test_data = json.load(f)
                    
                    # Extract and evaluate responses
                    agent_responses = self._extract_agent_responses(test_data)
                    for agent_type, query, response in agent_responses:
                        try:
                            result = self.evaluate_agent_response(agent_type, query, response)
                            all_results.append(result)
                        except Exception as e:
                            logger.error(f"Failed to evaluate {agent_type} from {filename}: {str(e)}")
                            continue
                            
                except Exception as e:
                    logger.error(f"Failed to process {filename}: {str(e)}")
                    continue
        
        logger.info(f"Test results evaluation completed: {len(all_results)} results")
        return all_results
    
    def generate_integration_report(self) -> str:
        """
        Generate comprehensive integration report.
        
        Returns:
            Formatted integration report
        """
        if not self.evaluation_history:
            return "No evaluations performed yet."
        
        report = f"# GPT5 Evaluator Agent - Integration Report\n\n"
        report += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"**Total Evaluations**: {len(self.evaluation_history)}\n\n"
        
        # Summary statistics
        total_scores = [r.total_score for r in self.evaluation_history]
        avg_score = sum(total_scores) / len(total_scores)
        min_score = min(total_scores)
        max_score = max(total_scores)
        
        report += f"## Summary Statistics\n\n"
        report += f"- **Average Score**: {avg_score:.1f}/10\n"
        report += f"- **Score Range**: {min_score}/10 - {max_score}/10\n"
        report += f"- **Total Evaluations**: {len(self.evaluation_history)}\n\n"
        
        # Agent performance breakdown
        agent_scores = {}
        for result in self.evaluation_history:
            if result.agent_type not in agent_scores:
                agent_scores[result.agent_type] = []
            agent_scores[result.agent_type].append(result.total_score)
        
        report += f"## Agent Performance Breakdown\n\n"
        for agent_type, scores in agent_scores.items():
            avg_agent_score = sum(scores) / len(scores)
            report += f"### {agent_type}\n"
            report += f"- **Evaluations**: {len(scores)}\n"
            report += f"- **Average Score**: {avg_agent_score:.1f}/10\n"
            report += f"- **Score Range**: {min(scores)}/10 - {max(scores)}/10\n\n"
        
        # Recent evaluations
        report += f"## Recent Evaluations\n\n"
        recent_results = sorted(
            self.evaluation_history, 
            key=lambda x: x.timestamp, 
            reverse=True
        )[:10]
        
        for result in recent_results:
            report += f"### {result.agent_type} - {result.timestamp}\n"
            report += f"- **Score**: {result.total_score}/10\n"
            report += f"- **Data Source Validation**: {result.data_source_validation_rating}/4\n"
            report += f"- **Query**: {result.query[:100]}...\n"
            report += f"- **Overall Assessment**: {result.overall_assessment[:200]}...\n\n"
        
        return report
    
    def save_evaluation_history(self, filename: str = None) -> str:
        """
        Save evaluation history to file.
        
        Args:
            filename: Output filename (auto-generated if None)
            
        Returns:
            Path to saved file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"evaluation_history_{timestamp}.json"
        
        try:
            # Convert to serializable format
            history_data = [result.to_dict() for result in self.evaluation_history]
            
            with open(filename, 'w') as f:
                json.dump(history_data, f, indent=2)
            
            logger.info(f"Evaluation history saved to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Failed to save evaluation history: {str(e)}")
            raise
    
    def load_evaluation_history(self, filename: str) -> None:
        """
        Load evaluation history from file.
        
        Args:
            filename: Path to evaluation history file
        """
        try:
            with open(filename, 'r') as f:
                history_data = json.load(f)
            
            # Convert back to EvaluationResult objects
            self.evaluation_history = []
            for data in history_data:
                result = EvaluationResult(**data)
                self.evaluation_history.append(result)
            
            logger.info(f"Loaded {len(self.evaluation_history)} evaluations from {filename}")
            
        except Exception as e:
            logger.error(f"Failed to load evaluation history: {str(e)}")
            raise


def main():
    """Main function for testing the integration."""
    import os
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("ERROR: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key to use the GPT5 Evaluator Agent")
        return
    
    try:
        # Initialize integration
        integration = GPT5EvaluatorIntegration(api_key)
        print("✅ GPT5 Evaluator Integration initialized successfully")
        
        # Test with sample data
        print("\n🧪 Testing integration with sample agent responses...")
        
        # Sample agent responses
        sample_responses = [
            ("Financial Impact Agent", "What is the most profitable region?", 
             "EMEA is the most profitable region with 23% profit margin."),
            ("Upsell Discovery Agent", "Find upsell opportunities", 
             "EMEA shows €2.4M upsell potential with 45% of customers on basic packages."),
            ("Operations Summary Agent", "Provide operational status", 
             "Current status: 94% asset utilization. EMEA has 15% higher maintenance costs.")
        ]
        
        # Evaluate each response
        for agent_type, query, response in sample_responses:
            try:
                result = integration.evaluate_agent_response(agent_type, query, response)
                print(f"✅ {agent_type}: {result.total_score}/10")
            except Exception as e:
                print(f"❌ {agent_type}: Failed - {str(e)}")
        
        # Generate report
        print("\n📋 Generating integration report...")
        report = integration.generate_integration_report()
        print(report)
        
        # Save history
        filename = integration.save_evaluation_history()
        print(f"\n💾 Evaluation history saved to {filename}")
        
        print("\n🎉 Integration test completed successfully!")
        
    except Exception as e:
        print(f"❌ Integration test failed: {str(e)}")
        logger.error(f"Integration test error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
