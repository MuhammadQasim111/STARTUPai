"""
Streamlit web application for Startup AI Agent
"""

import streamlit as st
import asyncio
import json
from datetime import datetime
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#from startup import agent   
from startup.agent import StartupAIAgent, StartupAnalysis
agent = StartupAIAgent()
# Page configuration
st.set_page_config(
    page_title="Startup AI Agent",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f1f1f;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .analysis-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    .section-title {
        color: #2c3e50;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .info-message {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_agent():
    """Get cached agent instance"""
    return StartupAIAgent()

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🚀 Startup AI Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Transform your startup idea into actionable insights using AI</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Navigation")
        page = st.selectbox(
            "Choose a page",
            ["Analyze Startup", "View History", "Generate Pitch", "Export Data"]
        )
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        
        agent = get_agent()
        history = agent.get_analysis_history()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Analyses", len(history))
        with col2:
            st.metric("Today", len([h for h in history if h.created_at.date() == datetime.now().date()]))
    
    # Main content based on selected page
    if page == "Analyze Startup":
        analyze_startup_page(agent)
    elif page == "View History":
        view_history_page(agent)
    elif page == "Generate Pitch":
        generate_pitch_page(agent)
    elif page == "Export Data":
        export_data_page(agent)

def analyze_startup_page(agent: StartupAIAgent):
    """Startup analysis page"""
    st.header("🔍 Startup Analysis")
    
    # Input section
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            startup_idea = st.text_area(
                "✍️ Describe your startup idea",
                height=150,
                placeholder="Describe your startup idea in detail... Include target market, core features, value proposition, and any other relevant information.",
                help="Be specific about your target market, core features, and value proposition"
            )
        
        with col2:
            st.markdown("### 📋 Analysis Options")
            
            include_market = st.checkbox("Market Research", value=True)
            include_customer = st.checkbox("Customer Analysis", value=True)
            include_business = st.checkbox("Business Model", value=True)
            include_technical = st.checkbox("Technical Feasibility", value=True)
            include_financial = st.checkbox("Financial Projections", value=True)
            include_gotm = st.checkbox("Go-to-Market", value=True)
            include_risk = st.checkbox("Risk Assessment", value=True)
    
    # Analysis button
    if st.button("🚀 Analyze Startup Idea", type="primary", use_container_width=True):
        if not startup_idea:
            st.error("❌ Please enter a startup idea to analyze")
            return
        
        # Show progress
        with st.spinner("🤖 AI is analyzing your startup idea..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Run analysis
                analysis = asyncio.run(agent.analyze_startup_idea(startup_idea))
                
                progress_bar.progress(100)
                status_text.text("✅ Analysis completed!")
                
                # Display results
                display_analysis_results(analysis)
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")

def display_analysis_results(analysis: StartupAnalysis):
    """Display analysis results in a structured format"""
    
    st.markdown('<div class="success-message">✨ Analysis completed successfully!</div>', unsafe_allow_html=True)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔍 Detailed Analysis", "📈 Visualizations", "💡 Recommendations"])
    
    with tab1:
        display_overview(analysis)
    
    with tab2:
        display_detailed_analysis(analysis)
    
    with tab3:
        display_visualizations(analysis)
    
    with tab4:
        display_recommendations(analysis)

def display_overview(analysis: StartupAnalysis):
    """Display analysis overview"""
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Market Size", "Large", "📈")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Competition", "Medium", "⚔️")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Feasibility", "High", "✅")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Risk Level", "Medium", "⚠️")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Summary
    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">📋 Executive Summary</p>', unsafe_allow_html=True)
    
    summary = f"""
    **Analysis Date:** {analysis.created_at.strftime('%Y-%m-%d %H:%M:%S')}
    
    This comprehensive analysis evaluates the startup idea across multiple dimensions including market research, 
    customer analysis, business model design, technical feasibility, financial projections, go-to-market strategy, 
    and risk assessment. The analysis leverages both OpenAI and Gemini AI models for enhanced insights.
    """
    
    st.markdown(summary)
    st.markdown('</div>', unsafe_allow_html=True)

def display_detailed_analysis(analysis: StartupAnalysis):
    """Display detailed analysis sections"""
    
    # Market Research
    with st.expander("📈 Market Research", expanded=True):
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.json(analysis.market_research)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Customer Analysis
    with st.expander("👥 Customer Analysis", expanded=True):
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.json(analysis.customer_analysis)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Business Model
    with st.expander("💼 Business Model", expanded=True):
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.json(analysis.business_model)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Technical Feasibility
    with st.expander("🔧 Technical Feasibility", expanded=True):
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.json(analysis.technical_feasibility)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Financial Projections
    with st.expander("💰 Financial Projections", expanded=True):
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.json(analysis.financial_projections)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Go-to-Market Strategy
    with st.expander("🚀 Go-to-Market Strategy", expanded=True):
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.json(analysis.go_to_market)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Risk Assessment
    with st.expander("⚠️ Risk Assessment", expanded=True):
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.json(analysis.risk_assessment)
        st.markdown('</div>', unsafe_allow_html=True)

def display_visualizations(analysis: StartupAnalysis):
    """Display data visualizations"""
    
    # Sample data for visualizations (in real app, this would come from analysis)
    st.markdown('<p class="section-title">📊 Market Analysis</p>', unsafe_allow_html=True)
    
    # Market size chart
    market_data = pd.DataFrame({
        'Market Segment': ['Direct Competitors', 'Indirect Competitors', 'Potential Partners', 'New Entrants'],
        'Market Share (%)': [30, 25, 35, 10]
    })
    
    fig = px.pie(market_data, values='Market Share (%)', names='Market Segment', 
                 title='Market Landscape Distribution')
    st.plotly_chart(fig, use_container_width=True)
    
    # Revenue projection
    revenue_data = pd.DataFrame({
        'Year': [1, 2, 3, 4, 5],
        'Revenue ($M)': [0.5, 2.5, 8.0, 15.0, 25.0],
        'Growth Rate (%)': [0, 400, 220, 87.5, 66.7]
    })
    
    fig = px.line(revenue_data, x='Year', y='Revenue ($M)', 
                  title='5-Year Revenue Projection')
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk matrix
    risk_data = pd.DataFrame({
        'Risk Category': ['Market Risk', 'Technical Risk', 'Financial Risk', 'Competitive Risk'],
        'Probability': [0.3, 0.2, 0.4, 0.5],
        'Impact': [0.7, 0.6, 0.8, 0.6]
    })
    
    fig = px.scatter(risk_data, x='Probability', y='Impact', 
                     size='Probability', color='Risk Category',
                     title='Risk Assessment Matrix')
    st.plotly_chart(fig, use_container_width=True)

def display_recommendations(analysis: StartupAnalysis):
    """Display recommendations"""
    
    st.markdown('<p class="section-title">💡 Key Recommendations</p>', unsafe_allow_html=True)
    
    for i, recommendation in enumerate(analysis.recommendations, 1):
        st.markdown(f"""
        <div class="analysis-card">
            <h4>🎯 Recommendation {i}</h4>
            <p>{recommendation}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Action items
    st.markdown('<p class="section-title">📋 Next Steps</p>', unsafe_allow_html=True)
    
    action_items = [
        "Conduct detailed market research",
        "Develop MVP prototype",
        "Create financial model",
        "Build founding team",
        "Secure initial funding",
        "Launch beta version"
    ]
    
    for item in action_items:
        st.markdown(f"- ✅ {item}")

def view_history_page(agent: StartupAIAgent):
    """View analysis history page"""
    st.header("📚 Analysis History")
    
    history = agent.get_analysis_history()
    
    if not history:
        st.info("📝 No analysis history found. Run your first analysis to see results here.")
        return
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        date_filter = st.date_input("Filter by date")
    with col2:
        search_term = st.text_input("Search analyses")
    
    # Display history
    for i, analysis in enumerate(reversed(history)):
        with st.expander(f"Analysis {len(history) - i - 1} - {analysis.created_at.strftime('%Y-%m-%d %H:%M:%S')}", expanded=False):
            st.markdown(f"**Created:** {analysis.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"View Details {i}", key=f"view_{i}"):
                    st.session_state.selected_analysis = analysis
                    st.rerun()
            
            with col2:
                if st.button(f"Export {i}", key=f"export_{i}"):
                    export_analysis(analysis)

def generate_pitch_page(agent: StartupAIAgent):
    """Generate pitch deck page"""
    st.header("📋 Pitch Deck Generator")
    
    history = agent.get_analysis_history()
    
    if not history:
        st.info("📝 No analysis history found. Run an analysis first to generate a pitch deck.")
        return
    
    # Select analysis
    analysis_options = [f"Analysis {i} - {h.created_at.strftime('%Y-%m-%d %H:%M:%S')}" 
                       for i, h in enumerate(history)]
    selected_analysis = st.selectbox("Select analysis for pitch deck", analysis_options)
    
    if st.button("🚀 Generate Pitch Deck", type="primary"):
        analysis_index = int(selected_analysis.split()[1])
        analysis = history[analysis_index]
        
        with st.spinner("Generating pitch deck..."):
            pitch_deck = asyncio.run(agent.generate_pitch_deck(analysis))
        
        if "error" in pitch_deck:
            st.error(f"❌ Error generating pitch deck: {pitch_deck['error']}")
        else:
            st.markdown('<div class="success-message">✅ Pitch deck generated successfully!</div>', unsafe_allow_html=True)
            st.markdown(pitch_deck["pitch_deck"])

def export_data_page(agent: StartupAIAgent):
    """Export data page"""
    st.header("📤 Export Data")
    
    history = agent.get_analysis_history()
    
    if not history:
        st.info("📝 No analysis history found. Run an analysis first to export data.")
        return
    
    # Export options
    col1, col2 = st.columns(2)
    
    with col1:
        analysis_index = st.selectbox("Select analysis", range(len(history)), 
                                     format_func=lambda x: f"Analysis {x} - {history[x].created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
    with col2:
        export_format = st.selectbox("Export format", ["JSON", "Markdown"])
    
    if st.button("📤 Export Analysis", type="primary"):
        analysis = history[analysis_index]
        content = agent.export_analysis(analysis, export_format.lower())
        
        # Create download button
        st.download_button(
            label=f"Download {export_format} file",
            data=content,
            file_name=f"startup_analysis_{analysis_index}_{analysis.created_at.strftime('%Y%m%d_%H%M%S')}.{export_format.lower()}",
            mime="application/json" if export_format.lower() == "json" else "text/markdown"
        )

def export_analysis(analysis: StartupAnalysis):
    """Export analysis to file"""
    content = agent.export_analysis(analysis, "json")
    
    # Create download link
    st.download_button(
        label="Download Analysis",
        data=content,
        file_name=f"startup_analysis_{analysis.created_at.strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

if __name__ == "__main__":
    main() 