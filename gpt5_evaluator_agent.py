#!/usr/bin/env python3
"""
GPT5 Evaluator Agent - Core Evaluation Engine

This module implements the GPT5 Evaluator Agent that provides comprehensive,
objective assessment of agent responses in the Energy Property AI System.

Author: Carlos Lozano
Date: August 11, 2025
Phase: 6 - Evaluation Phase
"""

import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import openai
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class EvaluationCriteria:
    """Evaluation criteria with weights for scoring calculation."""
    factuality: float = 0.30      # 30% weight
    data_source_validation: float = 0.15  # 15% weight
    instruction_following: float = 0.25  # 25% weight
    conciseness: float = 0.15     # 15% weight
    completeness: float = 0.15    # 15% weight


@dataclass
class EvaluationResult:
    """Structured evaluation result for a single agent response."""
    timestamp: str
    agent_type: str
    query: str
    response: str
    factuality_rating: int
    data_source_validation_rating: int
    instruction_following_rating: int
    conciseness_rating: int
    completeness_rating: int
    factuality_points: float
    data_source_validation_points: float
    instruction_following_points: float
    conciseness_points: float
    completeness_points: float
    total_score: int
    factuality_comment: str
    data_source_validation_comment: str
    instruction_following_comment: str
    conciseness_comment: str
    completeness_comment: str
    overall_assessment: str
    improvement_recommendations: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class GPT5EvaluatorAgent:
    """
    GPT5 Evaluator Agent - AI-powered evaluation system for agent responses.
    
    This agent uses GPT-5 exclusively to evaluate the quality and effectiveness
    of responses from specialized business intelligence agents.
    """
    
    def __init__(self, api_key: str, model: str = "gpt-5"):
        """
        Initialize the GPT5 Evaluator Agent.
        
        Args:
            api_key: OpenAI API key for GPT-5 access
            model: GPT-5 model variant (default: "gpt-5")
        """
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=api_key)
        self.criteria = EvaluationCriteria()
        
        # Validate model is GPT-5 variant
        if not model.startswith("gpt-5"):
            raise ValueError("GPT5 Evaluator Agent requires GPT-5 model variants only")
        
        logger.info(f"GPT5 Evaluator Agent initialized with model: {model}")
        
    def load_system_prompt(self) -> str:
        """
        Load the system prompt for the GPT5 Evaluator Agent.
        
        Returns:
            Complete system prompt for evaluation
        """
        try:
            with open("System Prompts/GPT5-Evaluator-Agent-System-Prompt.md", "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.error("System prompt file not found. Using fallback prompt.")
            return self._get_fallback_prompt()
    
    def _get_fallback_prompt(self) -> str:
        """Fallback system prompt if file cannot be loaded."""
        return """You are the GPT5 Evaluator Agent, an expert AI judge responsible for objectively assessing the quality and effectiveness of responses from specialized business intelligence agents in the Energy Property AI System.

Your primary responsibility is to provide comprehensive, objective evaluation of agent responses across multiple quality dimensions, delivering both quantitative scoring and qualitative feedback to drive continuous improvement in the AI system.

Evaluation Framework:
- Factuality (1-4 scale, 30% weight): Accuracy, data correctness, hallucinations
- Data Source Validation (1-4 scale, 15% weight): Reference to legitimate business data sources
- Instruction Following (1-4 scale, 25% weight): Query compliance, requirement adherence  
- Conciseness (1-4 scale, 15% weight): Communication efficiency, focus
- Completeness (1-4 scale, 15% weight): Coverage, thoroughness, gaps

Output your evaluation in the exact format specified in the system prompt."""
    
    def evaluate_response(
        self, 
        agent_type: str, 
        query: str, 
        response: str,
        context: Optional[Dict[str, Any]] = None
    ) -> EvaluationResult:
        """
        Evaluate an agent response using GPT-5.
        
        Args:
            agent_type: Type of agent that provided the response
            query: User query that was asked
            response: Agent response to evaluate
            context: Additional context for evaluation
            
        Returns:
            EvaluationResult with comprehensive assessment
        """
        logger.info(f"Starting evaluation of {agent_type} response")
        start_time = time.time()
        
        try:
            # Prepare evaluation prompt
            evaluation_prompt = self._prepare_evaluation_prompt(
                agent_type, query, response, context
            )
            
            # Get GPT-5 evaluation
            evaluation_text = self._call_gpt5(evaluation_prompt)
            
            # Parse evaluation results
            evaluation_result = self._parse_evaluation_result(
                evaluation_text, agent_type, query, response
            )
            
            # Calculate weighted scores
            evaluation_result = self._calculate_weighted_scores(evaluation_result)
            
            execution_time = time.time() - start_time
            logger.info(f"Evaluation completed in {execution_time:.2f} seconds")
            
            return evaluation_result
            
        except Exception as e:
            logger.error(f"Evaluation failed: {str(e)}")
            raise
    
    def _prepare_evaluation_prompt(
        self, 
        agent_type: str, 
        query: str, 
        response: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Prepare the evaluation prompt for GPT-5.
        
        Args:
            agent_type: Type of agent being evaluated
            query: User query that was asked
            response: Agent response to evaluate
            context: Additional context information
            
        Returns:
            Formatted evaluation prompt
        """
        prompt = f"""Please evaluate the following agent response according to the evaluation framework.

AGENT TYPE: {agent_type}
USER QUERY: {query}

AGENT RESPONSE:
{response}

{self._add_context_info(context) if context else ""}

IMPORTANT: Pay special attention to Data Source Validation - verify that the agent response references legitimate business data sources (Income Statement, Balance Sheet, Cash Flow, Installed Assets, Lead Funnel, Products) rather than making generic statements or hallucinations.

Please provide your evaluation in the exact format specified in the system prompt, including:
1. The evaluation table with ratings and points
2. Detailed assessment for each criterion (especially Data Source Validation)
3. Overall assessment
4. Improvement recommendations

Remember to use the 1-4 scale for each criterion and calculate the weighted 1-10 total score."""
        
        return prompt
    
    def _add_context_info(self, context: Dict[str, Any]) -> str:
        """Add context information to the evaluation prompt."""
        context_info = "\nADDITIONAL CONTEXT:\n"
        for key, value in context.items():
            context_info += f"- {key}: {value}\n"
        return context_info
    
    def _call_gpt5(self, prompt: str) -> str:
        """
        Call GPT-5 API for evaluation.
        
        Args:
            prompt: Evaluation prompt to send to GPT-5
            
        Returns:
            GPT-5 evaluation response
        """
        try:
            logger.info("Calling GPT-5 API for evaluation")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.load_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Low temperature for consistent evaluation
                max_tokens=2000,  # Sufficient tokens for detailed evaluation
                timeout=60  # 60 second timeout
            )
            
            evaluation_text = response.choices[0].message.content
            logger.info("GPT-5 evaluation received successfully")
            
            return evaluation_text
            
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error calling GPT-5: {str(e)}")
            raise
    
    def _parse_evaluation_result(
        self, 
        evaluation_text: str, 
        agent_type: str, 
        query: str, 
        response: str
    ) -> EvaluationResult:
        """
        Parse the GPT-5 evaluation text into structured results.
        
        Args:
            evaluation_text: Raw evaluation text from GPT-5
            agent_type: Type of agent evaluated
            query: User query that was asked
            response: Agent response that was evaluated
            
        Returns:
            Parsed EvaluationResult object
        """
        try:
            # Extract ratings from the evaluation table
            ratings = self._extract_ratings(evaluation_text)
            
            # Extract comments and assessments
            comments = self._extract_comments(evaluation_text)
            
            # Extract improvement recommendations
            recommendations = self._extract_recommendations(evaluation_text)
            
            # Create evaluation result
            result = EvaluationResult(
                timestamp=datetime.now().isoformat(),
                agent_type=agent_type,
                query=query,
                response=response,
                factuality_rating=ratings.get('factuality', 0),
                data_source_validation_rating=ratings.get('data_source_validation', 0),
                instruction_following_rating=ratings.get('instruction_following', 0),
                conciseness_rating=ratings.get('conciseness', 0),
                completeness_rating=ratings.get('completeness', 0),
                factuality_points=0.0,  # Will be calculated later
                data_source_validation_points=0.0,  # Will be calculated later
                instruction_following_points=0.0,  # Will be calculated later
                conciseness_points=0.0,  # Will be calculated later
                completeness_points=0.0,  # Will be calculated later
                total_score=0,  # Will be calculated later
                factuality_comment=comments.get('factuality', ''),
                data_source_validation_comment=comments.get('data_source_validation', ''),
                instruction_following_comment=comments.get('instruction_following', ''),
                conciseness_comment=comments.get('conciseness', ''),
                completeness_comment=comments.get('completeness', ''),
                overall_assessment=comments.get('overall', ''),
                improvement_recommendations=recommendations
            )
            
            logger.info("Evaluation result parsed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Failed to parse evaluation result: {str(e)}")
            raise
    
    def _extract_ratings(self, evaluation_text: str) -> Dict[str, int]:
        """Extract numerical ratings from the evaluation text."""
        ratings = {}
        
        # Look for ratings in the table format
        lines = evaluation_text.split('\n')
        for line in lines:
            if '|' in line and 'Factuality' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3:
                    try:
                        ratings['factuality'] = int(parts[2])
                    except ValueError:
                        pass
            elif '|' in line and 'Instruction Following' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3:
                    try:
                        ratings['instruction_following'] = int(parts[2])
                    except ValueError:
                        pass
            elif '|' in line and 'Conciseness' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3:
                    try:
                        ratings['conciseness'] = int(parts[2])
                    except ValueError:
                        pass
            elif '|' in line and 'Completeness' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3:
                    try:
                        ratings['completeness'] = int(parts[2])
                    except ValueError:
                        pass
        
        # Fallback: look for ratings in text format
        if not ratings:
            import re
            factuality_match = re.search(r'Factuality.*?(\d)', evaluation_text)
            if factuality_match:
                ratings['factuality'] = int(factuality_match.group(1))
            
            instruction_match = re.search(r'Instruction Following.*?(\d)', evaluation_text)
            if instruction_match:
                ratings['instruction_following'] = int(instruction_match.group(1))
            
            conciseness_match = re.search(r'Conciseness.*?(\d)', evaluation_text)
            if conciseness_match:
                ratings['conciseness'] = int(conciseness_match.group(1))
            
            completeness_match = re.search(r'Completeness.*?(\d)', evaluation_text)
            if completeness_match:
                ratings['completeness'] = int(completeness_match.group(1))
        
        return ratings
    
    def _extract_comments(self, evaluation_text: str) -> Dict[str, str]:
        """Extract comments and assessments from the evaluation text."""
        comments = {}
        
        # Extract detailed assessments
        sections = evaluation_text.split('###')
        for section in sections:
            if 'Factuality:' in section:
                comments['factuality'] = section.split(':', 1)[1].strip() if ':' in section else ''
            elif 'Instruction Following:' in section:
                comments['instruction_following'] = section.split(':', 1)[1].strip() if ':' in section else ''
            elif 'Conciseness:' in section:
                comments['conciseness'] = section.split(':', 1)[1].strip() if ':' in section else ''
            elif 'Completeness:' in section:
                comments['completeness'] = section.split(':', 1)[1].strip() if ':' in section else ''
            elif 'Overall Assessment' in section:
                comments['overall'] = section.split('\n', 1)[1].strip() if '\n' in section else ''
        
        return comments
    
    def _extract_recommendations(self, evaluation_text: str) -> List[str]:
        """Extract improvement recommendations from the evaluation text."""
        recommendations = []
        
        # Look for recommendations section
        if 'Improvement Recommendations' in evaluation_text:
            rec_section = evaluation_text.split('Improvement Recommendations')[-1]
            lines = rec_section.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and len(line) > 10:
                    recommendations.append(line)
        
        return recommendations
    
    def _calculate_weighted_scores(self, result: EvaluationResult) -> EvaluationResult:
        """
        Calculate weighted scores based on ratings and criteria weights.
        
        Args:
            result: EvaluationResult with ratings
            
        Returns:
            Updated EvaluationResult with calculated scores
        """
        # Calculate points for each criterion
        result.factuality_points = result.factuality_rating * self.criteria.factuality
        result.data_source_validation_points = result.data_source_validation_rating * self.criteria.data_source_validation
        result.instruction_following_points = result.instruction_following_rating * self.criteria.instruction_following
        result.conciseness_points = result.conciseness_rating * self.criteria.conciseness
        result.completeness_points = result.completeness_rating * self.criteria.completeness
        
        # Calculate total weighted score (1-10)
        total_points = (
            result.factuality_points +
            result.data_source_validation_points +
            result.instruction_following_points +
            result.conciseness_points +
            result.completeness_points
        )
        
        # Round to nearest whole number
        result.total_score = round(total_points)
        
        logger.info(f"Calculated total score: {result.total_score}/10")
        return result
    
    def batch_evaluate(
        self, 
        evaluations: List[Tuple[str, str, str, Optional[Dict[str, Any]]]]
    ) -> List[EvaluationResult]:
        """
        Evaluate multiple agent responses in batch.
        
        Args:
            evaluations: List of (agent_type, query, response, context) tuples
            
        Returns:
            List of EvaluationResult objects
        """
        logger.info(f"Starting batch evaluation of {len(evaluations)} responses")
        results = []
        
        for i, (agent_type, query, response, context) in enumerate(evaluations):
            try:
                logger.info(f"Evaluating response {i+1}/{len(evaluations)}: {agent_type}")
                result = self.evaluate_response(agent_type, query, response, context)
                results.append(result)
                
                # Small delay to avoid rate limiting
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Failed to evaluate response {i+1}: {str(e)}")
                # Continue with next evaluation
        
        logger.info(f"Batch evaluation completed: {len(results)}/{len(evaluations)} successful")
        return results
    
    def save_evaluation_result(self, result: EvaluationResult, filename: str) -> None:
        """
        Save evaluation result to a JSON file.
        
        Args:
            result: EvaluationResult to save
            filename: Output filename
        """
        try:
            with open(filename, 'w') as f:
                json.dump(result.to_dict(), f, indent=2)
            logger.info(f"Evaluation result saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save evaluation result: {str(e)}")
            raise
    
    def generate_evaluation_report(self, results: List[EvaluationResult]) -> str:
        """
        Generate a comprehensive evaluation report.
        
        Args:
            results: List of EvaluationResult objects
            
        Returns:
            Formatted evaluation report
        """
        if not results:
            return "No evaluation results to report."
        
        report = f"# GPT5 Evaluator Agent - Evaluation Report\n\n"
        report += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"**Total Evaluations**: {len(results)}\n\n"
        
        # Summary statistics
        total_scores = [r.total_score for r in results]
        avg_score = sum(total_scores) / len(total_scores)
        min_score = min(total_scores)
        max_score = max(total_scores)
        
        report += f"## Summary Statistics\n\n"
        report += f"- **Average Score**: {avg_score:.1f}/10\n"
        report += f"- **Score Range**: {min_score}/10 - {max_score}/10\n"
        report += f"- **Total Evaluations**: {len(results)}\n\n"
        
        # Individual results
        report += f"## Individual Evaluations\n\n"
        for i, result in enumerate(results, 1):
            report += f"### {i}. {result.agent_type}\n\n"
            report += f"- **Score**: {result.total_score}/10\n"
            report += f"- **Factuality**: {result.factuality_rating}/4 ({result.factuality_points:.1f} pts)\n"
            report += f"- **Instruction Following**: {result.instruction_following_rating}/4 ({result.instruction_following_points:.1f} pts)\n"
            report += f"- **Conciseness**: {result.conciseness_rating}/4 ({result.conciseness_points:.1f} pts)\n"
            report += f"- **Completeness**: {result.completeness_rating}/4 ({result.completeness_points:.1f} pts)\n\n"
            report += f"**Overall Assessment**: {result.overall_assessment}\n\n"
            report += f"**Improvement Recommendations**:\n"
            for rec in result.improvement_recommendations:
                report += f"- {rec}\n"
            report += f"\n---\n\n"
        
        return report


def main():
    """Main function for testing the GPT5 Evaluator Agent."""
    import os
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("ERROR: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key to use the GPT5 Evaluator Agent")
        return
    
    try:
        # Initialize evaluator
        evaluator = GPT5EvaluatorAgent(api_key)
        print("✅ GPT5 Evaluator Agent initialized successfully")
        
        # Test evaluation
        test_agent_type = "Financial Impact Agent"
        test_query = "What is the most profitable region and why?"
        test_response = "Based on the financial data, EMEA is the most profitable region with a 23% profit margin, driven by strong revenue growth and cost optimization."
        
        print(f"\n🧪 Testing evaluation with {test_agent_type}")
        print(f"Query: {test_query}")
        print(f"Response: {test_response}")
        
        result = evaluator.evaluate_response(test_agent_type, test_query, test_response)
        
        print(f"\n📊 Evaluation Results:")
        print(f"Total Score: {result.total_score}/10")
        print(f"Factuality: {result.factuality_rating}/4")
        print(f"Data Source Validation: {result.data_source_validation_rating}/4")
        print(f"Instruction Following: {result.instruction_following_rating}/4")
        print(f"Conciseness: {result.conciseness_rating}/4")
        print(f"Completeness: {result.completeness_rating}/4")
        
        # Save result
        evaluator.save_evaluation_result(result, "test_evaluation_result.json")
        print(f"\n💾 Test evaluation saved to test_evaluation_result.json")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        logger.error(f"Main function error: {str(e)}")


if __name__ == "__main__":
    main()
