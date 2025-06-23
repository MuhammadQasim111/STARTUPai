# 🚀 Startup AI Agent

A comprehensive AI-powered startup analysis tool using **OpenAI Agents SDK** and **Gemini API** integration. Transform your startup ideas into actionable insights with advanced AI analysis.

## ✨ Features

- **🤖 Dual AI Analysis**: Leverages both OpenAI GPT-4 and Google Gemini for enhanced insights
- **📊 Comprehensive Analysis**: Market research, customer analysis, business model design, technical feasibility, financial projections, go-to-market strategy, and risk assessment
- **🎯 Multiple Interfaces**: CLI, Web UI (Streamlit), and REST API
- **📈 Data Visualization**: Interactive charts and graphs for better insights
- **💼 Pitch Deck Generation**: Automatically generate compelling pitch materials
- **📋 Business Model Validation**: Validate and improve your business model
- **📤 Export Capabilities**: Export results in JSON and Markdown formats
- **📚 Analysis History**: Track and compare multiple analyses

## 🛠️ Installation

### Prerequisites

- Python 3.11 or higher
- OpenAI API key
- Gemini API key

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd startup
   ```

2. **Install dependencies**
   ```bash
   pip install -e .
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Verify installation**
   ```bash
   startup --help
   ```

## 🚀 Quick Start

### Command Line Interface

```bash
# Analyze a startup idea
startup analyze "AI-powered fitness app for busy professionals"

# Interactive mode
startup interactive

# Generate pitch deck from latest analysis
startup pitch

# Export analysis
startup export --format markdown
```

### Web Interface

```bash
# Start Streamlit web app
streamlit run src/startup/web_app.py
```

### API Server

```bash
# Start FastAPI server
python -m startup.api
```

## 📖 Usage Examples

### 1. Basic Startup Analysis

```python
from startup import StartupAIAgent
import asyncio

async def analyze_startup():
    agent = StartupAIAgent()
    
    startup_idea = """
    An AI-powered platform that helps small businesses automate their 
    customer service using natural language processing and machine learning. 
    The platform integrates with existing CRM systems and provides 24/7 
    customer support through chatbots and email automation.
    """
    
    analysis = await agent.analyze_startup_idea(startup_idea)
    print(f"Analysis completed: {len(analysis.recommendations)} recommendations")
    
    # Generate pitch deck
    pitch_deck = await agent.generate_pitch_deck(analysis)
    print("Pitch deck generated successfully!")

# Run analysis
asyncio.run(analyze_startup())
```

### 2. Business Model Validation

```python
business_model = {
    "revenue_streams": [
        {"type": "subscription", "price": 99, "frequency": "monthly"},
        {"type": "enterprise", "price": 999, "frequency": "monthly"}
    ],
    "cost_structure": {
        "development": 50000,
        "marketing": 20000,
        "operations": 15000
    },
    "target_market": "Small businesses with 10-100 employees"
}

validation = await agent.validate_business_model(business_model)
print(validation["validation"])
```

### 3. Export Analysis

```python
# Export as JSON
json_export = agent.export_analysis(analysis, "json")

# Export as Markdown
markdown_export = agent.export_analysis(analysis, "markdown")

# Save to file
with open("startup_analysis.md", "w") as f:
    f.write(markdown_export)
```

## 🌐 Web Interface

The Streamlit web interface provides a user-friendly way to interact with the Startup AI Agent:

1. **Start the web app**: `streamlit run src/startup/web_app.py`
2. **Navigate to**: `http://localhost:8501`
3. **Enter your startup idea** in the text area
4. **Click "Analyze Startup Idea"** to begin analysis
5. **View results** in organized sections with interactive visualizations

### Web Interface Features

- 📊 **Interactive Dashboards**: Real-time charts and graphs
- 📋 **Organized Results**: Structured analysis sections
- 📈 **Visualizations**: Market analysis, revenue projections, risk matrices
- 💾 **Export Options**: Download results in multiple formats
- 📚 **History Tracking**: View and compare previous analyses

## 🔌 API Reference

### REST API Endpoints

Start the API server: `python -m startup.api`

#### Base URL: `http://localhost:8000`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/analyze` | POST | Analyze startup idea |
| `/analyses` | GET | Get analysis history |
| `/analyses/{id}` | GET | Get specific analysis |
| `/pitch-deck` | POST | Generate pitch deck |
| `/validate-business-model` | POST | Validate business model |
| `/export` | POST | Export analysis |
| `/metrics` | GET | API usage metrics |

### API Example

```python
import requests

# Analyze startup idea
response = requests.post("http://localhost:8000/analyze", json={
    "idea": "AI-powered customer service platform",
    "include_market_research": True,
    "include_customer_analysis": True,
    "include_business_model": True
})

analysis = response.json()
print(f"Analysis ID: {analysis['analysis_id']}")

# Generate pitch deck
pitch_response = requests.post("http://localhost:8000/pitch-deck", json={
    "analysis_id": analysis['analysis_id']
})

pitch_deck = pitch_response.json()
print(pitch_deck['pitch_deck'])
```

## 📊 Analysis Components

The Startup AI Agent provides comprehensive analysis across multiple dimensions:

### 1. Market Research
- Market size and growth potential
- Competitive landscape analysis
- Industry trends and opportunities
- Market segmentation

### 2. Customer Analysis
- Target customer identification
- Customer pain points and needs
- Customer journey mapping
- Value proposition development

### 3. Business Model
- Revenue stream identification
- Cost structure analysis
- Key partnerships and resources
- Value chain optimization

### 4. Technical Feasibility
- Technology requirements
- Development timeline
- Resource requirements
- Technical risks and mitigation

### 5. Financial Projections
- Revenue forecasting
- Cost projections
- Break-even analysis
- Funding requirements

### 6. Go-to-Market Strategy
- Market entry approach
- Marketing and sales strategy
- Distribution channels
- Launch timeline

### 7. Risk Assessment
- Market risks
- Technical risks
- Financial risks
- Competitive risks

## 🎯 Use Cases

- **Entrepreneurs**: Validate startup ideas before investing time and resources
- **Investors**: Evaluate startup opportunities and due diligence
- **Incubators/Accelerators**: Screen and mentor startup applications
- **Business Consultants**: Provide data-driven startup advice
- **Students**: Learn about startup analysis and business planning

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 access | Yes |
| `GEMINI_API_KEY` | Google Gemini API key | Yes |

### Customization

You can customize the analysis by modifying the agent configuration:

```python
# Custom analysis parameters
analysis_params = {
    "include_market_research": True,
    "include_customer_analysis": True,
    "include_business_model": True,
    "include_technical_feasibility": True,
    "include_financial_projections": True,
    "include_go_to_market": True,
    "include_risk_assessment": True
}
```

## 📈 Performance

- **Analysis Time**: ~30-60 seconds per analysis
- **Concurrent Users**: Supports multiple simultaneous analyses
- **API Rate Limits**: Respects OpenAI and Gemini API limits
- **Caching**: Results cached for improved performance

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Install development dependencies**: `pip install -e ".[dev]"`
4. **Make your changes**
5. **Run tests**: `pytest`
6. **Submit a pull request**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT-4 API
- Google for providing the Gemini API
- Streamlit for the web framework
- FastAPI for the REST API framework
- The open-source community for various dependencies

## 📞 Support

- **Documentation**: [Wiki](https://github.com/your-repo/wiki)
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Email**: support@startup-ai-agent.com

## 🔄 Changelog

### Version 1.0.0
- Initial release
- OpenAI Agents SDK integration
- Gemini API integration
- CLI, Web UI, and REST API interfaces
- Comprehensive startup analysis
- Pitch deck generation
- Business model validation

---

**Made with ❤️ for entrepreneurs and innovators**
