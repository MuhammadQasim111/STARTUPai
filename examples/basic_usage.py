#!/usr/bin/env python3
"""
Basic usage example for Startup AI Agent
"""

import asyncio
import json
from pathlib import Path
import sys

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from startup import StartupAIAgent

async def main():
    """Main example function"""
    print("🚀 Startup AI Agent - Basic Usage Example")
    print("=" * 50)
    
    # Initialize the agent
    agent = StartupAIAgent()
    
    # Example startup idea
    startup_idea = """
    An AI-powered platform that helps small businesses automate their customer service 
    using natural language processing and machine learning. The platform integrates with 
    existing CRM systems and provides 24/7 customer support through chatbots and email 
    automation. It helps reduce response times, improve customer satisfaction, and lower 
    operational costs for businesses.
    
    Target market: Small to medium businesses (10-500 employees) in e-commerce, 
    SaaS, and service industries who struggle with customer support scalability.
    
    Key features:
    - Intelligent chatbot with human-like responses
    - Email automation and categorization
    - CRM integration (Salesforce, HubSpot, etc.)
    - Analytics and performance tracking
    - Multi-language support
    - Customizable workflows
    """
    
    print(f"📝 Analyzing startup idea: {startup_idea[:100]}...")
    print()
    
    try:
        # Run comprehensive analysis
        print("🤖 Running AI analysis...")
        analysis = await agent.analyze_startup_idea(startup_idea)
        
        print("✅ Analysis completed successfully!")
        print(f"📊 Generated {len(analysis.recommendations)} recommendations")
        print()
        
        # Display key insights
        print("📋 KEY INSIGHTS")
        print("-" * 30)
        
        # Market Research
        if analysis.market_research:
            print("📈 Market Research:")
            if isinstance(analysis.market_research, dict):
                for key, value in list(analysis.market_research.items())[:3]:
                    print(f"  • {key}: {str(value)[:100]}...")
            else:
                print(f"  • {str(analysis.market_research)[:200]}...")
            print()
        
        # Customer Analysis
        if analysis.customer_analysis:
            print("👥 Customer Analysis:")
            if isinstance(analysis.customer_analysis, dict):
                for key, value in list(analysis.customer_analysis.items())[:3]:
                    print(f"  • {key}: {str(value)[:100]}...")
            else:
                print(f"  • {str(analysis.customer_analysis)[:200]}...")
            print()
        
        # Business Model
        if analysis.business_model:
            print("💼 Business Model:")
            if isinstance(analysis.business_model, dict):
                for key, value in list(analysis.business_model.items())[:3]:
                    print(f"  • {key}: {str(value)[:100]}...")
            else:
                print(f"  • {str(analysis.business_model)[:200]}...")
            print()
        
        # Recommendations
        print("💡 Top Recommendations:")
        for i, rec in enumerate(analysis.recommendations[:5], 1):
            print(f"  {i}. {rec}")
        print()
        
        # Generate pitch deck
        print("📋 Generating pitch deck...")
        pitch_deck = await agent.generate_pitch_deck(analysis)
        
        if "error" not in pitch_deck:
            print("✅ Pitch deck generated successfully!")
            print("📄 Pitch Deck Preview:")
            print("-" * 30)
            print(pitch_deck["pitch_deck"][:500] + "...")
            print()
        else:
            print(f"❌ Pitch deck generation failed: {pitch_deck['error']}")
        
        # Export analysis
        print("📤 Exporting analysis...")
        json_export = agent.export_analysis(analysis, "json")
        markdown_export = agent.export_analysis(analysis, "markdown")
        
        # Save to files
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        with open(output_dir / "startup_analysis.json", "w") as f:
            f.write(json_export)
        
        with open(output_dir / "startup_analysis.md", "w") as f:
            f.write(markdown_export)
        
        print(f"✅ Analysis exported to {output_dir}/")
        print()
        
        # Show analysis history
        history = agent.get_analysis_history()
        print(f"📚 Analysis History: {len(history)} analyses completed")
        
        print("\n🎉 Example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        print("\n💡 Make sure you have set up your API keys in the .env file:")
        print("   OPENAI_API_KEY=your_openai_api_key")
        print("   GEMINI_API_KEY=your_gemini_api_key")

if __name__ == "__main__":
    asyncio.run(main()) 