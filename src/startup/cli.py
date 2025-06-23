"""
CLI interface for Startup AI Agent
"""

import asyncio
import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from .agent import StartupAIAgent

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Startup AI Agent - Comprehensive startup analysis using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  startup analyze "AI-powered fitness app for busy professionals"
  startup analyze --file startup_idea.txt
  startup pitch --analysis-id 0
  startup validate --business-model business_model.json
  startup export --analysis-id 0 --format markdown
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a startup idea")
    analyze_parser.add_argument("idea", nargs="?", help="Startup idea to analyze")
    analyze_parser.add_argument("--file", help="File containing startup idea")
    analyze_parser.add_argument("--output", help="Output file for results")
    analyze_parser.add_argument("--format", choices=["json", "markdown"], default="json", 
                               help="Output format")
    
    # Pitch command
    pitch_parser = subparsers.add_parser("pitch", help="Generate pitch deck")
    pitch_parser.add_argument("--analysis-id", type=int, default=-1, 
                             help="Analysis ID from history (default: latest)")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate business model")
    validate_parser.add_argument("--business-model", required=True, 
                                help="Business model JSON file")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export analysis")
    export_parser.add_argument("--analysis-id", type=int, default=-1, 
                              help="Analysis ID from history (default: latest)")
    export_parser.add_argument("--format", choices=["json", "markdown"], default="json",
                              help="Export format")
    export_parser.add_argument("--output", help="Output file")
    
    # History command
    history_parser = subparsers.add_parser("history", help="Show analysis history")
    
    # Interactive command
    interactive_parser = subparsers.add_parser("interactive", help="Start interactive mode")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Run the appropriate command
    asyncio.run(run_command(args))

async def run_command(args):
    """Execute the appropriate command"""
    agent = StartupAIAgent()
    
    try:
        if args.command == "analyze":
            await run_analyze(agent, args)
        elif args.command == "pitch":
            await run_pitch(agent, args)
        elif args.command == "validate":
            await run_validate(agent, args)
        elif args.command == "export":
            await run_export(agent, args)
        elif args.command == "history":
            await run_history(agent, args)
        elif args.command == "interactive":
            await run_interactive(agent)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

async def run_analyze(agent: StartupAIAgent, args):
    """Run startup analysis"""
    # Get startup idea
    startup_idea = args.idea
    if args.file:
        with open(args.file, 'r') as f:
            startup_idea = f.read().strip()
    
    if not startup_idea:
        print("❌ Please provide a startup idea or use --file option")
        return
    
    print(f"🚀 Analyzing startup idea: {startup_idea[:100]}...")
    
    # Run analysis
    analysis = await agent.analyze_startup_idea(startup_idea)
    
    # Output results
    if args.output:
        output_path = Path(args.output)
        content = agent.export_analysis(analysis, args.format)
        output_path.write_text(content)
        print(f"✅ Analysis saved to {output_path}")
    else:
        print("\n" + "="*50)
        print("📊 STARTUP ANALYSIS RESULTS")
        print("="*50)
        
        # Display key insights
        print(f"\n🎯 Market Research:")
        print(json.dumps(analysis.market_research, indent=2))
        
        print(f"\n👥 Customer Analysis:")
        print(json.dumps(analysis.customer_analysis, indent=2))
        
        print(f"\n💼 Business Model:")
        print(json.dumps(analysis.business_model, indent=2))
        
        print(f"\n🔧 Technical Feasibility:")
        print(json.dumps(analysis.technical_feasibility, indent=2))
        
        print(f"\n💰 Financial Projections:")
        print(json.dumps(analysis.financial_projections, indent=2))
        
        print(f"\n🚀 Go-to-Market Strategy:")
        print(json.dumps(analysis.go_to_market, indent=2))
        
        print(f"\n⚠️ Risk Assessment:")
        print(json.dumps(analysis.risk_assessment, indent=2))
        
        print(f"\n💡 Recommendations:")
        for i, rec in enumerate(analysis.recommendations, 1):
            print(f"{i}. {rec}")

async def run_pitch(agent: StartupAIAgent, args):
    """Generate pitch deck"""
    history = agent.get_analysis_history()
    
    if not history:
        print("❌ No analysis history found. Run 'analyze' first.")
        return
    
    analysis_id = args.analysis_id if args.analysis_id >= 0 else len(history) - 1
    
    if analysis_id >= len(history):
        print(f"❌ Analysis ID {analysis_id} not found. Available: 0-{len(history)-1}")
        return
    
    analysis = history[analysis_id]
    print(f"📊 Generating pitch deck for analysis {analysis_id}...")
    
    pitch_deck = await agent.generate_pitch_deck(analysis)
    
    if "error" in pitch_deck:
        print(f"❌ Error generating pitch deck: {pitch_deck['error']}")
        return
    
    print("\n" + "="*50)
    print("📋 PITCH DECK")
    print("="*50)
    print(pitch_deck["pitch_deck"])

async def run_validate(agent: StartupAIAgent, args):
    """Validate business model"""
    try:
        with open(args.business_model, 'r') as f:
            business_model = json.load(f)
    except Exception as e:
        print(f"❌ Error reading business model file: {e}")
        return
    
    print("🔍 Validating business model...")
    validation = await agent.validate_business_model(business_model)
    
    if "error" in validation:
        print(f"❌ Error validating business model: {validation['error']}")
        return
    
    print("\n" + "="*50)
    print("✅ BUSINESS MODEL VALIDATION")
    print("="*50)
    print(validation["validation"])

async def run_export(agent: StartupAIAgent, args):
    """Export analysis"""
    history = agent.get_analysis_history()
    
    if not history:
        print("❌ No analysis history found. Run 'analyze' first.")
        return
    
    analysis_id = args.analysis_id if args.analysis_id >= 0 else len(history) - 1
    
    if analysis_id >= len(history):
        print(f"❌ Analysis ID {analysis_id} not found. Available: 0-{len(history)-1}")
        return
    
    analysis = history[analysis_id]
    content = agent.export_analysis(analysis, args.format)
    
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(content)
        print(f"✅ Analysis exported to {output_path}")
    else:
        print(content)

async def run_history(agent: StartupAIAgent, args):
    """Show analysis history"""
    history = agent.get_analysis_history()
    
    if not history:
        print("📝 No analysis history found.")
        return
    
    print(f"📝 Analysis History ({len(history)} entries):")
    print("-" * 50)
    
    for i, analysis in enumerate(history):
        print(f"{i}: {analysis.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

async def run_interactive(agent: StartupAIAgent):
    """Run interactive mode"""
    print("🚀 Welcome to Startup AI Agent Interactive Mode!")
    print("Type 'help' for available commands, 'quit' to exit.")
    
    while True:
        try:
            command = input("\n🤖 startup-ai> ").strip().lower()
            
            if command in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            elif command == 'help':
                print_help()
            elif command == 'analyze':
                await interactive_analyze(agent)
            elif command == 'pitch':
                await interactive_pitch(agent)
            elif command == 'history':
                await run_history(agent, None)
            elif command == 'export':
                await interactive_export(agent)
            else:
                print("❌ Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def print_help():
    """Print interactive mode help"""
    print("""
Available commands:
  analyze  - Analyze a new startup idea
  pitch    - Generate pitch deck from latest analysis
  history  - Show analysis history
  export   - Export latest analysis
  help     - Show this help
  quit     - Exit interactive mode
    """)

async def interactive_analyze(agent: StartupAIAgent):
    """Interactive analysis"""
    print("✍️ Enter your startup idea (press Enter twice to finish):")
    
    lines = []
    while True:
        line = input()
        if line.strip() == "" and lines:
            break
        lines.append(line)
    
    startup_idea = "\n".join(lines).strip()
    
    if not startup_idea:
        print("❌ No startup idea provided.")
        return
    
    await run_analyze(agent, type('Args', (), {
        'idea': startup_idea,
        'file': None,
        'output': None,
        'format': 'json'
    })())

async def interactive_pitch(agent: StartupAIAgent):
    """Interactive pitch generation"""
    await run_pitch(agent, type('Args', (), {
        'analysis_id': -1
    })())

async def interactive_export(agent: StartupAIAgent):
    """Interactive export"""
    format_choice = input("Export format (json/markdown): ").strip().lower()
    if format_choice not in ['json', 'markdown']:
        format_choice = 'json'
    
    await run_export(agent, type('Args', (), {
        'analysis_id': -1,
        'format': format_choice,
        'output': None
    })()) 