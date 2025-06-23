# 🚀 Quick Start Guide

Get your Startup AI Agent up and running in 5 minutes!

## ⚡ Quick Setup

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### 2. Set Up API Keys

1. **Get OpenAI API Key**:
   - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create a new API key
   - Copy the key

2. **Get Gemini API Key**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key

3. **Create .env file**:
   ```bash
   cp config.example.env .env
   ```

4. **Edit .env file**:
   ```env
   OPENAI_API_KEY=sk-your-openai-key-here
   GEMINI_API_KEY=your-gemini-key-here
   ```

### 3. Test Installation

```bash
# Run the example
python run.py example
```

You should see output like:
```
🚀 Running Startup AI Agent Example...
📝 Analyzing startup idea...
✅ Analysis completed!
📊 Generated 5 recommendations
💡 Top Recommendations:
  1. Conduct detailed market research...
  2. Develop MVP prototype...
  3. Create financial model...
🎉 Example completed successfully!
```

## 🎯 Usage Options

### Option 1: Web Interface (Recommended for beginners)

```bash
python run.py web
```

Then open your browser to `http://localhost:8501`

### Option 2: Command Line Interface

```bash
python run.py cli
```

Or use the direct command:
```bash
startup analyze "Your startup idea here"
```

### Option 3: API Server

```bash
python run.py api
```

Then visit `http://localhost:8000/docs` for API documentation

## 📝 Your First Analysis

### Using the Web Interface

1. **Start the web app**: `python run.py web`
2. **Enter your startup idea** in the text area
3. **Click "Analyze Startup Idea"**
4. **Wait 30-60 seconds** for AI analysis
5. **Review results** in organized sections
6. **Export** your analysis as JSON or Markdown

### Using Python Code

```python
import asyncio
from startup import StartupAIAgent

async def analyze_my_startup():
    agent = StartupAIAgent()
    
    startup_idea = """
    My startup idea: [Describe your idea here]
    Target market: [Who are your customers?]
    Key features: [What does your product do?]
    """
    
    analysis = await agent.analyze_startup_idea(startup_idea)
    
    print(f"Analysis completed with {len(analysis.recommendations)} recommendations")
    
    # Generate pitch deck
    pitch_deck = await agent.generate_pitch_deck(analysis)
    print("Pitch deck generated!")

# Run the analysis
asyncio.run(analyze_my_startup())
```

## 🔧 Troubleshooting

### Common Issues

1. **"API key not found" error**:
   - Make sure your `.env` file exists and has the correct API keys
   - Check that the keys are valid and have sufficient credits

2. **"Module not found" error**:
   - Install dependencies: `pip install -r requirements.txt`
   - Or install in development mode: `pip install -e .`

3. **"Analysis failed" error**:
   - Check your internet connection
   - Verify API keys are working
   - Try with a shorter startup idea description

4. **Web interface not loading**:
   - Make sure port 8501 is available
   - Try: `python run.py web --port 8502`

### Getting Help

- **Check the logs** for detailed error messages
- **Verify API keys** are working with a simple test
- **Try the example** first: `python run.py example`
- **Check the full documentation** in `README.md`

## 🎉 Next Steps

Once you're up and running:

1. **Try different startup ideas** to see how the analysis varies
2. **Explore the web interface** features like history and export
3. **Use the API** to integrate with your own applications
4. **Generate pitch decks** for your startup ideas
5. **Validate business models** using the validation feature

## 📚 Learn More

- **Full Documentation**: See `README.md` for complete feature list
- **API Reference**: Visit `http://localhost:8000/docs` when running the API
- **Examples**: Check the `examples/` directory for more use cases
- **Configuration**: See `config.example.env` for all available options

---

**Happy analyzing! 🚀** 