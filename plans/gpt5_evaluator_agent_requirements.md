# GPT5 Evaluator Agent Requirements

## **Document Information**
- **Author**: Carlos Lozano
- **Date**: August 11, 2025
- **Phase**: 6 - Evaluation Phase
- **Purpose**: Define requirements for AI-powered evaluation of agent responses

---

## **Executive Summary**

The GPT5 Evaluator Agent is a critical component of Phase 6 that will provide comprehensive, objective assessment of all agent responses in the Energy Property AI System. This agent will act as an "AI judge" to evaluate the quality, accuracy, and effectiveness of responses from all specialized agents in the system.

---

## **Core Mission**

Create an intelligent evaluation system that can:
1. **Objectively assess** agent responses across multiple quality dimensions
2. **Provide quantitative scoring** (1-10 scale) for measurable comparison
3. **Deliver qualitative feedback** explaining scoring decisions
4. **Maintain consistency** in evaluation standards across all assessments
5. **Identify patterns** in agent performance and areas for improvement

---

## **Evaluation Framework**

### **Primary Evaluation Criteria**

#### **1. Factuality (1-4 Scale)**
- **1 - Very Poor**: Significant factual errors, hallucinations, incorrect data, no data source validation
- **2 - Poor**: Multiple factual inaccuracies, some hallucinations, limited data source validation
- **3 - Good**: Mostly accurate with minor factual issues, some data source validation
- **4 - Very Good**: Highly accurate, factually correct, well-grounded, comprehensive data source validation

#### **2. Instruction Following (1-4 Scale)**
- **1 - Very Poor**: Completely ignores or misinterprets instructions
- **2 - Poor**: Partially follows instructions but misses key requirements
- **3 - Good**: Follows most instructions with minor deviations
- **4 - Very Good**: Precisely follows all instructions and requirements

#### **3. Conciseness (1-4 Scale)**
- **1 - Very Poor**: Extremely verbose, repetitive, unfocused
- **2 - Poor**: Too wordy, some repetition, lacks focus
- **3 - Good**: Generally concise with minor verbosity
- **4 - Very Good**: Optimal length, focused, efficient communication

#### **4. Completeness (1-4 Scale)**
- **1 - Very Poor**: Missing critical information, incomplete answers
- **2 - Poor**: Missing important details, partial coverage
- **3 - Good**: Covers most requirements with minor gaps
- **4 - Very Good**: Comprehensive coverage of all requirements

#### **5. Data Source Validation (1-4 Scale)**
- **1 - Very Poor**: No reference to business data sources, pure speculation, hallucinations
- **2 - Poor**: Limited data source references, mostly generic statements
- **3 - Good**: Some specific data source references, partial grounding in business data
- **4 - Very Good**: Comprehensive data source validation, specific references to business data sources

### **Quantitative Assessment**
- **Scale**: 1-10 (whole numbers only)
- **Weighting**: 
  - Factuality: 30% (3.0 points max)
  - Instruction Following: 25% (2.5 points max)
  - Conciseness: 15% (1.5 points max)
  - Completeness: 15% (1.5 points max)
  - Data Source Validation: 15% (1.5 points max)

### **Qualitative Assessment**
- **Format**: Detailed explanation of scoring decisions
- **Content**: Specific examples of strengths and weaknesses
- **Actionable Feedback**: Suggestions for improvement
- **Context**: Consideration of query complexity and domain expertise

---

## **Technical Requirements**

### **AI Model**
- **Primary Model**: GPT-5 (OpenAI API)
- **Fallback Model**: GPT-5-mini (for cost optimization)
- **Model Parameters**:
  - Temperature: 0.1 (for consistent evaluation)
  - Max Tokens: 2000 (for detailed feedback)
  - Verbosity: Medium (balanced detail)

### **Input Processing**
- **Query Context**: Full user query and conversation context
- **Agent Response**: Complete response from evaluated agent
- **Data Sources**: Reference to business data used and validation of data source grounding
- **Agent Type**: Identification of agent specialization
- **Business Data Validation**: Verification that responses reference legitimate business data sources

### **Output Format**
- **Structured Table**: Consistent evaluation matrix
- **JSON Output**: Machine-readable evaluation data
- **Human Readable**: Clear, actionable feedback
- **Audit Trail**: Evaluation timestamp and criteria used

---

## **Evaluation Process**

### **Step 1: Context Analysis**
1. **Parse User Query**: Understand the business question/request
2. **Identify Agent Type**: Determine which specialized agent responded
3. **Extract Key Requirements**: Identify what the query was asking for
4. **Assess Complexity**: Evaluate the difficulty level of the request

### **Step 2: Response Assessment**
1. **Factuality Check**: Verify accuracy against business data
2. **Data Source Validation**: Verify responses reference legitimate business data sources
3. **Instruction Compliance**: Check adherence to query requirements
4. **Communication Quality**: Assess clarity and conciseness
5. **Completeness Review**: Verify all aspects were addressed

### **Step 3: Scoring and Feedback**
1. **Apply Scoring Rubric**: Use standardized evaluation criteria
2. **Calculate Quantitative Score**: Apply weighted scoring system
3. **Generate Qualitative Feedback**: Provide detailed assessment
4. **Identify Improvement Areas**: Suggest specific enhancements

---

## **Business Context Requirements**

### **Energy & Property Tech Domain Knowledge**
- **Financial Analysis**: Revenue, costs, profit margins, ROI
- **Operational Metrics**: Asset utilization, lead funnel, performance
- **Strategic Planning**: Upsell opportunities, market analysis, growth
- **Regional Focus**: EMEA, APAC, Americas market understanding

### **Data Source Familiarity**
- **Income Statement**: Monthly financial performance data
- **Balance Sheet**: Quarterly financial position data
- **Cash Flow**: Quarterly cash movement analysis
- **Installed Assets**: Customer installation and upsell data
- **Lead Funnel**: Sales pipeline and conversion metrics
- **Products**: Product catalog and market positioning

---

## **Quality Assurance Requirements**

### **Consistency Standards**
- **Inter-rater Reliability**: Consistent scoring across similar responses
- **Temporal Consistency**: Stable evaluation standards over time
- **Domain Consistency**: Uniform assessment across business areas
- **Complexity Adjustment**: Fair evaluation considering query difficulty

### **Bias Prevention**
- **Objective Criteria**: Evidence-based evaluation only
- **No Favoritism**: Equal treatment of all agent types
- **Context Awareness**: Consider environmental factors fairly
- **Transparency**: Clear explanation of all scoring decisions

---

## **Integration Requirements**

### **System Integration**
- **Agent Monitor**: Integrate with performance tracking system
- **Performance Dashboard**: Feed evaluation results to monitoring
- **Report Generation**: Create evaluation summaries and trends
- **Alert System**: Flag significant quality issues

### **Data Flow**
- **Input**: Agent responses and user queries
- **Processing**: GPT-5 evaluation engine
- **Output**: Structured evaluation results
- **Storage**: Evaluation history and trends
- **Reporting**: Performance analytics and insights

---

## **Success Metrics**

### **Evaluation Quality**
- **Accuracy**: Evaluator assessments align with human expert review
- **Consistency**: Stable scoring across similar scenarios
- **Completeness**: All evaluation criteria properly applied
- **Timeliness**: Evaluation completed within acceptable timeframe

### **Business Impact**
- **Agent Improvement**: Identified areas lead to better responses
- **Quality Monitoring**: Continuous quality assurance system
- **Performance Tracking**: Measurable agent performance metrics
- **Decision Support**: Data-driven agent optimization decisions

---

## **Implementation Phases**

### **Phase 6.1: Core Evaluator**
- Basic evaluation framework implementation
- GPT-5 integration and testing
- Core evaluation criteria validation
- Basic output format establishment

### **Phase 6.2: Advanced Features**
- Enhanced evaluation algorithms
- Pattern recognition and trend analysis
- Automated quality alerts
- Performance dashboard integration

### **Phase 6.3: Optimization**
- Evaluation accuracy improvements
- Cost optimization strategies
- Advanced analytics and reporting
- Full system integration

---

## **Risk Mitigation**

### **Technical Risks**
- **API Reliability**: Fallback models and error handling
- **Cost Management**: Token usage optimization and monitoring
- **Performance**: Response time optimization for real-time evaluation
- **Scalability**: Handle increasing evaluation volume

### **Quality Risks**
- **Evaluation Bias**: Regular bias assessment and correction
- **Inconsistent Standards**: Regular calibration and training
- **Context Misunderstanding**: Enhanced context parsing
- **Domain Knowledge Gaps**: Continuous learning and updates

---

## **Deliverables**

### **Phase 6.1 Deliverables**
1. **GPT5 Evaluator Agent**: Core evaluation engine
2. **Evaluation Framework**: Scoring system and criteria
3. **Basic Integration**: Connection to agent monitoring system
4. **Initial Testing**: Validation with sample agent responses

### **Phase 6.2 Deliverables**
1. **Advanced Analytics**: Pattern recognition and trend analysis
2. **Quality Dashboard**: Real-time evaluation monitoring
3. **Automated Alerts**: Quality issue detection and notification
4. **Performance Reports**: Comprehensive evaluation summaries

### **Phase 6.3 Deliverables**
1. **Full System Integration**: Complete evaluation ecosystem
2. **Optimization Reports**: Performance improvement recommendations
3. **Quality Metrics**: Long-term quality trend analysis
4. **Documentation**: Complete system documentation and user guides

---

## **Success Criteria**

### **Technical Success**
- ✅ GPT-5 integration working reliably
- ✅ Evaluation framework producing consistent results
- ✅ System integration with agent monitoring
- ✅ Performance meeting latency requirements

### **Quality Success**
- ✅ Evaluation accuracy validated against human experts
- ✅ Consistent scoring across different scenarios
- ✅ Actionable feedback leading to agent improvements
- ✅ Quality metrics showing measurable improvements

### **Business Success**
- ✅ Agent response quality improving over time
- ✅ Quality issues identified and addressed proactively
- ✅ Performance metrics supporting optimization decisions
- ✅ Evaluation system providing business value

---

## **Next Steps**

1. **Review Requirements**: Validate requirements with stakeholders
2. **Create System Prompt**: Develop GPT-5 system prompt
3. **Implement Core Engine**: Build basic evaluation framework
4. **Integration Testing**: Connect with existing agent system
5. **Validation**: Test with real agent responses
6. **Iteration**: Refine based on initial results

---

## **Contact**

For questions about these requirements or implementation details:
- **Documentation**: This requirements document
- **Code**: Implementation files in the project directory
- **Testing**: Evaluation framework and test results
- **Integration**: System integration and monitoring
