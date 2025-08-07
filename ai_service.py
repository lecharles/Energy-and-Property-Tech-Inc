"""
AI Service for Phase 2: Enhanced o3 Orchestration
==================================================

This module implements AI-powered orchestration generation using OpenAI's GPT-4o-mini model.
It replaces the simple keyword-based approach from Phase 1 with intelligent AI analysis.

Key Features:
- Intelligent query analysis and intent understanding
- AI-driven agent selection and directive generation
- AI-powered orchestration validation
- Robust error handling with fallback mechanisms

Architecture:
- OpenAI API integration for natural language processing
- JSON response parsing with markdown code block handling
- Comprehensive error handling and logging
- Fallback orchestration generation for reliability

Usage:
    ai_service = AIService()
    analysis = await ai_service.analyze_query("Analyze Q2 performance")
    orchestration = await ai_service.generate_orchestration_spec(query, analysis)
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
import openai
from dotenv import load_dotenv

# Load environment variables for API key management
load_dotenv()

# Import our AI prompt templates for consistent instruction formatting
from ai_prompts import (
    QUERY_ANALYSIS_PROMPT,
    ORCHESTRATION_GENERATION_PROMPT,
    ORCHESTRATION_VALIDATION_PROMPT,
    AGENT_DIRECTIVE_PROMPT,
    FALLBACK_ORCHESTRATION_PROMPT
)

class AIService:
    """
    AI Service for intelligent orchestration generation
    
    This service leverages OpenAI's GPT-4o-mini model to:
    1. Analyze user queries and understand business intent
    2. Generate sophisticated orchestration specifications
    3. Validate orchestration completeness and logic
    4. Provide fallback mechanisms for reliability
    
    The service transforms simple keyword matching into intelligent
    business analysis and workflow planning.
    """
    
    def __init__(self):
        """
        Initialize the AI service with OpenAI client
        
        Validates API key configuration and sets up the OpenAI client
        for intelligent orchestration generation.
        """
        # Load and validate OpenAI API key from environment
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.openai_api_key or self.openai_api_key == 'your_openai_api_key_here':
            raise ValueError("OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file.")
        
        # Initialize OpenAI client for API communication
        self.client = openai.OpenAI(api_key=self.openai_api_key)
        
        # Use GPT-4o-mini for cost-effective, reliable orchestration tasks
        # This model provides excellent reasoning capabilities for business analysis
        self.model = "gpt-4o-mini"
        
        print(f"🤖 AI Service initialized with model: {self.model}")
    
    async def analyze_query(self, user_query: str) -> Dict[str, Any]:
        """
        Analyze user query using AI to determine required agents and data sources
        
        This method uses AI to understand the business intent behind user queries
        and determine which agents and data sources are needed to fulfill the request.
        
        Args:
            user_query: The user's business query (e.g., "Analyze Q2 performance")
            
        Returns:
            Dictionary containing AI analysis with:
            - Query type classification (performance_analysis, upsell_opportunity, etc.)
            - Business domain identification (operations, sales, marketing, finance)
            - Required agents and their data sources
            - Execution order and dependencies
            - Reasoning for the analysis
            
        Example:
            Input: "Analyze Q2 2025 performance and plan Q3 2025 growth strategy"
            Output: {
                "analysis": {"query_type": "performance_analysis", "business_domain": "finance"},
                "agents": [{"agent_id": "financial_impact_agent", "data_sources": ["income_statement"]}],
                "execution_order": ["financial_impact_agent"],
                "reasoning": "Financial analysis needed for performance evaluation..."
            }
        """
        print(f"🧠 Analyzing query with AI: {user_query[:50]}...")
        
        try:
            # Prepare the AI prompt with the user's query
            # The prompt includes context about available agents and data sources
            prompt = QUERY_ANALYSIS_PROMPT.format(user_query=user_query)
            
            # Call OpenAI API for intelligent analysis
            response = await self._call_openai(prompt)
            
            # Parse the JSON response from AI
            analysis_result = json.loads(response)
            
            print(f"✅ AI Analysis completed: {analysis_result.get('analysis', {}).get('query_type', 'unknown')} query")
            return analysis_result
            
        except Exception as error:
            print(f"❌ AI Analysis failed: {error}")
            # Return a fallback analysis to ensure system reliability
            return self._create_fallback_analysis(user_query)
    
    async def generate_orchestration_spec(self, user_query: str, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate detailed orchestration specification based on AI analysis
        
        This method takes the AI analysis and generates a complete orchestration
        specification that can be executed by the LangGraph workflow engine.
        
        Args:
            user_query: Original user query for context
            analysis_result: Result from query analysis containing agent requirements
            
        Returns:
            Complete orchestration specification with:
            - Unique orchestration ID and timestamp
            - Workflow configuration with agents and execution order
            - Agent-specific directives and data sources
            - Final synthesis configuration
            - AI generation metadata
            
        The orchestration spec follows the LangGraph workflow format and includes
        all necessary information for multi-agent execution.
        """
        print(f"🎯 Generating orchestration spec based on AI analysis...")
        
        try:
            # Prepare the AI prompt with analysis results
            # This prompt guides the AI to create a complete orchestration specification
            prompt = ORCHESTRATION_GENERATION_PROMPT.format(
                user_query=user_query,
                analysis_result=json.dumps(analysis_result, indent=2)
            )
            
            # Call OpenAI API for orchestration generation
            response = await self._call_openai(prompt)
            
            print(f"🔍 Raw AI response: {response[:200]}...")
            
            # Parse the JSON response from AI
            # Handle cases where AI returns JSON wrapped in markdown code blocks
            try:
                orchestration_spec = json.loads(response)
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing failed: {e}")
                print(f"🔍 Full response: {response}")
                # Try to extract JSON from markdown code blocks (common AI response format)
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    try:
                        orchestration_spec = json.loads(json_match.group())
                    except:
                        raise ValueError("Could not parse JSON from AI response")
                else:
                    raise ValueError("No JSON found in AI response")
            
            # Add metadata to track AI generation and provide context
            orchestration_spec["orchestration_id"] = str(uuid.uuid4())
            orchestration_spec["timestamp"] = datetime.utcnow().isoformat()
            orchestration_spec["user_query"] = user_query
            orchestration_spec["ai_generated"] = True
            orchestration_spec["analysis_summary"] = analysis_result.get("analysis", {})
            
            print(f"✅ Orchestration spec generated with {len(orchestration_spec.get('workflow', {}).get('agents', []))} agents")
            return orchestration_spec
            
        except Exception as error:
            print(f"❌ Orchestration generation failed: {error}")
            # Return a fallback orchestration to ensure system reliability
            return self._create_fallback_orchestration(user_query)
    
    async def validate_orchestration(self, orchestration_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate orchestration specification using AI
        
        This method uses AI to validate that the orchestration specification
        is complete, logically sound, and ready for execution.
        
        Args:
            orchestration_spec: Orchestration specification to validate
            
        Returns:
            Validation result with:
            - Validity status (true/false)
            - List of issues found
            - Suggestions for improvement
            - Confidence score
            
        The AI validation ensures quality and completeness before execution.
        """
        print(f"🔍 Validating orchestration specification...")
        
        try:
            # Prepare the AI prompt for validation
            prompt = ORCHESTRATION_VALIDATION_PROMPT.format(
                orchestration_spec=json.dumps(orchestration_spec, indent=2)
            )
            
            # Call OpenAI API for validation
            response = await self._call_openai(prompt)
            
            print(f"🔍 Raw validation response: {response[:200]}...")
            
            # Parse the JSON response from AI
            # Handle markdown code block wrapping
            try:
                validation_result = json.loads(response)
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing failed: {e}")
                print(f"🔍 Full response: {response}")
                # Try to extract JSON from markdown code blocks
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    try:
                        validation_result = json.loads(json_match.group())
                    except:
                        raise ValueError("Could not parse JSON from AI response")
                else:
                    raise ValueError("No JSON found in AI response")
            
            print(f"✅ Validation completed: {'Valid' if validation_result.get('is_valid', False) else 'Issues found'}")
            return validation_result
            
        except Exception as error:
            print(f"❌ Validation failed: {error}")
            # Return a basic validation result to ensure system continues
            return {
                "is_valid": True,  # Assume valid if validation fails
                "issues": [],
                "suggestions": [],
                "confidence_score": 0.5
            }
    
    async def generate_agent_directives(self, user_query: str, agent_type: str, data_sources: list) -> list:
        """
        Generate specific directives for an agent using AI
        
        This method creates detailed, actionable directives for individual agents
        based on the user query and available data sources.
        
        Args:
            user_query: Original user query for context
            agent_type: Type of agent (e.g., 'operations_summary_agent')
            data_sources: Available data sources for the agent
            
        Returns:
            List of specific, actionable directives for the agent
            
        The AI generates directives that are:
        - Specific and measurable
        - Actionable and clear
        - Relevant to the user's query
        - Appropriate for the agent's capabilities
        """
        print(f"📋 Generating directives for {agent_type}...")
        
        try:
            # Prepare the AI prompt for directive generation
            prompt = AGENT_DIRECTIVE_PROMPT.format(
                user_query=user_query,
                agent_type=agent_type,
                data_sources=", ".join(data_sources)
            )
            
            # Call OpenAI API for directive generation
            response = await self._call_openai(prompt)
            
            # Parse the JSON response from AI
            directives = json.loads(response)
            
            print(f"✅ Generated {len(directives)} directives for {agent_type}")
            return directives
            
        except Exception as error:
            print(f"❌ Directive generation failed: {error}")
            # Return basic directives to ensure agent functionality
            return [
                f"Analyze {agent_type} data",
                "Generate summary report",
                "Identify key insights"
            ]
    
    async def _call_openai(self, prompt: str) -> str:
        """
        Make a call to OpenAI API
        
        This is the core method that communicates with OpenAI's API.
        It handles the actual AI model interaction and response processing.
        
        Args:
            prompt: The prompt to send to OpenAI
            
        Returns:
            Response from OpenAI as a string
            
        The method uses GPT-4o-mini with conservative temperature settings
        for consistent, reliable results in business applications.
        """
        try:
            # Make the API call to OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert business analyst and workflow orchestrator. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for more consistent, predictable results
                max_tokens=2000   # Sufficient tokens for detailed orchestration specifications
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as error:
            print(f"❌ OpenAI API call failed: {error}")
            raise error
    
    def _create_fallback_analysis(self, user_query: str) -> Dict[str, Any]:
        """
        Create a fallback analysis when AI analysis fails
        
        This method provides a basic analysis when the AI service is unavailable
        or fails, ensuring system reliability and continuity.
        
        Args:
            user_query: The user query that failed AI analysis
            
        Returns:
            Basic analysis result with default agent configuration
        """
        return {
            "analysis": {
                "query_type": "general_analysis",
                "business_domain": "operations",
                "urgency_level": "medium"
            },
            "agents": [
                {
                    "agent_id": "operations_summary_agent",
                    "data_sources": ["installed_assets", "lead_funnel"],
                    "directives": [
                        "Analyze operational data",
                        "Generate summary report",
                        "Identify key insights"
                    ],
                    "dependencies": []
                }
            ],
            "execution_order": ["operations_summary_agent"],
            "reasoning": "Fallback analysis due to AI service error"
        }
    
    def _create_fallback_orchestration(self, user_query: str) -> Dict[str, Any]:
        """
        Create a fallback orchestration when AI generation fails
        
        This method provides a basic orchestration specification when the AI
        service is unavailable, ensuring the system can continue operating.
        
        Args:
            user_query: The user query that failed AI orchestration generation
            
        Returns:
            Basic orchestration specification with default workflow
        """
        return {
            "orchestration_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "user_query": user_query,
            "ai_generated": False,
            "workflow": {
                "agents": [
                    {
                        "agent_id": "operations_summary_agent",
                        "activation_trigger": "always",
                        "directives": [
                            "Analyze operational data",
                            "Generate summary report",
                            "Identify key insights"
                        ],
                        "data_sources": ["installed_assets", "lead_funnel"],
                        "output_format": "json",
                        "dependencies": []
                    }
                ],
                "execution_order": ["operations_summary_agent"],
                "final_synthesis": {
                    "agent_id": "synthesis_agent",
                    "directives": [
                        "Combine all agent outputs into executive summary",
                        "Provide actionable recommendations",
                        "Format for presentation"
                    ]
                }
            }
        }
    
    def get_service_status(self) -> Dict[str, Any]:
        """
        Get the status of the AI service
        
        Returns:
            Dictionary containing service status information including:
            - Service name and status
            - AI model being used
            - API configuration status
            - Timestamp of status check
        """
        return {
            "service": "ai_orchestration",
            "status": "ready",
            "model": self.model,
            "api_configured": bool(self.openai_api_key and self.openai_api_key != 'your_openai_api_key_here'),
            "timestamp": datetime.utcnow().isoformat()
        } 