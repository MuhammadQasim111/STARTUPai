"""
Basic tests for Startup AI Agent
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from startup.agent import StartupAIAgent, StartupAnalysis
from startup.utils import clean_text, extract_key_metrics


class TestStartupAIAgent:
    """Test cases for StartupAIAgent"""
    
    def test_agent_initialization(self):
        """Test that the agent can be initialized"""
        agent = StartupAIAgent()
        assert agent is not None
        assert hasattr(agent, 'client')
        assert hasattr(agent, 'gemini_model')
        assert hasattr(agent, 'analysis_history')
    
    def test_analysis_history(self):
        """Test analysis history functionality"""
        agent = StartupAIAgent()
        history = agent.get_analysis_history()
        assert isinstance(history, list)
        assert len(history) == 0  # Should be empty initially
    
    @pytest.mark.asyncio
    async def test_analyze_startup_idea_mock(self):
        """Test startup analysis with mocked APIs"""
        agent = StartupAIAgent()
        
        # Mock the API calls
        with patch.object(agent, '_analyze_with_openai') as mock_openai, \
             patch.object(agent, '_analyze_with_gemini') as mock_gemini, \
             patch.object(agent, '_combine_analysis_results') as mock_combine:
            
            # Setup mock returns
            mock_openai.return_value = {"analysis": "OpenAI analysis", "source": "OpenAI"}
            mock_gemini.return_value = {"analysis": "Gemini analysis", "source": "Gemini"}
            mock_combine.return_value = {
                "combined_analysis": "Combined analysis",
                "openai_insights": {"analysis": "OpenAI analysis"},
                "gemini_insights": {"analysis": "Gemini analysis"},
                "enhanced": True
            }
            
            # Test analysis
            startup_idea = "Test startup idea"
            analysis = await agent.analyze_startup_idea(startup_idea)
            
            # Verify the analysis object
            assert isinstance(analysis, StartupAnalysis)
            assert hasattr(analysis, 'market_research')
            assert hasattr(analysis, 'customer_analysis')
            assert hasattr(analysis, 'business_model')
            assert hasattr(analysis, 'technical_feasibility')
            assert hasattr(analysis, 'financial_projections')
            assert hasattr(analysis, 'go_to_market')
            assert hasattr(analysis, 'risk_assessment')
            assert hasattr(analysis, 'recommendations')
            assert hasattr(analysis, 'created_at')
            
            # Verify history was updated
            history = agent.get_analysis_history()
            assert len(history) == 1
            assert history[0] == analysis
    
    def test_export_analysis_json(self):
        """Test JSON export functionality"""
        agent = StartupAIAgent()
        
        # Create a mock analysis
        analysis = StartupAnalysis(
            market_research={"test": "data"},
            customer_analysis={"test": "data"},
            business_model={"test": "data"},
            technical_feasibility={"test": "data"},
            financial_projections={"test": "data"},
            go_to_market={"test": "data"},
            risk_assessment={"test": "data"},
            recommendations=["Test recommendation"]
        )
        
        # Test JSON export
        json_export = agent.export_analysis(analysis, "json")
        assert isinstance(json_export, str)
        assert "test" in json_export
        assert "data" in json_export
    
    def test_export_analysis_markdown(self):
        """Test Markdown export functionality"""
        agent = StartupAIAgent()
        
        # Create a mock analysis
        analysis = StartupAnalysis(
            market_research={"test": "data"},
            customer_analysis={"test": "data"},
            business_model={"test": "data"},
            technical_feasibility={"test": "data"},
            financial_projections={"test": "data"},
            go_to_market={"test": "data"},
            risk_assessment={"test": "data"},
            recommendations=["Test recommendation"]
        )
        
        # Test Markdown export
        markdown_export = agent.export_analysis(analysis, "markdown")
        assert isinstance(markdown_export, str)
        assert "# Startup Analysis Report" in markdown_export
        assert "Test recommendation" in markdown_export
    
    def test_export_analysis_invalid_format(self):
        """Test export with invalid format"""
        agent = StartupAIAgent()
        
        analysis = StartupAnalysis(
            market_research={},
            customer_analysis={},
            business_model={},
            technical_feasibility={},
            financial_projections={},
            go_to_market={},
            risk_assessment={},
            recommendations=[]
        )
        
        with pytest.raises(ValueError, match="Unsupported format"):
            agent.export_analysis(analysis, "invalid_format")


class TestUtils:
    """Test cases for utility functions"""
    
    def test_clean_text(self):
        """Test text cleaning functionality"""
        # Test normal text
        assert clean_text("  Hello   World  ") == "Hello World"
        
        # Test with special characters
        assert clean_text("Hello@World#123") == "HelloWorld123"
        
        # Test empty string
        assert clean_text("") == ""
        assert clean_text(None) == ""
    
    def test_extract_key_metrics(self):
        """Test key metrics extraction"""
        text = """
        The market size is $10 billion with low competition. 
        The feasibility score is 85% and it's a low risk investment.
        Projected revenue is $5 million in the first year.
        Time to market is 6 months.
        """
        
        metrics = extract_key_metrics(text)
        
        assert metrics["market_size"] == 10000000000  # $10 billion
        assert metrics["competition_level"] == "low"
        assert metrics["feasibility_score"] == 85
        assert metrics["risk_level"] == "low"
        assert metrics["estimated_revenue"] == 5000000  # $5 million
        assert metrics["time_to_market"] == 6  # 6 months
    
    def test_extract_key_metrics_no_matches(self):
        """Test key metrics extraction with no matches"""
        text = "This is a test text with no specific metrics."
        
        metrics = extract_key_metrics(text)
        
        # All metrics should be None when no matches found
        for value in metrics.values():
            assert value is None


if __name__ == "__main__":
    pytest.main([__file__]) 