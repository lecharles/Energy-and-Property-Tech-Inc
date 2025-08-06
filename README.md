# Energy & Property Tech Inc. Multi-Agent AI System

## Phase 1: Foundation Setup

A focused implementation of the multi-agent AI system using Fast MCP framework, o3 orchestration, and LangGraph execution. This phase establishes the foundation for the complete demo system.

## 🏗️ Architecture

### Technology Stack
- **Fast MCP Framework**: Rapid MCP tool development and data connectors
- **o3 Orchestrator**: JSON specification generation for agent workflows
- **LangGraph**: Multi-agent workflow execution engine
- **Python**: Core implementation language
- **Pandas**: Data processing and analysis
- **JSON**: Structured orchestration specifications and agent outputs

### Data Sources
- **Income Statement**: Monthly financial performance (Jan 2024 - Jun 2025)
- **Balance Sheet**: Quarterly financial position (Q1 2024 - Q2 2025)
- **Cash Flow**: Quarterly cash movements (Q1 2024 - Q2 2025)
- **Installed Assets**: Customer installations with upsell potential
- **Lead Funnel**: Sales pipeline and conversion data
- **Products**: Product catalog and descriptions

## 📁 Project Structure

```
Energy-and-Property-Tech-Inc/
├── fast_mcp_connectors.py      # Fast MCP data connectors and tools
├── o3_orchestrator.py          # o3 orchestration system
├── langgraph_workflow.py       # LangGraph workflow execution
├── main_integration.py         # Main system integration
├── requirements.txt            # Python dependencies
├── README.md                  # This file
├── demo-plan.md               # Complete demo plan
├── requirements.md             # Project requirements
├── lang-graph-examples.md     # LangGraph examples
├── Requirements/              # Agent requirements
├── System Prompts/            # Agent system prompts
└── orchestrations/            # Generated orchestration specs
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Phase 1 Demo
```bash
python main_integration.py
```

### 3. Interactive Mode
```bash
python main_integration.py interactive
```

## 🧪 Testing Individual Components

### Test Fast MCP Connectors
```bash
python fast_mcp_connectors.py
```

### Test o3 Orchestrator
```bash
python o3_orchestrator.py
```

### Test LangGraph Workflow
```bash
python langgraph_workflow.py
```

## 📊 Phase 1 Features

### ✅ Fast MCP Data Connectors
- **CSVDataConnector**: Generic CSV data connector with query capabilities
- **FinancialDataTool**: Access to income statement, balance sheet, and cash flow data
- **OperationalDataTool**: Access to installed assets, lead funnel, and products data
- **ClaudeCodeTool**: Integration with Claude Code for advanced analysis

### ✅ o3 Orchestration System
- **Query Analysis**: Intelligent parsing of user queries to determine required agents
- **JSON Specification Generation**: Structured orchestration specifications
- **File Management**: Save and load orchestration specifications
- **Validation**: Comprehensive validation of orchestration specs

### ✅ LangGraph Workflow Execution
- **State Management**: Typed state management for agent workflows
- **Agent Workers**: Mock implementations of all specialized agents
- **Workflow Orchestration**: Conditional execution based on orchestration specs
- **Final Synthesis**: Executive summary generation from all agent outputs

### ✅ Main Integration
- **System Initialization**: Complete system setup and validation
- **Query Processing**: End-to-end workflow from user query to final output
- **Status Monitoring**: System health and component status
- **Demo Modes**: Automated demo and interactive modes

## 🤖 Agent Types

### Operations Summary Agent
- **Purpose**: Generate operational summaries and identify critical issues
- **Data Sources**: Installed assets, lead funnel
- **Output**: Operational status, regional breakdown, critical issues

### Upsell Discovery Agent
- **Purpose**: Find and prioritize upsell opportunities
- **Data Sources**: Installed assets, products
- **Output**: Customer opportunities, potential value, next steps

### Campaign Planner Agent
- **Purpose**: Create targeted marketing campaigns
- **Data Sources**: Lead funnel, products
- **Output**: Campaign plans, timelines, projected revenue

### Financial Impact Agent
- **Purpose**: Calculate financial impact and ROI analysis
- **Data Sources**: Income statement, balance sheet, cash flow
- **Output**: Revenue projections, ROI analysis, quarterly forecasts

## 📈 Demo Scenarios

### Scenario 1: Performance Analysis
**Query**: "Analyze Q2 2025 performance and plan Q3 2025 growth strategy"
**Agents**: Operations Summary → Upsell Discovery → Campaign Planner → Financial Impact
**Output**: Comprehensive analysis with actionable recommendations

### Scenario 2: Regional Focus
**Query**: "Find upsell opportunities in EMEA region"
**Agents**: Operations Summary → Upsell Discovery
**Output**: Regional opportunity analysis with customer targeting

### Scenario 3: Campaign Planning
**Query**: "Create marketing campaign for new products"
**Agents**: Campaign Planner → Financial Impact
**Output**: Campaign strategy with financial projections

## 🔧 Configuration

### Environment Variables
Create a `.env` file for API keys and configuration:
```env
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

### Data Sources
Ensure all CSV files are in the project root:
- `Energy-&-Property-Tech-Inc_Sample_Data.xlsx - Income Statement.csv`
- `Energy-&-Property-Tech-Inc_Sample_Data.xlsx - Balance Sheet.csv`
- `Energy-&-Property-Tech-Inc_Sample_Data.xlsx - Cash Flow.csv`
- `Energy-&-Property-Tech-Inc_Sample_Data.xlsx - Installed Assets.csv`
- `Energy-&-Property-Tech-Inc_Sample_Data.xlsx - Lead Funnel.csv`
- `Energy-&-Property-Tech-Inc_Sample_Data.xlsx - Products.csv`

## 📋 Success Criteria

- ✅ Fast MCP tools successfully access all CSV data
- ✅ o3 generates valid JSON orchestration specifications
- ✅ LangGraph orchestrates multi-agent workflow execution
- ✅ All agents produce structured JSON outputs
- ✅ System demonstrates end-to-end workflow from query to results
- ✅ Orchestration specifications are saved to project folder

## 🔄 Next Steps

Phase 1 establishes the foundation. Future phases will include:
- **Phase 2**: Enhanced o3 orchestration with real AI integration
- **Phase 3**: Real agent implementations with Claude integration
- **Phase 4**: Advanced LangGraph workflows with error handling
- **Phase 5**: Integration testing and optimization
- **Phase 6**: Complete demo execution and presentation

## 🤝 Contributing

1. Follow the established code structure
2. Add comprehensive error handling
3. Include docstrings for all functions
4. Test individual components before integration
5. Update this README for any new features

## 📄 License

This project is part of the Energy & Property Tech Inc. multi-agent AI system demonstration.

---

**Phase 1 Status**: ✅ Complete  
**Last Updated**: December 2024  
**Version**: 1.0.0 