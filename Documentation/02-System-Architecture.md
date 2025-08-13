# System Architecture: Energy & Property Tech Inc. Multi-Agent AI System

## 🏗️ High-Level Architecture

The Energy & Property Tech Inc. Multi-Agent AI System is built on a **layered architecture** that separates concerns and enables scalability, maintainability, and extensibility. The system follows modern software engineering principles with clear separation between data, business logic, orchestration, and presentation layers.

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    User Interface Layer                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   Streamlit │  │   Terminal  │  │      API Endpoints      │ │
│  │   Dashboard │  │   Interface │  │                         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                  Orchestration Layer                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │     O3      │  │  LangGraph  │  │    Agent Coordinator    │ │
│  │Orchestrator │  │  Workflows  │  │                         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                    Agent Layer                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ Operations  │  │   Upsell    │  │      Financial          │ │
│  │  Summary    │  │ Discovery   │  │       Impact            │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
│  ┌─────────────┐  ┌─────────────┐                             │
│  │  Campaign   │  │  Synthesis  │                             │
│  │  Planner    │  │    Agent    │                             │
│  └─────────────┘  └─────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                   Data Access Layer                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ Fast MCP    │  │   Pandas    │  │      Data Connectors    │ │
│  │  Tools      │  │  Processing │  │                         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                     Data Layer                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   Income    │  │   Balance   │  │      Cash Flow          │ │
│  │ Statement   │  │   Sheet     │  │                         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ Installed   │  │    Lead     │  │       Products          │ │
│  │   Assets    │  │   Funnel    │  │                         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

### Core Technologies

#### **Programming Language**
- **Python 3.10+**: Primary development language
  - **Why Python?**: Extensive AI/ML ecosystem, rapid development, strong community
  - **Version**: 3.10+ for modern language features and performance improvements

#### **AI and Machine Learning**
- **OpenAI GPT Models**: Primary reasoning and analysis capabilities
  - **Models Used**: GPT-4, GPT-5 (when available)
  - **Purpose**: Natural language understanding, complex reasoning, text generation
  - **Integration**: OpenAI Python client with async support

- **Anthropic Claude**: Support for context-heavy tasks
  - **Models Used**: Claude 3.5 Sonnet, Claude 3.5 Haiku
  - **Purpose**: Long-context analysis, document processing, specialized tasks
  - **Integration**: Anthropic Python client with streaming support

#### **Multi-Agent Orchestration**
- **LangGraph**: Core workflow orchestration engine
  - **Version**: 0.2.0+
  - **Purpose**: Multi-agent workflow management, state management, error handling
  - **Features**: Supervisor pattern, parallel execution, conditional routing

- **LangChain**: AI application framework
  - **Purpose**: LLM integration, prompt management, output parsing
  - **Features**: Structured outputs, memory management, tool integration

#### **Data Processing and Analysis**
- **Pandas**: Data manipulation and analysis
  - **Version**: 2.0.0+
  - **Purpose**: CSV processing, data transformation, statistical analysis
  - **Features**: High-performance data operations, rich data structures

- **NumPy**: Numerical computing
  - **Purpose**: Mathematical operations, array processing, statistical functions
  - **Integration**: Used by Pandas for underlying numerical operations

### Integration Technologies

#### **Model Context Protocol (MCP)**
- **FastMCP**: Rapid MCP tool development framework
  - **Version**: 2.11.1+
  - **Purpose**: Universal translator for connecting AI agents to external systems
  - **Features**: Tool generation, data connectors, API integration

#### **Web Framework**
- **Streamlit**: User interface and dashboard
  - **Version**: 1.48.0+
  - **Purpose**: Interactive web interface, real-time data visualization
  - **Features**: Rapid prototyping, rich widgets, real-time updates

- **FastAPI**: API development (future)
  - **Purpose**: RESTful API endpoints, OpenAPI documentation
  - **Features**: Async support, automatic validation, high performance

#### **Data Visualization**
- **Plotly**: Interactive charts and graphs
  - **Version**: 6.2.0+
  - **Purpose**: Data visualization, interactive dashboards, reporting
  - **Features**: Rich chart types, interactivity, export capabilities

### Development and Operations

#### **Development Tools**
- **Poetry/UV**: Dependency management
  - **Purpose**: Package management, virtual environments, dependency resolution
  - **Features**: Lock files, dependency groups, development dependencies

- **Pydantic**: Data validation and settings
  - **Version**: 2.0.0+
  - **Purpose**: Data model validation, configuration management, serialization
  - **Features**: Type hints, automatic validation, JSON serialization

#### **System Monitoring**
- **PSUtil**: System and process monitoring
  - **Version**: 7.0.0+
  - **Purpose**: Performance monitoring, resource usage tracking
  - **Features**: CPU, memory, disk, network monitoring

- **Logging**: Built-in Python logging
  - **Purpose**: Application logging, debugging, monitoring
  - **Features**: Configurable levels, handlers, formatters

## 🔄 Data Flow Architecture

### Data Flow Overview

```
User Query → Query Analysis → Agent Selection → Data Retrieval → Agent Execution → Response Synthesis → Output Delivery
```

### Detailed Data Flow

#### **1. Query Input and Analysis**
```
User Query (Natural Language)
         │
         ▼
┌─────────────────┐
│  Query Analyzer │ ← Determines required agents and data sources
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ Agent Selector  │ ← Selects optimal agent combination
└─────────────────┘
```

#### **2. Data Retrieval and Processing**
```
┌─────────────────┐
│   Data Source   │ ← CSV files, databases, APIs
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ Fast MCP Tools  │ ← Universal data access layer
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  Pandas Engine  │ ← Data processing and analysis
└─────────────────┘
```

#### **3. Agent Execution and Coordination**
```
┌─────────────────┐
│  Agent 1        │ ← Specialized analysis
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  Agent 2        │ ← Builds on Agent 1 results
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  Agent N        │ ← Final specialized analysis
└─────────────────┘
```

#### **4. Response Synthesis and Delivery**
```
┌─────────────────┐
│  Synthesis      │ ← Combines all agent outputs
│    Agent        │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  Output         │ ← Formatted response delivery
│  Formatter      │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  User Interface │ ← Dashboard, terminal, API
└─────────────────┘
```

## 🔌 Integration Patterns

### MCP Integration

#### **Fast MCP Tools**
The system uses FastMCP to create universal data access tools:

```python
# Example MCP tool for financial data
@mcp_tool
async def get_financial_data(
    statement_type: str,
    period: str,
    region: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve financial data from various statements.
    
    Args:
        statement_type: Type of statement (income, balance, cash_flow)
        period: Time period (Q1 2024, Jan 2025, etc.)
        region: Optional regional filter
        
    Returns:
        Dictionary containing financial data and metadata
    """
    # Implementation details...
```

#### **Data Source Connectors**
Each data source has a dedicated connector:

```python
class FinancialDataConnector:
    """Connector for financial data sources."""
    
    def __init__(self):
        self.income_statement = pd.read_csv("Income Statement.csv")
        self.balance_sheet = pd.read_csv("Balance Sheet.csv")
        self.cash_flow = pd.read_csv("Cash Flow.csv")
    
    async def get_revenue_data(self, period: str, region: str) -> Dict[str, Any]:
        """Retrieve revenue data for specific period and region."""
        # Implementation details...
```

### LangGraph Integration

#### **Workflow Definition**
Workflows are defined using LangGraph's declarative syntax:

```python
from langgraph import StateGraph, END

# Define workflow state
class WorkflowState(TypedDict):
    query: str
    selected_agents: List[str]
    agent_results: Dict[str, Any]
    final_response: str

# Create workflow
workflow = StateGraph(WorkflowState)

# Add nodes for each agent
workflow.add_node("operations_summary", operations_summary_agent)
workflow.add_node("upsell_discovery", upsell_discovery_agent)
workflow.add_node("financial_impact", financial_impact_agent)
workflow.add_node("campaign_planner", campaign_planner_agent)
workflow.add_node("synthesis", synthesis_agent)

# Define workflow edges
workflow.add_edge("operations_summary", "upsell_discovery")
workflow.add_edge("upsell_discovery", "financial_impact")
workflow.add_edge("financial_impact", "campaign_planner")
workflow.add_edge("campaign_planner", "synthesis")
workflow.add_edge("synthesis", END)

# Compile workflow
app = workflow.compile()
```

#### **Agent Coordination**
Agents coordinate through shared state and context:

```python
async def execute_workflow(query: str) -> Dict[str, Any]:
    """Execute the complete workflow for a given query."""
    
    # Initialize state
    initial_state = WorkflowState(
        query=query,
        selected_agents=[],
        agent_results={},
        final_response=""
    )
    
    # Execute workflow
    result = await app.ainvoke(initial_state)
    
    return result
```

## 🏛️ System Components

### Core Components

#### **1. Main Integration System**
- **File**: `main_integration_v2.py`
- **Purpose**: System entry point and coordination
- **Responsibilities**: Query processing, agent orchestration, response delivery

#### **2. O3 Orchestrator**
- **File**: `o3_orchestrator.py`
- **Purpose**: Dynamic agent selection and workflow generation
- **Responsibilities**: Query analysis, agent selection, workflow specification

#### **3. LangGraph Workflow Engine**
- **File**: `langgraph_workflow_v2.py`
- **Purpose**: Multi-agent workflow execution
- **Responsibilities**: Agent coordination, state management, error handling

#### **4. Fast MCP Connectors**
- **File**: `fast_mcp_connectors.py`
- **Purpose**: Data access and external system integration
- **Responsibilities**: Data retrieval, API integration, tool generation

#### **5. Agent Implementations**
- **File**: `claude_agents.py`
- **Purpose**: Specialized AI agent implementations
- **Responsibilities**: Domain-specific analysis, insight generation

### Supporting Components

#### **6. Performance Monitoring**
- **File**: `performance_dashboard.py`
- **Purpose**: System performance tracking and optimization
- **Responsibilities**: Metrics collection, performance analysis, optimization

#### **7. Evaluation System**
- **File**: `gpt5_evaluator_agent.py`
- **Purpose**: AI-powered system evaluation and quality assurance
- **Responsibilities**: Response evaluation, quality metrics, improvement recommendations

#### **8. Testing Framework**
- **File**: `comprehensive_emea_test.py`
- **Purpose**: End-to-end system testing and validation
- **Responsibilities**: Test execution, result validation, performance measurement

## 🔧 Configuration Management

### Environment Configuration

#### **Environment Variables**
The system uses environment variables for configuration:

```bash
# API Keys
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# System Configuration
LOG_LEVEL=INFO
MAX_CONCURRENT_QUERIES=10
ENABLE_STREAMLIT=true
ENABLE_PERFORMANCE_MONITORING=true

# Data Source Configuration
DATA_SOURCE_PATH=./data/
CACHE_ENABLED=true
CACHE_TTL=3600
```

#### **Configuration Files**
Configuration is managed through multiple files:

```python
# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    """System configuration settings."""
    
    # API Configuration
    openai_api_key: str
    anthropic_api_key: str
    
    # System Configuration
    log_level: str = "INFO"
    max_concurrent_queries: int = 10
    
    # Data Configuration
    data_source_path: str = "./data/"
    cache_enabled: bool = True
    cache_ttl: int = 3600
    
    class Config:
        env_file = ".env"
```

### Data Source Configuration

#### **CSV Data Sources**
Data sources are configured through file paths and schemas:

```python
DATA_SOURCES = {
    "income_statement": {
        "file": "Energy-&-Property-Tech-Inc_Sample_Data.xlsx - Income Statement.csv",
        "schema": {
            "date": "datetime64[ns]",
            "region": "category",
            "revenue": "float64",
            "cogs": "float64",
            "gross_profit": "float64"
        }
    },
    "balance_sheet": {
        "file": "Energy-&-Property-Tech-Inc_Sample_Data.xlsx - Balance Sheet.csv",
        "schema": {
            "date": "datetime64[ns]",
            "region": "category",
            "assets": "float64",
            "liabilities": "float64",
            "equity": "float64"
        }
    }
    # Additional data sources...
}
```

## 🚀 Deployment Architecture

### Development Environment

#### **Local Development**
```bash
# Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the system
python main_integration_v2.py
```

#### **Docker Development**
```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main_integration_v2.py"]
```

### Production Deployment

#### **Container Orchestration**
```yaml
# docker-compose.yml
version: '3.8'

services:
  ai-system:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
```

#### **Cloud Deployment**
The system is designed for cloud deployment with:
- **Horizontal Scaling**: Multiple instances for load balancing
- **Auto-scaling**: Automatic scaling based on demand
- **Load Balancing**: Distribution of queries across instances
- **Monitoring**: Cloud-native monitoring and alerting

## 🔒 Security and Privacy

### Security Measures

#### **API Key Management**
- **Environment Variables**: API keys stored in environment variables
- **Secure Storage**: No hardcoded credentials in source code
- **Access Control**: Limited access to production credentials

#### **Data Security**
- **Data Encryption**: All data encrypted in transit and at rest
- **Access Logging**: Comprehensive audit trail for all data access
- **Data Validation**: Input validation and sanitization

### Privacy Protection

#### **Data Handling**
- **Minimal Data**: Only necessary data is processed
- **Data Retention**: Configurable data retention policies
- **User Consent**: Clear data usage policies and consent mechanisms

## 📊 Performance Characteristics

### Response Time Targets

#### **Simple Queries**
- **Target**: <5 seconds
- **Typical**: 2-4 seconds
- **Components**: Single agent, basic data retrieval

#### **Complex Queries**
- **Target**: <30 seconds
- **Typical**: 15-25 seconds
- **Components**: Multiple agents, complex analysis, synthesis

### Scalability Metrics

#### **Concurrent Users**
- **Current**: 10+ concurrent users
- **Target**: 100+ concurrent users
- **Scaling**: Linear scaling with additional resources

#### **Query Throughput**
- **Current**: 100+ queries per hour
- **Target**: 1000+ queries per hour
- **Optimization**: Parallel processing, caching, resource optimization

## 🔮 Future Architecture Enhancements

### Planned Improvements

#### **1. Microservices Architecture**
- **Current**: Monolithic application
- **Future**: Microservices with API gateway
- **Benefits**: Independent scaling, technology diversity, team autonomy

#### **2. Event-Driven Architecture**
- **Current**: Request-response pattern
- **Future**: Event-driven with message queues
- **Benefits**: Asynchronous processing, better scalability, loose coupling

#### **3. Advanced Caching**
- **Current**: Basic in-memory caching
- **Future**: Redis-based distributed caching
- **Benefits**: Better performance, shared state, persistence

#### **4. Machine Learning Pipeline**
- **Current**: Rule-based agent selection
- **Future**: ML-powered agent selection and optimization
- **Benefits**: Adaptive behavior, continuous improvement, better performance

---

**Next**: [Agent System](./03-Agent-System.md) - Understanding the specialized AI agents and how they work
