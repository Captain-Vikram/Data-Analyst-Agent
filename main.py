#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 AI Data Analyst Agent - Main Application Entry Point

A powerful AI-powered data analysis application that supports multiple file formats,
provides intelligent insights, and offers both local and cloud-based AI integration.

Usage:
    python main.py [--interface {streamlit,gradio}] [--port PORT] [--backend {local,cloud}]

Examples:
    python main.py                          # Streamlit interface with local backend
    python main.py --interface gradio       # Gradio interface
    python main.py --backend cloud          # Cloud AI backend
    python main.py --port 8502             # Custom port
"""

import os
import sys
import argparse
import tempfile
from typing import Dict, Any
import warnings
warnings.filterwarnings('ignore')

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import organized source code modules
from core import DataAnalystAgent, AIBackend
from visualization import VisualizationEngine
from processors import FileProcessor

# UI libraries
try:
    import streamlit as st
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import plotly.express as px
except ImportError as e:
    st = None
    print(f"Warning: Streamlit dependencies not available: {e}")

try:
    import gradio as gr
except ImportError:
    gr = None


def create_streamlit_app(agent: DataAnalystAgent):
    """Create Streamlit interface"""
    st.set_page_config(
        page_title="🤖 AI Data Analyst Agent",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Advanced AI Data Analyst Agent")
    st.markdown("**Upload your data and get AI-powered insights!**")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Backend selection
        backend_type = st.selectbox(
            "AI Backend",
            ["local", "cloud"],
            index=0 if agent.backend_type == "local" else 1,
            help="Local: LM Studio, Cloud: Together.ai"
        )
        
        # API Key input for cloud backend
        api_key = None
        if backend_type == "cloud":
            st.subheader("🔑 Cloud AI Configuration")
            api_key = st.text_input(
                "Together.ai API Key",
                type="password",
                value=os.getenv("TOGETHER_API_KEY", ""),
                help="Enter your Together.ai API key. Get one at https://api.together.xyz/",
                placeholder="Enter your API key here..."
            )
            
            if not api_key:
                st.warning("⚠️ Please enter your Together.ai API key to use cloud backend")
                st.info("💡 You can also set the TOGETHER_API_KEY environment variable")
        
        # Update backend if changed
        if backend_type != agent.backend_type or (backend_type == "cloud" and api_key):
            try:
                agent.update_backend(backend_type, api_key)
                if backend_type == "cloud" and api_key:
                    st.success("✅ Cloud backend configured!")
            except Exception as e:
                st.error(f"❌ Failed to configure backend: {str(e)}")
                # Fall back to local backend
                agent.update_backend("local")
                backend_type = "local"
        
        # Connection status
        if backend_type == "local":
            if hasattr(agent.ai_backend.client, 'check_connection') and agent.ai_backend.client.check_connection():
                st.success("✅ LM Studio Connected")
            else:
                st.error("❌ LM Studio Not Connected")
                st.info("Please start LM Studio server first")
        else:
            if api_key:
                st.success("✅ Together.ai API Key Configured")
            else:
                st.error("❌ Together.ai API Key Missing")
        
        # Clear conversation
        if st.button("🗑️ Clear Conversation"):
            agent.ai_backend.clear_conversation_history()
            st.success("Conversation cleared!")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload your data file",
        type=['csv', 'xlsx', 'xls', 'pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'],
        help="Supported formats: CSV, Excel, PDF, DOCX, TXT, Images"
    )
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Process file
        with st.spinner("Processing file..."):
            result = agent.process_file(tmp_file_path)
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        if 'error' in result:
            st.error(f"Error: {result['error']}")
            if 'message' in result:
                st.info(result['message'])
        else:
            st.success("✅ File processed successfully!")
            
            # Display file info
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 File Information")
                if 'info' in result:
                    for key, value in result['info'].items():
                        if isinstance(value, (int, float, str)):
                            st.metric(key.replace('_', ' ').title(), value)
            
            with col2:
                st.subheader("📈 Quick Stats")
                if 'data' in result and not result['data'].empty:
                    df = result['data']
                    st.metric("Rows", len(df))
                    st.metric("Columns", len(df.columns))
                    st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
            
            # Show data preview
            if 'data' in result and not result['data'].empty:
                st.subheader("🔍 Data Preview")
                st.dataframe(result['data'].head(10), use_container_width=True)
                
                # Basic visualizations
                st.subheader("📊 Quick Visualizations")
                numeric_columns = result['data'].select_dtypes(include=[np.number]).columns
                
                if len(numeric_columns) > 0:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if len(numeric_columns) >= 2:
                            fig = px.scatter(result['data'], x=numeric_columns[0], y=numeric_columns[1])
                            st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        fig = px.histogram(result['data'], x=numeric_columns[0])
                        st.plotly_chart(fig, use_container_width=True)
                
                # Advanced Visualizations
                st.subheader("📈 Advanced Visualizations")
                viz_engine = VisualizationEngine(agent)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📊 Summary Dashboard", key="summary_dashboard"):
                        with st.spinner("Creating summary dashboard..."):
                            fig = viz_engine.create_summary_dashboard()
                            if fig:
                                st.pyplot(fig)
                            else:
                                st.info("No data available for summary dashboard")
                
                with col2:
                    if st.button("🔗 Correlation Matrix", key="correlation_matrix"):
                        with st.spinner("Creating correlation matrix..."):
                            fig = viz_engine.create_correlation_matrix()
                            if fig:
                                st.pyplot(fig)
                            else:
                                st.info("No numeric data available for correlation analysis")
            
            # Text content preview
            elif 'text' in result:
                st.subheader("📄 Content Preview")
                st.text_area("Document Content", result['text'][:1000] + "...", height=200, disabled=True)
    
    # Q&A Section
    st.subheader("💬 Ask Questions About Your Data")
    
    # Display conversation history
    if agent.ai_backend.conversation_history:
        st.subheader("🗨️ Conversation History")
        for entry in agent.ai_backend.conversation_history:
            if entry['role'] == 'user':
                st.write(f"**You:** {entry['content']}")
            elif entry['role'] == 'assistant':
                st.write(f"**AI:** {entry['content']}")
            st.write("---")
    
    # Question input
    question = st.text_input("Ask a question about your data:", placeholder="What insights can you provide about this data?")
    
    if st.button("🔍 Analyze") and question:
        if agent.current_data is not None or agent.current_file_info:
            with st.spinner("Analyzing..."):
                context = agent.get_data_context()
                response = agent.ai_backend.answer_question(question, context)
                st.write(f"**AI Response:**")
                st.write(response)
        else:
            st.warning("Please upload a file first!")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Advanced AI Data Analyst Agent',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--interface',
        choices=['streamlit', 'gradio'],
        default='streamlit',
        help='Interface type (default: streamlit)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8501,
        help='Port to run on (default: 8501)'
    )
    
    parser.add_argument(
        '--backend',
        choices=['local', 'cloud'],
        default='local',
        help='AI backend type (default: local)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = DataAnalystAgent(backend_type=args.backend)
    
    if args.interface == 'streamlit':
        if st is None:
            print("❌ Streamlit not installed. Install with: pip install streamlit")
            sys.exit(1)
        
        # Run Streamlit app
        create_streamlit_app(agent)
    
    elif args.interface == 'gradio':
        if gr is None:
            print("❌ Gradio not installed. Install with: pip install gradio")
            sys.exit(1)
        
        # Create Gradio interface with backend selection
        def process_and_answer(file, question, backend_choice, api_key=""):
            if file is None:
                return "Please upload a file first!"
            
            # Update backend if needed
            if backend_choice == "Cloud (Together.ai)":
                if not api_key.strip():
                    return "❌ Please provide your Together.ai API key for cloud backend"
                try:
                    agent.update_backend("cloud", api_key.strip())
                except Exception as e:
                    return f"❌ Failed to configure cloud backend: {str(e)}"
            else:
                agent.update_backend("local")
            
            result = agent.process_file(file.name)
            if 'error' in result:
                return f"Error: {result['error']}"
            
            context = agent.get_data_context()
            response = agent.ai_backend.answer_question(question, context)
            return response
        
        # Create inputs
        inputs = [
            gr.File(label="Upload Data File"),
            gr.Textbox(label="Ask a Question", placeholder="What insights can you provide?"),
            gr.Dropdown(
                choices=["Local (LM Studio)", "Cloud (Together.ai)"],
                value="Local (LM Studio)",
                label="AI Backend"
            ),
            gr.Textbox(
                label="Together.ai API Key (for cloud backend)",
                type="password",
                placeholder="Enter API key here (only needed for cloud backend)",
                value=os.getenv("TOGETHER_API_KEY", "")
            )
        ]
        
        interface = gr.Interface(
            fn=process_and_answer,
            inputs=inputs,
            outputs=gr.Textbox(label="AI Response"),
            title="🤖 AI Data Analyst Agent",
            description="Upload your data and get AI-powered insights! Choose between local LM Studio or cloud Together.ai backend."
        )
        
        interface.launch(server_port=args.port)


if __name__ == "__main__":
    main()
