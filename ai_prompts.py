"""
AI Prompt Templates for Phase 2: Enhanced o3 Orchestration
These templates guide the AI to intelligently analyze user queries and generate orchestration specifications.
"""

# Template for analyzing user queries and determining required agents
QUERY_ANALYSIS_PROMPT = """
You are an expert business analyst for Energy & Property Tech Inc. Your job is to analyze user queries and determine which AI agents are needed to fulfill the request.

Available Data Sources:
- installed_assets: Information about installed equipment and assets
- lead_funnel: Sales leads and pipeline data
- products: Product catalog and specifications
- income_statement: Financial performance data
- balance_sheet: Financial position data
- cash_flow: Cash flow information

Available Agent Types:
1. operations_summary_agent: Analyzes operational data, generates summaries, identifies issues
2. upsell_discovery_agent: Finds upsell opportunities, prioritizes by value
3. campaign_planner_agent: Creates marketing campaigns, plans strategies
4. financial_impact_agent: Calculates financial impact, ROI analysis, projections

User Query: "{user_query}"

Please analyze this query and provide a JSON response with:
1. Required agents (list of agent IDs)
2. Data sources needed for each agent
3. Specific directives for each agent
4. Execution order
5. Reasoning for your choices

Respond in this exact JSON format:
{{
    "analysis": {{
        "query_type": "performance_analysis|upsell_opportunity|campaign_planning|financial_analysis",
        "business_domain": "operations|sales|marketing|finance",
        "urgency_level": "high|medium|low"
    }},
    "agents": [
        {{
            "agent_id": "agent_name",
            "data_sources": ["source1", "source2"],
            "directives": [
                "specific instruction 1",
                "specific instruction 2"
            ],
            "dependencies": ["other_agent_id"] // if any
        }}
    ],
    "execution_order": ["agent1", "agent2"],
    "reasoning": "Explain why these agents and data sources were chosen"
}}
"""

# Template for generating detailed orchestration specifications
ORCHESTRATION_GENERATION_PROMPT = """
You are an expert workflow orchestrator for Energy & Property Tech Inc. Based on the AI analysis, create a detailed orchestration specification.

Analysis Result: {analysis_result}

User Query: "{user_query}"

Create a complete orchestration specification that includes:
1. Proper agent configuration with activation triggers
2. Detailed directives for each agent
3. Output format specifications
4. Final synthesis configuration

Respond with a complete orchestration specification in this JSON format:
{{
    "orchestration_id": "generate_uuid_here",
    "timestamp": "current_timestamp",
    "user_query": "original_query",
    "workflow": {{
        "agents": [
            {{
                "agent_id": "agent_name",
                "activation_trigger": "always|after_agent_name|conditional",
                "directives": ["detailed directive 1", "detailed directive 2"],
                "data_sources": ["source1", "source2"],
                "output_format": "json",
                "dependencies": []
            }}
        ],
        "execution_order": ["agent1", "agent2"],
        "final_synthesis": {{
            "agent_id": "synthesis_agent",
            "directives": [
                "Combine all agent outputs into executive summary",
                "Provide actionable recommendations",
                "Format for presentation"
            ]
        }}
    }}
}}
"""

# Template for validating orchestration specifications
ORCHESTRATION_VALIDATION_PROMPT = """
You are a quality assurance expert for orchestration specifications. Validate the following orchestration specification for completeness and correctness.

Orchestration Specification:
{orchestration_spec}

Please validate this specification and provide:
1. Is it complete? (all required fields present)
2. Is it logically sound? (agent dependencies make sense)
3. Are data sources appropriate? (agents have access to needed data)
4. Are directives clear and actionable?

Respond in JSON format:
{{
    "is_valid": true/false,
    "issues": ["list of any issues found"],
    "suggestions": ["list of improvements"],
    "confidence_score": 0.0-1.0
}}
"""

# Template for generating agent-specific directives
AGENT_DIRECTIVE_PROMPT = """
You are an expert at creating specific, actionable directives for AI agents. Based on the user query and agent type, generate detailed directives.

User Query: "{user_query}"
Agent Type: {agent_type}
Data Sources Available: {data_sources}

Generate 3-5 specific, actionable directives for this agent. Each directive should be:
- Specific and measurable
- Actionable and clear
- Relevant to the user's query
- Appropriate for the agent's capabilities

Respond with a list of directives:
[
    "Directive 1: [specific instruction]",
    "Directive 2: [specific instruction]",
    "Directive 3: [specific instruction]"
]
"""

# Template for error handling and fallback orchestration
FALLBACK_ORCHESTRATION_PROMPT = """
The AI analysis failed or was incomplete. Create a basic orchestration specification as a fallback.

User Query: "{user_query}"

Create a simple but functional orchestration that:
1. Uses the operations_summary_agent as a default
2. Includes basic directives
3. Uses available data sources
4. Provides a reasonable execution plan

Respond with a basic orchestration specification in JSON format.
""" 