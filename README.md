# Energy & Property Tech Inc. Multi-Agent AI System

## Phase 5: Core System Complete - Business Intelligence Delivered

The Energy Property AI System has been **fully validated at the core orchestration level** and successfully delivers complex business intelligence capabilities. While the core system is working perfectly, the Streamlit user interface has been identified as needing significant fixes.

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
├── plans/                     # Project planning and status reports
├── orchestrations/            # Generated orchestration specs
├── performance_reports/        # System performance metrics
└── test_results/              # Test execution results
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Phase 5 Demo (Terminal-Based)
```bash
python main_integration_v2.py
```

### 3. Interactive Mode
```bash
python main_integration_v2.py interactive
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
python langgraph_workflow_v2.py
```

## 📊 Phase 5 Features

### ✅ Core AI Orchestration System
- **AI Orchestration Generation**: Successfully creates 5-agent workflows
- **Agent Execution**: All 5 agents execute successfully with proper orchestration
- **Workflow Engine**: LangGraph workflow executes properly with real-time monitoring
- **Performance Tracking**: Detailed timing and performance metrics captured
- **Data Sources**: All 6 business data sources loaded and accessible

### ✅ Terminal-Based Execution
- **Query Processing**: Complex business queries processed successfully
- **Agent Orchestration**: Dynamic agent assignment and execution
- **Performance Monitoring**: Real-time metrics and optimization
- **File Generation**: Orchestration files, performance reports, test results

### ✅ Business Intelligence Capabilities
- **Financial Analysis**: Revenue, cost, and profit margin analysis by region
- **Operational Insights**: Asset utilization, lead funnel analysis
- **Strategic Planning**: Upsell opportunity identification and campaign planning
- **Synthesis**: Executive-level business insights and recommendations

### ❌ Known Issues (Phase 7 Priority)
- **Streamlit Dashboard**: Interface exists but not displaying real-time system metrics
- **Demo Launcher**: Interface exists but not properly connected to main integration system
- **Real-Time Updates**: No live execution visualization

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

### Synthesis Agent
- **Purpose**: Combine all agent outputs into executive-level insights
- **Data Sources**: All agent outputs
- **Output**: Business-ready recommendations and strategic insights

## 📈 Demo Scenarios

### Scenario 1: Comprehensive Business Analysis
**Query**: "I need to know: What is the most profitable region, why do we believe that is the case, which upsell opportunity is it the one that we are going to exploit there, what is the potential growth for that region, what is the potential business impact that we will get, which products do we have to sell over there, if you can help me prepare a campaign and for which channel we can do it in detail and explain why that would be great"
**Agents**: Financial Impact → Upsell Discovery → Operations Summary → Campaign Planner → Synthesis
**Output**: Complete business analysis with actionable recommendations
**Execution Time**: ~2.6 minutes

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
- ✅ All 5 agents produce structured JSON outputs
- ✅ System demonstrates end-to-end workflow from query to results
- ✅ Orchestration specifications are saved to project folder
- ✅ Performance metrics and timing data captured
- ✅ Complex business queries processed successfully
- ✅ Business intelligence insights generated and synthesized

## 🔄 Next Steps

### Phase 6: Evaluation Phase (Current Priority)
- **AI Evaluation**: Focus on business value validation
- **Evaluation Criteria**: Factuality, instruction adherence, coherence, hallucinations
- **LLM Agent as Judge**: Create an "LLM Agent as judge" for the whole system using GPT5
- **Evaluation Rubric**: Establish comprehensive evaluation framework
- **Performance Testing**: Comprehensive system testing
- **User Feedback**: Gather demo user experience feedback

### Phase 7: Streamlit UI Frontend (Future Priority)
- **Fix Streamlit Integration**: Connect web interface to core system
- **Streamlit UI Fixes**: Proper integration with core system
- **Real-Time Visualization**: Live execution monitoring
- **User Experience**: Professional demo interface

## 🤝 Contributing

1. Follow the established code structure
2. Add comprehensive error handling
3. Include docstrings for all functions
4. Test individual components before integration
5. Update this README for any new features

## 📄 License

This project is part of the Energy & Property Tech Inc. multi-agent AI system demonstration.

---

**Phase 5 Status**: ✅ Complete - Core System Working, UI Issues Identified  
**Last Updated**: August 11, 2025  
**Version**: 5.0.0  
**Next Phase**: Phase 6 - Evaluation Phase 
