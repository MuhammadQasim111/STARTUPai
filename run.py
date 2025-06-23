#!/usr/bin/env python3
"""
Startup AI Agent Launcher
"""

import sys
import argparse
from pathlib import Path

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(
        description="Startup AI Agent Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py web          # Start web interface
  python run.py api          # Start API server
  python run.py cli          # Start CLI interface
  python run.py example      # Run example analysis
        """
    )
    
    parser.add_argument(
        "mode",
        choices=["web", "api", "cli", "example"],
        help="Mode to run the startup AI agent"
    )
    
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host for web/API server (default: localhost)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port for web/API server (auto-assigned if not specified)"
    )
    
    args = parser.parse_args()
    
    # Add src to path
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))
    
    try:
        if args.mode == "web":
            run_web_interface(args.host, args.port)
        elif args.mode == "api":
            run_api_server(args.host, args.port)
        elif args.mode == "cli":
            run_cli_interface()
        elif args.mode == "example":
            run_example()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def run_web_interface(host, port):
    """Run Streamlit web interface"""
    import subprocess
    import sys
    
    print("🌐 Starting Startup AI Agent Web Interface...")
    print(f"📍 URL: http://{host}:{port or 8501}")
    print("🔄 Press Ctrl+C to stop")
    
    cmd = [sys.executable, "-m", "streamlit", "run", "src/startup/web_app.py"]
    if host != "localhost":
        cmd.extend(["--server.address", host])
    if port:
        cmd.extend(["--server.port", str(port)])
    
    subprocess.run(cmd)

def run_api_server(host, port):
    """Run FastAPI server"""
    import subprocess
    import sys
    
    print("🔌 Starting Startup AI Agent API Server...")
    print(f"📍 URL: http://{host}:{port or 8000}")
    print("📚 API Docs: http://{host}:{port or 8000}/docs")
    print("🔄 Press Ctrl+C to stop")
    
    cmd = [sys.executable, "-m", "uvicorn", "startup.api:app"]
    if host != "localhost":
        cmd.extend(["--host", host])
    if port:
        cmd.extend(["--port", str(port)])
    else:
        cmd.extend(["--port", "8000"])
    
    subprocess.run(cmd)

def run_cli_interface():
    """Run CLI interface"""
    from startup.cli import main as cli_main
    
    print("💻 Starting Startup AI Agent CLI...")
    cli_main()

def run_example():
    """Run example analysis"""
    import asyncio
    from startup import StartupAIAgent
    
    print("🚀 Running Startup AI Agent Example...")
    
    async def run_example_analysis():
        agent = StartupAIAgent()
        
        startup_idea = """
        An AI-powered platform that helps small businesses automate their customer service 
        using natural language processing and machine learning. The platform integrates with 
        existing CRM systems and provides 24/7 customer support through chatbots and email 
        automation.
        """
        
        print("📝 Analyzing startup idea...")
        analysis = await agent.analyze_startup_idea(startup_idea)
        
        print("✅ Analysis completed!")
        print(f"📊 Generated {len(analysis.recommendations)} recommendations")
        
        # Show first few recommendations
        print("\n💡 Top Recommendations:")
        for i, rec in enumerate(analysis.recommendations[:3], 1):
            print(f"  {i}. {rec}")
        
        print("\n🎉 Example completed successfully!")
    
    asyncio.run(run_example_analysis())

if __name__ == "__main__":
    main() 