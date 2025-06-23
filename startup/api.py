"""
FastAPI backend for Startup AI Agent
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import asyncio
import json
from datetime import datetime
import uvicorn

from .agent import StartupAIAgent, StartupAnalysis

# Initialize FastAPI app
app = FastAPI(
    title="Startup AI Agent API",
    description="Comprehensive startup analysis using OpenAI Agents SDK and Gemini API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent
agent = StartupAIAgent()

# Pydantic models
class StartupIdeaRequest(BaseModel):
    idea: str = Field(..., description="Startup idea description", min_length=10)
    include_market_research: bool = Field(True, description="Include market research analysis")
    include_customer_analysis: bool = Field(True, description="Include customer analysis")
    include_business_model: bool = Field(True, description="Include business model analysis")
    include_technical_feasibility: bool = Field(True, description="Include technical feasibility analysis")
    include_financial_projections: bool = Field(True, description="Include financial projections")
    include_go_to_market: bool = Field(True, description="Include go-to-market strategy")
    include_risk_assessment: bool = Field(True, description="Include risk assessment")

class AnalysisResponse(BaseModel):
    analysis_id: int
    created_at: datetime
    market_research: Dict[str, Any]
    customer_analysis: Dict[str, Any]
    business_model: Dict[str, Any]
    technical_feasibility: Dict[str, Any]
    financial_projections: Dict[str, Any]
    go_to_market: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    recommendations: List[str]

class PitchDeckRequest(BaseModel):
    analysis_id: int = Field(..., description="Analysis ID to generate pitch deck for")

class PitchDeckResponse(BaseModel):
    analysis_id: int
    pitch_deck: str
    generated_at: datetime

class BusinessModelValidationRequest(BaseModel):
    business_model: Dict[str, Any] = Field(..., description="Business model to validate")

class ValidationResponse(BaseModel):
    validation: str
    validated_at: datetime

class ExportRequest(BaseModel):
    analysis_id: int = Field(..., description="Analysis ID to export")
    format: str = Field("json", description="Export format (json or markdown)")

# API Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Startup AI Agent API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agent_ready": True
    }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_startup_idea(request: StartupIdeaRequest, background_tasks: BackgroundTasks):
    """
    Analyze a startup idea comprehensively
    """
    try:
        # Run analysis
        analysis = await agent.analyze_startup_idea(request.idea)
        
        # Get analysis ID
        history = agent.get_analysis_history()
        analysis_id = len(history) - 1
        
        return AnalysisResponse(
            analysis_id=analysis_id,
            created_at=analysis.created_at,
            market_research=analysis.market_research,
            customer_analysis=analysis.customer_analysis,
            business_model=analysis.business_model,
            technical_feasibility=analysis.technical_feasibility,
            financial_projections=analysis.financial_projections,
            go_to_market=analysis.go_to_market,
            risk_assessment=analysis.risk_assessment,
            recommendations=analysis.recommendations
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/analyses", response_model=List[Dict[str, Any]])
async def get_analysis_history():
    """
    Get all analysis history
    """
    try:
        history = agent.get_analysis_history()
        return [
            {
                "analysis_id": i,
                "created_at": analysis.created_at.isoformat(),
                "summary": {
                    "market_research": bool(analysis.market_research),
                    "customer_analysis": bool(analysis.customer_analysis),
                    "business_model": bool(analysis.business_model),
                    "technical_feasibility": bool(analysis.technical_feasibility),
                    "financial_projections": bool(analysis.financial_projections),
                    "go_to_market": bool(analysis.go_to_market),
                    "risk_assessment": bool(analysis.risk_assessment)
                }
            }
            for i, analysis in enumerate(history)
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get history: {str(e)}")

@app.get("/analyses/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(analysis_id: int):
    """
    Get specific analysis by ID
    """
    try:
        history = agent.get_analysis_history()
        
        if analysis_id < 0 or analysis_id >= len(history):
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        analysis = history[analysis_id]
        
        return AnalysisResponse(
            analysis_id=analysis_id,
            created_at=analysis.created_at,
            market_research=analysis.market_research,
            customer_analysis=analysis.customer_analysis,
            business_model=analysis.business_model,
            technical_feasibility=analysis.technical_feasibility,
            financial_projections=analysis.financial_projections,
            go_to_market=analysis.go_to_market,
            risk_assessment=analysis.risk_assessment,
            recommendations=analysis.recommendations
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analysis: {str(e)}")

@app.post("/pitch-deck", response_model=PitchDeckResponse)
async def generate_pitch_deck(request: PitchDeckRequest):
    """
    Generate pitch deck for a specific analysis
    """
    try:
        history = agent.get_analysis_history()
        
        if request.analysis_id < 0 or request.analysis_id >= len(history):
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        analysis = history[request.analysis_id]
        pitch_deck = await agent.generate_pitch_deck(analysis)
        
        if "error" in pitch_deck:
            raise HTTPException(status_code=500, detail=f"Failed to generate pitch deck: {pitch_deck['error']}")
        
        return PitchDeckResponse(
            analysis_id=request.analysis_id,
            pitch_deck=pitch_deck["pitch_deck"],
            generated_at=datetime.fromisoformat(pitch_deck["generated_at"])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate pitch deck: {str(e)}")

@app.post("/validate-business-model", response_model=ValidationResponse)
async def validate_business_model(request: BusinessModelValidationRequest):
    """
    Validate a business model
    """
    try:
        validation = await agent.validate_business_model(request.business_model)
        
        if "error" in validation:
            raise HTTPException(status_code=500, detail=f"Validation failed: {validation['error']}")
        
        return ValidationResponse(
            validation=validation["validation"],
            validated_at=datetime.fromisoformat(validation["validated_at"])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to validate business model: {str(e)}")

@app.post("/export")
async def export_analysis(request: ExportRequest):
    """
    Export analysis in specified format
    """
    try:
        history = agent.get_analysis_history()
        
        if request.analysis_id < 0 or request.analysis_id >= len(history):
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        analysis = history[request.analysis_id]
        content = agent.export_analysis(analysis, request.format)
        
        return JSONResponse(
            content={
                "analysis_id": request.analysis_id,
                "format": request.format,
                "content": content,
                "exported_at": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export analysis: {str(e)}")

@app.delete("/analyses/{analysis_id}")
async def delete_analysis(analysis_id: int):
    """
    Delete a specific analysis (not implemented in current version)
    """
    raise HTTPException(status_code=501, detail="Delete functionality not implemented yet")

@app.get("/metrics")
async def get_metrics():
    """
    Get API usage metrics
    """
    try:
        history = agent.get_analysis_history()
        
        return {
            "total_analyses": len(history),
            "analyses_today": len([h for h in history if h.created_at.date() == datetime.now().date()]),
            "analyses_this_week": len([h for h in history if (datetime.now() - h.created_at).days <= 7]),
            "analyses_this_month": len([h for h in history if h.created_at.month == datetime.now().month]),
            "average_analysis_time": "~30 seconds",  # Placeholder
            "api_status": "healthy"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get metrics: {str(e)}")

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Resource not found", "detail": str(exc)}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup"""
    print("🚀 Startup AI Agent API starting...")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on shutdown"""
    print("👋 Startup AI Agent API shutting down...")

def run_api_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """Run the FastAPI server"""
    uvicorn.run(
        "startup.api:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    run_api_server() 