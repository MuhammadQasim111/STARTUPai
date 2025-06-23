"""
Startup AI Agent using Gemini API only
"""

import os
import asyncio
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

import google.generativeai as genai
from dotenv import load_dotenv
from pydantic import Field

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel('gemini-2.0-flash')

@dataclass
class StartupAnalysis:
    """Data structure for startup analysis results"""
    market_research: Dict[str, Any]
    customer_analysis: Dict[str, Any]
    business_model: Dict[str, Any]
    technical_feasibility: Dict[str, Any]
    financial_projections: Dict[str, Any]
    go_to_market: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    recommendations: List[str]
    created_at: datetime = field(default_factory=datetime.now)

class StartupAIAgent:
    """
    AI Agent for comprehensive startup analysis using Gemini API only
    """
    
    def __init__(self):
        self.gemini_model = gemini_model
        self.analysis_history = []
        
    async def analyze_startup_idea(self, startup_idea: str) -> StartupAnalysis:
        """
        Perform comprehensive startup analysis using Gemini
        """
        print("🚀 Starting comprehensive startup analysis...")
        
        # Create analysis tasks
        tasks = [
            ("market_research", "Analyze market size, trends, and competitive landscape"),
            ("customer_analysis", "Define target customers and their pain points"),
            ("business_model", "Design comprehensive business model and revenue streams"),
            ("technical_feasibility", "Evaluate technical requirements and feasibility"),
            ("financial_projections", "Create financial projections and funding requirements"),
            ("go_to_market", "Develop go-to-market strategy and launch plan"),
            ("risk_assessment", "Identify potential risks and mitigation strategies"),
            ("recommendations", "Provide actionable recommendations and next steps")
        ]
        
        results = {}
        
        for task_name, task_description in tasks:
            print(f"📊 Processing: {task_description}")
            gemini_result = await self._analyze_with_gemini(startup_idea, task_description)
            results[task_name] = gemini_result
        
        # Create comprehensive analysis
        analysis = StartupAnalysis(
            market_research=results["market_research"],
            customer_analysis=results["customer_analysis"],
            business_model=results["business_model"],
            technical_feasibility=results["technical_feasibility"],
            financial_projections=results["financial_projections"],
            go_to_market=results["go_to_market"],
            risk_assessment=results["risk_assessment"],
            recommendations=results["recommendations"] if isinstance(results["recommendations"], list) else [str(results["recommendations"])]
        )
        
        self.analysis_history.append(analysis)
        return analysis
    
    async def _analyze_with_gemini(self, startup_idea: str, task: str) -> Dict[str, Any]:
        """Analyze using Gemini API"""
        try:
            prompt = f"""
            As an expert startup analyst, provide detailed analysis for: {task}
            
            Startup Idea: {startup_idea}
            
            Please provide your analysis in a structured format with clear sections and actionable insights.
            """
            
            response = await asyncio.to_thread(
                self.gemini_model.generate_content,
                prompt
            )
            
            return {
                "analysis": response.text,
                "source": "Gemini"
            }
            
        except Exception as e:
            print(f"Gemini analysis error: {e}")
            return {"error": str(e), "source": "Gemini"}
    
    async def generate_pitch_deck(self, analysis: StartupAnalysis) -> Dict[str, Any]:
        """Generate pitch deck content based on analysis"""
        pitch_prompt = f"""
        Based on the following startup analysis, create a compelling pitch deck structure:
        
        {json.dumps(analysis.__dict__, indent=2, default=str)}
        
        Include:
        1. Problem Statement
        2. Solution Overview
        3. Market Opportunity
        4. Business Model
        5. Competitive Advantage
        6. Financial Projections
        7. Go-to-Market Strategy
        8. Team & Execution Plan
        9. Funding Requirements
        10. Call to Action
        """
        
        try:
            response = await asyncio.to_thread(
                self.gemini_model.generate_content,
                pitch_prompt
            )
            
            return {
                "pitch_deck": response.text,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    async def validate_business_model(self, business_model: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and improve business model"""
        validation_prompt = f"""
        Validate and improve this business model:
        
        {json.dumps(business_model, indent=2)}
        
        Provide:
        1. Strengths and weaknesses
        2. Potential improvements
        3. Risk factors
        4. Scalability assessment
        5. Revenue optimization suggestions
        """
        
        try:
            response = await asyncio.to_thread(
                self.gemini_model.generate_content,
                validation_prompt
            )
            
            return {
                "validation": response.text,
                "validated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def get_analysis_history(self) -> List[StartupAnalysis]:
        """Get analysis history"""
        return self.analysis_history
    
    def export_analysis(self, analysis: StartupAnalysis, format: str = "json") -> str:
        """Export analysis in specified format"""
        if format.lower() == "json":
            return json.dumps(analysis.__dict__, indent=2, default=str)
        elif format.lower() == "markdown":
            return self._convert_to_markdown(analysis)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _convert_to_markdown(self, analysis: StartupAnalysis) -> str:
        """Convert analysis to markdown format"""
        md_content = f"""# Startup Analysis Report
Generated on: {analysis.created_at}

## Market Research
{json.dumps(analysis.market_research, indent=2)}

## Customer Analysis
{json.dumps(analysis.customer_analysis, indent=2)}

## Business Model
{json.dumps(analysis.business_model, indent=2)}

## Technical Feasibility
{json.dumps(analysis.technical_feasibility, indent=2)}

## Financial Projections
{json.dumps(analysis.financial_projections, indent=2)}

## Go-to-Market Strategy
{json.dumps(analysis.go_to_market, indent=2)}

## Risk Assessment
{json.dumps(analysis.risk_assessment, indent=2)}

## Recommendations
{chr(10).join(f"- {rec}" for rec in analysis.recommendations)}
"""
        return md_content 