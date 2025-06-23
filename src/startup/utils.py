"""
Utility functions for Startup AI Agent
"""

import json
import re
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\-\:\;\(\)]', '', text)
    
    return text

def extract_key_metrics(text: str) -> Dict[str, Any]:
    """Extract key metrics from analysis text"""
    metrics = {
        "market_size": None,
        "competition_level": None,
        "feasibility_score": None,
        "risk_level": None,
        "estimated_revenue": None,
        "time_to_market": None
    }
    
    # Extract market size
    market_patterns = [
        r'market size[:\s]*\$?([\d,]+\.?\d*)\s*(billion|million|thousand|trillion)',
        r'\$?([\d,]+\.?\d*)\s*(billion|million|thousand|trillion)\s*market',
        r'market.*\$?([\d,]+\.?\d*)\s*(billion|million|thousand|trillion)'
    ]
    
    for pattern in market_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = float(match.group(1).replace(',', ''))
            unit = match.group(2).lower()
            if unit == 'billion':
                metrics["market_size"] = value * 1e9
            elif unit == 'million':
                metrics["market_size"] = value * 1e6
            elif unit == 'thousand':
                metrics["market_size"] = value * 1e3
            elif unit == 'trillion':
                metrics["market_size"] = value * 1e12
            break
    
    # Extract competition level
    competition_keywords = {
        "low": ["low competition", "few competitors", "niche market", "blue ocean"],
        "medium": ["moderate competition", "some competitors", "competitive market"],
        "high": ["high competition", "many competitors", "saturated market", "red ocean"]
    }
    
    for level, keywords in competition_keywords.items():
        if any(keyword in text.lower() for keyword in keywords):
            metrics["competition_level"] = level
            break
    
    # Extract feasibility score (0-100)
    feasibility_patterns = [
        r'feasibility.*?(\d{1,2})%',
        r'(\d{1,2})%.*?feasibility',
        r'feasibility.*?(\d{1,2})\s*out\s*of\s*100'
    ]
    
    for pattern in feasibility_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            metrics["feasibility_score"] = int(match.group(1))
            break
    
    # Extract risk level
    risk_keywords = {
        "low": ["low risk", "minimal risk", "safe investment"],
        "medium": ["medium risk", "moderate risk", "balanced risk"],
        "high": ["high risk", "significant risk", "risky venture"]
    }
    
    for level, keywords in risk_keywords.items():
        if any(keyword in text.lower() for keyword in keywords):
            metrics["risk_level"] = level
            break
    
    # Extract estimated revenue
    revenue_patterns = [
        r'revenue.*?\$?([\d,]+\.?\d*)\s*(billion|million|thousand)',
        r'\$?([\d,]+\.?\d*)\s*(billion|million|thousand).*?revenue',
        r'projected.*?\$?([\d,]+\.?\d*)\s*(billion|million|thousand)'
    ]
    
    for pattern in revenue_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = float(match.group(1).replace(',', ''))
            unit = match.group(2).lower()
            if unit == 'billion':
                metrics["estimated_revenue"] = value * 1e9
            elif unit == 'million':
                metrics["estimated_revenue"] = value * 1e6
            elif unit == 'thousand':
                metrics["estimated_revenue"] = value * 1e3
            break
    
    # Extract time to market
    time_patterns = [
        r'(\d+)\s*(months?|years?)\s*to\s*market',
        r'time\s*to\s*market.*?(\d+)\s*(months?|years?)',
        r'launch.*?(\d+)\s*(months?|years?)'
    ]
    
    for pattern in time_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = int(match.group(1))
            unit = match.group(2).lower()
            if unit in ['month', 'months']:
                metrics["time_to_market"] = value
            elif unit in ['year', 'years']:
                metrics["time_to_market"] = value * 12
            break
    
    return metrics

def create_market_visualization(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create market analysis visualizations"""
    visualizations = {}
    
    # Market size pie chart data
    market_segments = ['Direct Competitors', 'Indirect Competitors', 'Potential Partners', 'New Entrants']
    market_shares = [30, 25, 35, 10]  # Example data
    
    fig_pie = px.pie(
        values=market_shares,
        names=market_segments,
        title='Market Landscape Distribution'
    )
    visualizations['market_landscape'] = fig_pie.to_json()
    
    # Revenue projection line chart
    years = list(range(1, 6))
    revenue_data = [0.5, 2.5, 8.0, 15.0, 25.0]  # Example data in millions
    
    fig_line = px.line(
        x=years,
        y=revenue_data,
        title='5-Year Revenue Projection',
        labels={'x': 'Year', 'y': 'Revenue ($M)'}
    )
    visualizations['revenue_projection'] = fig_line.to_json()
    
    # Risk matrix scatter plot
    risk_categories = ['Market Risk', 'Technical Risk', 'Financial Risk', 'Competitive Risk']
    probabilities = [0.3, 0.2, 0.4, 0.5]
    impacts = [0.7, 0.6, 0.8, 0.6]
    
    fig_scatter = px.scatter(
        x=probabilities,
        y=impacts,
        size=probabilities,
        color=risk_categories,
        title='Risk Assessment Matrix',
        labels={'x': 'Probability', 'y': 'Impact'}
    )
    visualizations['risk_matrix'] = fig_scatter.to_json()
    
    return visualizations

def generate_financial_model(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate financial model based on analysis"""
    
    # Extract key metrics
    metrics = extract_key_metrics(str(analysis_data))
    
    # Base assumptions
    base_revenue = metrics.get("estimated_revenue", 1000000)  # Default $1M
    market_size = metrics.get("market_size", 10000000)  # Default $10M
    
    # Calculate market share (assume 1-5% of market)
    market_share = min(0.05, max(0.01, base_revenue / market_size))
    
    # Generate 5-year projections
    years = list(range(1, 6))
    revenue_growth_rates = [0.5, 1.5, 1.2, 0.8, 0.6]  # Year-over-year growth
    
    financial_model = {
        "assumptions": {
            "market_size": market_size,
            "target_market_share": market_share,
            "initial_revenue": base_revenue,
            "cost_of_goods_sold": 0.3,  # 30% of revenue
            "operating_expenses": 0.4,   # 40% of revenue
            "tax_rate": 0.25,            # 25% tax rate
        },
        "projections": {
            "years": years,
            "revenue": [],
            "cost_of_goods_sold": [],
            "gross_profit": [],
            "operating_expenses": [],
            "operating_income": [],
            "taxes": [],
            "net_income": [],
            "cumulative_cash_flow": []
        }
    }
    
    # Calculate projections
    current_revenue = base_revenue
    cumulative_cash_flow = 0
    
    for i, growth_rate in enumerate(revenue_growth_rates):
        if i == 0:
            revenue = current_revenue
        else:
            revenue = current_revenue * (1 + growth_rate)
        
        cogs = revenue * financial_model["assumptions"]["cost_of_goods_sold"]
        gross_profit = revenue - cogs
        operating_expenses = revenue * financial_model["assumptions"]["operating_expenses"]
        operating_income = gross_profit - operating_expenses
        taxes = max(0, operating_income * financial_model["assumptions"]["tax_rate"])
        net_income = operating_income - taxes
        
        cumulative_cash_flow += net_income
        
        financial_model["projections"]["revenue"].append(revenue)
        financial_model["projections"]["cost_of_goods_sold"].append(cogs)
        financial_model["projections"]["gross_profit"].append(gross_profit)
        financial_model["projections"]["operating_expenses"].append(operating_expenses)
        financial_model["projections"]["operating_income"].append(operating_income)
        financial_model["projections"]["taxes"].append(taxes)
        financial_model["projections"]["net_income"].append(net_income)
        financial_model["projections"]["cumulative_cash_flow"].append(cumulative_cash_flow)
        
        current_revenue = revenue
    
    return financial_model

def create_competitor_analysis(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create competitor analysis matrix"""
    
    # Example competitor data (in real app, this would be extracted from analysis)
    competitors = [
        {
            "name": "Competitor A",
            "market_share": 25,
            "strengths": ["Strong brand", "Large user base", "Deep pockets"],
            "weaknesses": ["Slow innovation", "Poor UX", "High costs"],
            "threat_level": "High"
        },
        {
            "name": "Competitor B",
            "market_share": 15,
            "strengths": ["Innovative features", "Agile development"],
            "weaknesses": ["Small team", "Limited funding"],
            "threat_level": "Medium"
        },
        {
            "name": "Competitor C",
            "market_share": 10,
            "strengths": ["Niche focus", "Customer loyalty"],
            "weaknesses": ["Limited scale", "Geographic constraints"],
            "threat_level": "Low"
        }
    ]
    
    return {
        "competitors": competitors,
        "total_market_share_covered": sum(c["market_share"] for c in competitors),
        "opportunity_market_share": 100 - sum(c["market_share"] for c in competitors),
        "analysis_date": datetime.now().isoformat()
    }

def generate_swot_analysis(analysis_data: Dict[str, Any]) -> Dict[str, List[str]]:
    """Generate SWOT analysis from startup analysis"""
    
    # Extract SWOT elements from analysis text
    analysis_text = str(analysis_data).lower()
    
    swot = {
        "strengths": [],
        "weaknesses": [],
        "opportunities": [],
        "threats": []
    }
    
    # Strengths
    strength_keywords = [
        "unique", "innovative", "competitive advantage", "strong team",
        "proven technology", "market demand", "scalable", "profitable"
    ]
    
    for keyword in strength_keywords:
        if keyword in analysis_text:
            swot["strengths"].append(f"Strong {keyword.replace('_', ' ')}")
    
    # Weaknesses
    weakness_keywords = [
        "limited", "small", "unproven", "risky", "expensive",
        "complex", "difficult", "challenging", "uncertain"
    ]
    
    for keyword in weakness_keywords:
        if keyword in analysis_text:
            swot["weaknesses"].append(f"Potential {keyword} challenges")
    
    # Opportunities
    opportunity_keywords = [
        "growing market", "increasing demand", "market expansion",
        "new technology", "partnership", "acquisition", "funding"
    ]
    
    for keyword in opportunity_keywords:
        if keyword in analysis_text:
            swot["opportunities"].append(f"Market {keyword}")
    
    # Threats
    threat_keywords = [
        "competition", "market saturation", "regulation", "economic",
        "technology change", "customer churn", "funding risk"
    ]
    
    for keyword in threat_keywords:
        if keyword in analysis_text:
            swot["threats"].append(f"Potential {keyword} threats")
    
    # Add default items if none found
    if not swot["strengths"]:
        swot["strengths"] = ["Innovative solution", "Market opportunity", "Scalable business model"]
    
    if not swot["weaknesses"]:
        swot["weaknesses"] = ["New market entrant", "Limited resources", "Unproven concept"]
    
    if not swot["opportunities"]:
        swot["opportunities"] = ["Market growth", "Technology advancement", "Partnership potential"]
    
    if not swot["threats"]:
        swot["threats"] = ["Competition", "Market changes", "Economic factors"]
    
    return swot

def create_action_plan(analysis_data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    """Create actionable plan from analysis"""
    
    action_plan = {
        "immediate_actions": [],
        "short_term_goals": [],
        "medium_term_goals": [],
        "long_term_goals": []
    }
    
    # Immediate actions (0-3 months)
    action_plan["immediate_actions"] = [
        {
            "action": "Conduct detailed market research",
            "timeline": "1-2 months",
            "priority": "High",
            "resources_needed": ["Market research tools", "Industry contacts"],
            "success_metrics": ["Market size validation", "Customer interviews completed"]
        },
        {
            "action": "Develop MVP prototype",
            "timeline": "2-3 months",
            "priority": "High",
            "resources_needed": ["Development team", "Design resources"],
            "success_metrics": ["Working prototype", "User feedback collected"]
        },
        {
            "action": "Create financial model",
            "timeline": "1 month",
            "priority": "Medium",
            "resources_needed": ["Financial expertise", "Market data"],
            "success_metrics": ["5-year projections", "Break-even analysis"]
        }
    ]
    
    # Short-term goals (3-6 months)
    action_plan["short_term_goals"] = [
        {
            "goal": "Launch beta version",
            "timeline": "3-6 months",
            "priority": "High",
            "dependencies": ["MVP completed", "Initial funding secured"],
            "success_metrics": ["Beta users acquired", "Product-market fit validation"]
        },
        {
            "goal": "Secure initial funding",
            "timeline": "3-4 months",
            "priority": "High",
            "dependencies": ["Financial model", "Pitch deck"],
            "success_metrics": ["Funding secured", "Investor commitments"]
        }
    ]
    
    # Medium-term goals (6-18 months)
    action_plan["medium_term_goals"] = [
        {
            "goal": "Achieve product-market fit",
            "timeline": "6-12 months",
            "priority": "High",
            "dependencies": ["Beta launch", "User feedback"],
            "success_metrics": ["User retention rate", "Customer satisfaction"]
        },
        {
            "goal": "Scale operations",
            "timeline": "12-18 months",
            "priority": "Medium",
            "dependencies": ["Product-market fit", "Additional funding"],
            "success_metrics": ["Revenue growth", "Team expansion"]
        }
    ]
    
    # Long-term goals (18+ months)
    action_plan["long_term_goals"] = [
        {
            "goal": "Market leadership",
            "timeline": "18-36 months",
            "priority": "Medium",
            "dependencies": ["Scaled operations", "Market expansion"],
            "success_metrics": ["Market share", "Brand recognition"]
        },
        {
            "goal": "Exit strategy",
            "timeline": "36+ months",
            "priority": "Low",
            "dependencies": ["Market leadership", "Financial performance"],
            "success_metrics": ["Valuation", "Exit options"]
        }
    ]
    
    return action_plan

def save_analysis_report(analysis_data: Dict[str, Any], filename: str, format: str = "json"):
    """Save analysis report to file"""
    
    output_path = Path(filename)
    
    if format.lower() == "json":
        with open(output_path, 'w') as f:
            json.dump(analysis_data, f, indent=2, default=str)
    elif format.lower() == "markdown":
        markdown_content = convert_to_markdown(analysis_data)
        with open(output_path, 'w') as f:
            f.write(markdown_content)
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    return output_path

def convert_to_markdown(analysis_data: Dict[str, Any]) -> str:
    """Convert analysis data to markdown format"""
    
    markdown = f"""# Startup Analysis Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
This comprehensive analysis evaluates the startup opportunity across multiple dimensions including market research, customer analysis, business model design, technical feasibility, financial projections, go-to-market strategy, and risk assessment.

## Key Findings
- Market Size: {analysis_data.get('market_size', 'To be determined')}
- Competition Level: {analysis_data.get('competition_level', 'To be assessed')}
- Feasibility Score: {analysis_data.get('feasibility_score', 'To be calculated')}%
- Risk Level: {analysis_data.get('risk_level', 'To be evaluated')}

## Detailed Analysis

### Market Research
{json.dumps(analysis_data.get('market_research', {}), indent=2)}

### Customer Analysis
{json.dumps(analysis_data.get('customer_analysis', {}), indent=2)}

### Business Model
{json.dumps(analysis_data.get('business_model', {}), indent=2)}

### Technical Feasibility
{json.dumps(analysis_data.get('technical_feasibility', {}), indent=2)}

### Financial Projections
{json.dumps(analysis_data.get('financial_projections', {}), indent=2)}

### Go-to-Market Strategy
{json.dumps(analysis_data.get('go_to_market', {}), indent=2)}

### Risk Assessment
{json.dumps(analysis_data.get('risk_assessment', {}), indent=2)}

## Recommendations
{chr(10).join(f"- {rec}" for rec in analysis_data.get('recommendations', []))}

## Next Steps
1. Review and validate key assumptions
2. Develop detailed implementation plan
3. Secure necessary resources and funding
4. Execute go-to-market strategy
5. Monitor and iterate based on feedback

---
*Report generated by Startup AI Agent*
"""
    
    return markdown 