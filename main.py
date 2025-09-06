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
import time
from typing import Dict, Any
import warnings
warnings.filterwarnings('ignore')

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import organized source code modules
from src.core import DataAnalystAgent, AIBackend
from src.visualization import VisualizationEngine
from src.processors import FileProcessor

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
    """Create an improved Streamlit interface with better organization"""
    assert st is not None
    st.set_page_config(
        page_title="🤖 Advanced AI Data Analyst Agent",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header with better styling
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="color: #1f77b4; margin-bottom: 0;">🤖 Advanced AI Data Analyst Agent</h1>
        <p style="font-size: 1.2em; color: #666; margin-top: 0.5rem;">
            Upload your data and get AI-powered insights with professional analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Sidebar Configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # Backend Selection with better UI (Cloud only for deployment)
        st.markdown("#### 🔧 AI Backend")
        # Comment out local backend for Streamlit deployment
        # backend_type = st.radio(
        #     "Choose your AI backend:",
        #     ["local", "cloud"],
        #     index=0 if agent.backend_type == "local" else 1,
        #     help="Local: LM Studio (Free) | Cloud: Google Gemini AI (Requires API key)"
        # )
        
        # Force cloud backend for Streamlit deployment
        backend_type = "cloud"
        st.info("🌐 Using Google Gemini AI (Cloud Backend)")
        
        # Backend-specific configuration
        st.markdown("#### 🔑 Google AI Configuration")

        # Visible API key input (persisted in session_state)
        input_default = st.session_state.get('google_api_key', os.getenv("GOOGLE_API_KEY", ""))
        api_key_input = st.text_input(
            "Google AI API Key",
            type="password",
            value=input_default,
            help="Get your free API key at https://aistudio.google.com/app/apikey",
            placeholder="Enter your API key here...",
            key="google_api_key_input"
        )

        # Configure button applies the key to the agent backend and stores it in session_state
        col_k1, col_k2 = st.columns([3, 1])
        with col_k2:
            if st.button("Configure Google AI", use_container_width=True):
                st.session_state['google_api_key'] = api_key_input
                # Apply backend change right away
                selected_model = st.session_state.get('selected_model', 'gemini-2.5-pro')
                try:
                    agent.update_backend("cloud", api_key_input, model_name=selected_model)
                    st.success("✅ Google AI backend configured!")
                except Exception as e:
                    st.error(f"❌ Backend error: {str(e)}")

        # Short helper expander
        with st.expander("Google AI Setup", expanded=False):
            st.markdown("Enter your Google AI API key in the field above and click 'Configure Google AI' to apply it.")

        # Determine effective API key (session takes precedence)
        current_key = st.session_state.get('google_api_key') or api_key_input

        # Model selection dropdown (only if a key is available)
        if current_key:
            st.markdown("#### 🤖 Select AI Model")
            available_models = {
                "gemini-2.5-pro": "Gemini 2.5 Pro - Top-end reasoning and multimodal model",
                "gemini-2.5-flash": "Gemini 2.5 Flash - Balanced price-performance", 
                "gemini-2.5-flash-lite": "Gemini 2.5 Flash Lite - Cost-efficient, high throughput",
                "gemini-2.0-flash-experimental": "Gemini 2.0 Flash (Experimental) - Early release with better benchmarks",
                "gemini-2.0-flash": "Gemini 2.0 Flash - New multimodal model with advanced capabilities",
                "gemini-2.0-flash-lite": "Gemini 2.0 Flash Lite - Optimized for low latency and cost"
            }

            # Initialize default selected model once
            if 'selected_model' not in st.session_state:
                st.session_state['selected_model'] = 'gemini-2.5-pro'

            selected_model = st.selectbox(
                "Choose AI Model:",
                options=list(available_models.keys()),
                format_func=lambda x: available_models[x],
                index=0,
                help="Different models offer various capabilities, performance levels, and cost efficiency",
                key="selected_model"
            )

            # Show model info with updated descriptions
            model_info = {
                "gemini-2.5-pro": "🎯 Most capable model with top-end reasoning and multimodal capabilities",
                "gemini-2.5-flash": "⚡ Best balance of performance and cost-effectiveness",
                "gemini-2.5-flash-lite": "💨 High throughput model optimized for cost efficiency",
                "gemini-2.0-flash-experimental": "🚀 Experimental model with enhanced benchmarks vs Gemini 1.5 Pro",
                "gemini-2.0-flash": "� Advanced multimodal model with new capabilities",
                "gemini-2.0-flash-lite": "⚡ Ultra-fast responses with low latency optimization"
            }

            st.info(model_info[selected_model])
        else:
            st.warning("⚠️ API key required for AI analysis")
            st.info("💡 You can paste your GOOGLE_API_KEY here or set the environment variable")
            st.markdown("[🔗 Get API Key](https://aistudio.google.com/app/apikey)")
        
        # Update backend configuration
        selected_model = st.session_state.get('selected_model', 'gemini-2.5-pro')
        # Use the current_key (session or input) to decide whether to configure backend
        if backend_type != agent.backend_type or (backend_type == "cloud" and current_key):
            try:
                agent.update_backend(backend_type, current_key, model_name=selected_model)
                if backend_type == "cloud" and current_key:
                    st.success("✅ Google AI backend configured!")
            except Exception as e:
                st.error(f"❌ Backend error: {str(e)}")
                # Fallback to cloud backend for deployment
                st.warning("Falling back to default cloud configuration...")
        
        # Connection Status with better visualization (Cloud only)
        st.markdown("#### 📡 Connection Status")
        # Comment out local backend status for deployment
        # if backend_type == "local":
        #     if hasattr(agent.ai_backend.client, 'check_connection') and agent.ai_backend.client.check_connection():
        #         st.success("🟢 LM Studio Connected")
        #     else:
        #         st.error("🔴 LM Studio Disconnected")
        #         with st.expander("How to connect LM Studio"):
        #             st.markdown("""
        #             1. Download and install LM Studio
        #             2. Load a model (e.g., Llama 2, Mistral)
        #             3. Start the local server
        #             4. Ensure it's running on localhost:1234
        #             """)
        # else:
        if current_key:
            st.success("🟢 Google AI Connected")
            st.info(f"🤖 Using model: {selected_model}")
        else:
            st.error("🔴 Google AI Not Configured")
        
        # Additional controls
        st.markdown("---")
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            agent.ai_backend.clear_conversation_history()
            st.success("Conversation cleared!")
        
        # Help section
        with st.expander("ℹ️ Help & Tips"):
            st.markdown("""
            **Supported File Types:**
            - 📊 CSV, Excel (xlsx, xls)
            - 📄 PDF, DOCX, TXT
            - 🖼️ Images (PNG, JPG, JPEG)
            
            **Best Practices:**
            - Use descriptive questions
            - Mention specific columns/data points
            - Ask for actionable insights
            """)
    
    # Main content area with tabs for better organization
    tab1, tab2, tab3, tab4 = st.tabs(["📂 Data Upload", "📊 Analysis", "📈 Visualizations", "💬 AI Chat"])
    
    # Tab 1: Data Upload and Processing
    with tab1:
        st.markdown("### 📂 Upload and Process Your Data")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_files = st.file_uploader(
                "Choose your data files",
                type=['csv', 'xlsx', 'xls', 'pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'],
                help="Drag and drop or click to browse (supports multiple files)",
                key="file_uploader",
                accept_multiple_files=True
            )
        
        with col2:
            if uploaded_files:
                st.markdown(f"**Files Selected ({len(uploaded_files)}):**")
                for i, uploaded_file in enumerate(uploaded_files[:3]):  # Show first 3
                    st.info(f"� **{uploaded_file.name}** ({uploaded_file.size:,} bytes)")
                if len(uploaded_files) > 3:
                    st.info(f"... and {len(uploaded_files) - 3} more files")
        
        # Process uploaded files
        if uploaded_files:
            process_uploaded_files(agent, uploaded_files)
    
    # Tab 2: Data Analysis Overview
    with tab2:
        if agent.current_data is not None or agent.current_file_info:
            show_data_analysis(agent)
        else:
            st.info("👆 Please upload a file in the 'Data Upload' tab to see analysis")
    
    # Tab 3: Advanced Visualizations
    with tab3:
        if agent.current_data is not None:
            show_visualizations(agent)
        else:
            st.info("👆 Please upload data to create visualizations")    # Tab 4: AI Chat Interface
    with tab4:
        show_ai_chat_interface(agent)


def process_uploaded_files(agent: DataAnalystAgent, uploaded_files):
    """Process and display multiple uploaded files information"""
    assert st is not None
    
    if not uploaded_files:
        return
    
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, uploaded_file in enumerate(uploaded_files):
        status_text.text(f"Processing {uploaded_file.name}...")
        progress_bar.progress((i + 1) / len(uploaded_files))
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Process file
        with st.spinner(f"🔄 Processing {uploaded_file.name}..."):
            result = agent.process_file(tmp_file_path)
            result['original_filename'] = uploaded_file.name
            results.append(result)
        
        # Clean up temporary file with retries (Windows may lock files briefly)
        def _remove_path(path: str, retries: int = 5, delay: float = 0.2):
            for attempt in range(retries):
                try:
                    if os.path.exists(path):
                        os.remove(path)
                    return True
                except PermissionError:
                    time.sleep(delay)
                except Exception:
                    break
            return False

        removed = _remove_path(tmp_file_path)
        if not removed:
            # If we couldn't delete, show a non-blocking warning and continue
            try:
                st.warning(f"Temporary file could not be deleted immediately: {tmp_file_path}")
            except Exception:
                pass
    
    progress_bar.empty()
    status_text.empty()
    
    # Display results summary
    successful_files = [r for r in results if 'error' not in r]
    error_files = [r for r in results if 'error' in r]
    
    if successful_files:
        st.success(f"✅ Successfully processed {len(successful_files)} file(s)!")
        
        # Show summary
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📊 Processed Files:**")
            for result in successful_files:
                file_type = result.get('type', 'unknown')
                filename = result.get('original_filename', 'unknown')
                st.write(f"• {filename} ({file_type})")
        
        with col2:
            st.markdown("**📈 Data Summary:**")
            total_rows = sum(len(r.get('data', [])) for r in successful_files if 'data' in r)
            total_text_files = sum(1 for r in successful_files if 'text' in r)
            if total_rows > 0:
                st.metric("Total Data Rows", f"{total_rows:,}")
            if total_text_files > 0:
                st.metric("Text/Document Files", total_text_files)
    
    if error_files:
        st.error(f"❌ Failed to process {len(error_files)} file(s)")
        with st.expander("Error Details"):
            for result in error_files:
                filename = result.get('original_filename', 'unknown')
                error_msg = result.get('error', 'Unknown error')
                st.write(f"**{filename}:** {error_msg}")
    
    # Store all processed results for other tabs
    st.session_state['file_processed'] = len(successful_files) > 0
    st.session_state['file_results'] = results
    st.session_state['successful_results'] = successful_files


def process_uploaded_file(agent: DataAnalystAgent, uploaded_file):
    """Process and display uploaded file information"""
    assert st is not None
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name
    
    # Process file
    with st.spinner("🔄 Processing file..."):
        result = agent.process_file(tmp_file_path)
    
    # Clean up temporary file with retries (Windows may lock files briefly)
    def _remove_path(path: str, retries: int = 5, delay: float = 0.2):
        for attempt in range(retries):
            try:
                if os.path.exists(path):
                    os.remove(path)
                return True
            except PermissionError:
                time.sleep(delay)
            except Exception:
                break
        return False

    removed = _remove_path(tmp_file_path)
    if not removed:
        # If we couldn't delete, show a non-blocking warning and continue
        try:
            st.warning(f"Temporary file could not be deleted immediately: {tmp_file_path}")
        except Exception:
            pass
    
    if 'error' in result:
        st.error(f"❌ Error: {result['error']}")
        if 'message' in result:
            st.info(result['message'])
    else:
        st.success("✅ File processed successfully!")
        
        # Store processed data info for other tabs
        st.session_state['file_processed'] = True
        st.session_state['file_result'] = result


def show_data_analysis(agent: DataAnalystAgent):
    """Display comprehensive data analysis"""
    assert st is not None
    st.markdown("### 📊 Data Analysis Overview")
    
    if 'file_processed' not in st.session_state or not st.session_state['file_processed']:
        st.warning("Please upload and process file(s) first")
        return
    
    results = st.session_state.get('successful_results', [])
    if not results:
        st.warning("No successfully processed files available")
        return
    
    # Multi-file overview
    st.markdown(f"#### 📁 Analysis of {len(results)} File(s)")
    
    # Aggregate statistics
    col1, col2, col3 = st.columns(3)
    
    total_data_files = sum(1 for r in results if 'data' in r)
    total_text_files = sum(1 for r in results if 'text' in r)
    total_rows = sum(len(r['data']) if 'data' in r and r['data'] is not None else 0 for r in results)
    
    with col1:
        st.metric("Data Files", total_data_files)
        st.metric("Text/Document Files", total_text_files)
    
    with col2:
        if total_rows > 0:
            st.metric("Total Data Rows", f"{total_rows:,}")
        
        # Calculate total file size approximation
        total_memory = sum(
            r['data'].memory_usage(deep=True).sum() / 1024 if 'data' in r and r['data'] is not None else 0 
            for r in results
        )
        if total_memory > 0:
            st.metric("Total Memory Usage", f"{total_memory:.1f} KB")
    
    with col3:
        # Data quality overview
        total_missing = sum(
            r['data'].isnull().sum().sum() if 'data' in r and r['data'] is not None else 0 
            for r in results
        )
        if total_missing >= 0:
            st.metric("Total Missing Values", total_missing)
    
    # Individual file details
    st.markdown("#### 📋 Individual File Details")
    
    for i, result in enumerate(results):
        filename = result.get('original_filename', f'File {i+1}')
        file_type = result.get('type', 'unknown')
        
        with st.expander(f"📄 {filename} ({file_type})", expanded=i == 0):
            if 'data' in result and result['data'] is not None:
                df = result['data']
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.dataframe(df.head(5), use_container_width=True)
                
                with col2:
                    st.markdown("**Column Info:**")
                    for col in df.columns[:5]:  # Show first 5 columns
                        dtype = str(df[col].dtype)
                        st.write(f"**{col}:** {dtype}")
                    if len(df.columns) > 5:
                        st.write(f"... and {len(df.columns) - 5} more columns")
                
                # Basic statistics for numeric columns
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    st.markdown("**📊 Numeric Summary:**")
                    st.dataframe(df[numeric_cols].describe(), use_container_width=True)
            
            elif 'text' in result:
                # Text content preview
                content = result['text']
                content_preview = content[:1000] + "..." if len(content) > 1000 else content
                st.text_area("Content Preview", content_preview, height=200, disabled=True, key=f"text_preview_{i}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Characters", len(content))
                with col2:
                    st.metric("Words", len(content.split()))
                with col3:
                    st.metric("Lines", content.count('\n') + 1)


def show_visualizations(agent: DataAnalystAgent):
    """Display advanced visualizations"""
    assert st is not None
    st.markdown("### 📈 Advanced Visualizations")
    
    if 'file_processed' not in st.session_state or not st.session_state['file_processed']:
        st.warning("Please upload and process file(s) first")
        return
    
    results = st.session_state.get('successful_results', [])
    data_results = [r for r in results if 'data' in r and r['data'] is not None]
    
    if not data_results:
        st.warning("No data files available for visualization")
        return
    
    # File selection for visualization
    if len(data_results) > 1:
        st.markdown("#### 📁 Select Dataset for Visualization")
        file_options = {f"{r.get('original_filename', f'File {i+1}')}": i for i, r in enumerate(data_results)}
        selected_file = st.selectbox("Choose dataset:", options=list(file_options.keys()))
        selected_idx = file_options[selected_file]
        df = data_results[selected_idx]['data']
        st.info(f"Visualizing: {selected_file}")
    else:
        df = data_results[0]['data']
        st.info(f"Visualizing: {data_results[0].get('original_filename', 'Dataset')}")
    
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_columns) == 0:
        st.warning("No numeric columns found for visualization")
        return
    
    # Quick Visualizations Section
    st.markdown("#### 🚀 Quick Visualizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Distribution Plot**")
        if len(numeric_columns) > 0:
            selected_col = st.selectbox("Select column for distribution:", numeric_columns, key="dist_col")
            fig = px.histogram(df, x=selected_col, title=f"Distribution of {selected_col}")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Correlation Heatmap**")
        if len(numeric_columns) >= 2:
            if st.button("Generate Correlation Matrix", key="corr_matrix"):
                with st.spinner("Creating correlation matrix..."):
                    corr_matrix = df[numeric_columns].corr()
                    fig = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                                  title="Correlation Matrix")
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least 2 numeric columns for correlation analysis")
    
    # Advanced Visualizations Section
    st.markdown("#### 🎯 Advanced Analysis")
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        if st.button("📊 Create Summary Dashboard", key="summary_dashboard"):
            with st.spinner("Creating comprehensive dashboard..."):
                try:
                    # Temporarily set current_data for visualization engine
                    agent.current_data = df
                    viz_engine = VisualizationEngine(agent)
                    fig = viz_engine.create_summary_dashboard()
                    if fig:
                        st.pyplot(fig)
                    else:
                        st.info("Unable to create summary dashboard with current data")
                except Exception as e:
                    st.error(f"Error creating dashboard: {str(e)}")
    
    with viz_col2:
        if st.button("🔗 Advanced Correlation Analysis", key="advanced_corr"):
            with st.spinner("Creating advanced correlation analysis..."):
                try:
                    # Temporarily set current_data for visualization engine
                    agent.current_data = df
                    viz_engine = VisualizationEngine(agent)
                    fig = viz_engine.create_correlation_matrix()
                    if fig:
                        st.pyplot(fig)
                    else:
                        st.info("Unable to create correlation analysis")
                except Exception as e:
                    st.error(f"Error creating correlation analysis: {str(e)}")
    
    # Interactive Scatter Plot
    if len(numeric_columns) >= 2:
        st.markdown("#### 🎲 Interactive Scatter Plot")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            x_col = st.selectbox("X-axis:", numeric_columns, key="scatter_x")
        with col2:
            y_col = st.selectbox("Y-axis:", numeric_columns, index=1, key="scatter_y")
        with col3:
            color_col = st.selectbox("Color by:", ['None'] + list(df.columns), key="scatter_color")
        
        color_var = None if color_col == 'None' else color_col
        fig = px.scatter(df, x=x_col, y=y_col, color=color_var, 
                        title=f"{x_col} vs {y_col}")
        st.plotly_chart(fig, use_container_width=True)


def show_ai_chat_interface(agent: DataAnalystAgent):
    """Display AI chat interface"""
    assert st is not None
    st.markdown("### 💬 AI-Powered Data Analysis Chat")
    
    # Check if data is available
    if not st.session_state.get('file_processed', False):
        st.warning("⚠️ Please upload file(s) first to enable AI analysis")
        st.info("👆 Go to the 'Data Upload' tab to upload your data")
        return
    
    # Display conversation history in a nicer format
    if agent.ai_backend.conversation_history:
        st.markdown("#### 🗨️ Conversation History")
          # Create a container for scrollable chat history
        chat_container = st.container()
        with chat_container:
            for i, entry in enumerate(agent.ai_backend.conversation_history):
                if entry['role'] == 'user':
                    st.markdown(f"""
                    <div style="background-color: #f0f8ff; color: #2c3e50; padding: 10px; border-radius: 10px; margin: 5px 0; border-left: 3px solid #3498db;">
                        <strong>👤 You:</strong> {entry['content']}
                    </div>
                    """, unsafe_allow_html=True)
                elif entry['role'] == 'assistant':
                    st.markdown(f"""
                    <div style="background-color: #f8f8f8; color: #2c3e50; padding: 10px; border-radius: 10px; margin: 5px 0; border-left: 3px solid #27ae60;">
                        <strong>🤖 AI Assistant:</strong> {entry['content']}
                    </div>
                    """, unsafe_allow_html=True)
                
                if i < len(agent.ai_backend.conversation_history) - 1:
                    st.markdown("---")
    
    # Question input section
    st.markdown("#### ❓ Ask Your Question")
    
    # Provide example questions
    with st.expander("💡 Example Questions"):
        example_questions = [
            "What are the key patterns in this data?",
            "Can you identify any outliers or anomalies?",
            "What insights can you provide about the trends?",
            "What are the main correlations in the data?",
            "Can you summarize the most important findings?",
            "What actionable recommendations do you have?",
            "Are there any data quality issues I should be aware of?"
        ]
        
        for i, example in enumerate(example_questions):
            if st.button(f"📋 {example}", key=f"example_{i}"):
                st.session_state['question_input'] = example
    
    # Question input
    question = st.text_area(
        "Enter your question about the data:",
        placeholder="What insights can you provide about this data?",
        height=100,
        value=st.session_state.get('question_input', ''),
        key="main_question_input"
    )
    
    # Analyze button with better styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button(
            "🔍 Analyze with AI",
            use_container_width=True,
            type="primary"
        )
    
    if analyze_button and isinstance(question, str) and question.strip():
        if st.session_state.get('file_processed', False):
            with st.spinner("🤖 AI is analyzing your data..."):
                try:
                    context = agent.get_data_context()
                    # If the last processed files have Gemini file_uris, include them
                    file_uri = None
                    mime_type = None
                    results = st.session_state.get('successful_results', [])
                    
                    # For multi-file support, we'll use the first file with file_uri for now
                    # Future enhancement could combine multiple file_uris
                    for result in results:
                        if result.get('file_uri'):
                            file_uri = result.get('file_uri')
                            mime_type = result.get('mime_type')
                            break
                    
                    question_str = question or ""
                    
                    # Build enhanced context for multi-file analysis
                    if len(results) > 1:
                        context += f"\n\nNote: This analysis covers {len(results)} files. "
                        context += "The files processed are: " + ", ".join([
                            r.get('original_filename', 'unknown') for r in results
                        ])
                    
                    response = agent.ai_backend.answer_question(question_str, context, file_uri=file_uri, mime_type=mime_type)
                      # Display the response in a nice format
                    st.markdown("#### 🎯 AI Analysis Result")
                    st.markdown(f"""
                    <div style="background-color: #f8f8f8; color: #333333; padding: 15px; border-radius: 10px; border-left: 4px solid #1f77b4; font-size: 14px; line-height: 1.6;">
                        {response}
                    """, unsafe_allow_html=True)
                    
                    # Clear the question input
                    st.session_state['question_input'] = ''
                    
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")
        else:
            st.warning("Please upload file(s) first!")
    elif analyze_button and (not isinstance(question, str) or not question.strip()):
        st.warning("Please enter a question before analyzing!")
    
    # Quick action buttons
    st.markdown("#### ⚡ Quick Actions")
    quick_col1, quick_col2, quick_col3 = st.columns(3)
    
    with quick_col1:
        if st.button("📊 Data Summary", use_container_width=True):
            st.session_state['question_input'] = "Can you provide a comprehensive summary of this data including key statistics, patterns, and insights?"
    
    with quick_col2:
        if st.button("🔍 Find Insights", use_container_width=True):
            st.session_state['question_input'] = "What are the most important insights and patterns you can identify in this data?"
    
    with quick_col3:
        if st.button("💡 Recommendations", use_container_width=True):
            st.session_state['question_input'] = "Based on this data analysis, what actionable recommendations do you have?"


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
    
    # Comment out Gradio interface for Streamlit deployment
    # elif args.interface == 'gradio':
    #     if gr is None:
    #         print("❌ Gradio not installed. Install with: pip install gradio")
    #         sys.exit(1)
    #     
    #     # Create Gradio interface with backend selection
    #     def process_and_answer(file, question, backend_choice, api_key=""):
    #         if file is None:
    #             return "Please upload a file first!"
    #           # Update backend if needed
    #         if backend_choice == "Cloud (Google Gemini)":
    #             if not api_key.strip():
    #                 return "❌ Please provide your Google AI API key for cloud backend"
    #             try:
    #                 agent.update_backend("cloud", api_key.strip())
    #             except Exception as e:
    #                 return f"❌ Failed to configure cloud backend: {str(e)}"
    #         else:
    #             agent.update_backend("local")
    #         
    #         result = agent.process_file(file.name)
    #         if 'error' in result:
    #             return f"Error: {result['error']}"
    #         
    #         context = agent.get_data_context()
    #         response = agent.ai_backend.answer_question(question, context)
    #         return response
    #     
    #     # Create inputs
    #     inputs = [
    #         gr.File(label="Upload Data File"),
    #         gr.Textbox(label="Ask a Question", placeholder="What insights can you provide?"),
    #         gr.Dropdown(
    #             choices=["Local (LM Studio)", "Cloud (Google Gemini)"],
    #             value="Local (LM Studio)",
    #             label="AI Backend"
    #         ),
    #         gr.Textbox(
    #             label="Google AI API Key (for cloud backend)",
    #             type="password",
    #             placeholder="Enter API key here (only needed for cloud backend)",
    #             value=os.getenv("GOOGLE_API_KEY", "")
    #         )
    #     ]
    #     
    #     interface = gr.Interface(
    #         fn=process_and_answer,
    #         inputs=inputs,
    #         outputs=gr.Textbox(label="AI Response"),
    #         title="🤖 AI Data Analyst Agent",
    #         description="Upload your data and get AI-powered insights! Choose between local LM Studio or cloud Google Gemini backend."
    #     )
    #     
    #     interface.launch(server_port=args.port)
    
    # Additional Gradio interface commented out for Streamlit deployment
    # elif args.interface == 'gradio':
    #     if gr is None:
    #         print("❌ Gradio not installed. Install with: pip install gradio")
    #         sys.exit(1)
    #     
    #     # Create Gradio interface with backend selection
    #     def process_and_answer(file, question, backend_choice, api_key=""):
    #         if file is None:
    #             return "Please upload a file first!"
    #           # Update backend if needed
    #         if backend_choice == "Cloud (Google Gemini)":
    #             if not api_key.strip():
    #                 return "❌ Please provide your Google AI API key for cloud backend"
    #             try:
    #                 agent.update_backend("cloud", api_key.strip())
    #             except Exception as e:
    #                 return f"❌ Failed to configure cloud backend: {str(e)}"
    #         else:
    #             agent.update_backend("local")
    #         
    #         result = agent.process_file(file.name)
    #         if 'error' in result:
    #             return f"Error: {result['error']}"
    #         
    #         context = agent.get_data_context()
    #         response = agent.ai_backend.answer_question(question, context)
    #         return response
    #     
    #     # Create inputs
    #     inputs = [
    #         gr.File(label="Upload Data File"),
    #         gr.Textbox(label="Ask a Question", placeholder="What insights can you provide?"),
    #         gr.Dropdown(
    #             choices=["Local (LM Studio)", "Cloud (Google Gemini)"],
    #             value="Local (LM Studio)",
    #             label="AI Backend"
    #         ),
    #         gr.Textbox(
    #             label="Google AI API Key (for cloud backend)",
    #             type="password",
    #             placeholder="Enter API key here (only needed for cloud backend)",
    #             value=os.getenv("GOOGLE_API_KEY", "")
    #         )
    #     ]
    #     
    #     interface = gr.Interface(
    #         fn=process_and_answer,
    #         inputs=inputs,
    #         outputs=gr.Textbox(label="AI Response"),
    #         title="🤖 AI Data Analyst Agent",
    #         description="Upload your data and get AI-powered insights! Choose between local LM Studio or cloud Google Gemini backend."
    #     )
    #     
    #     interface.launch(server_port=args.port)


if __name__ == "__main__":
    main()
