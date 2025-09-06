"""
Core classes for the AI Data Analyst Agent.

This module contains the main DataAnalystAgent class and AIBackend class
that provide the core functionality for data analysis and AI interactions.
"""

import os
import json
import tempfile
from datetime import datetime
from typing import Dict, List, Any, Optional
import warnings
warnings.filterwarnings('ignore')

# Data processing libraries
import pandas as pd
import numpy as np

# Visualization libraries
import matplotlib.pyplot as plt
import seaborn as sns
try:
    import plotly.express as px
    import plotly.graph_objects as go
except ImportError:
    px = None
    go = None

from .processors import FileProcessor
from .clients import CloudAIClient  # LocalLMStudioClient commented out for cloud deployment


class AIBackend:
    """
    Unified AI backend supporting both local and cloud providers.
    
    This class provides a consistent interface for interacting with both
    local LM Studio and cloud-based AI services like Together.ai.
    """
    
    def __init__(self, backend_type: str = "cloud", api_key: Optional[str] = None, model_name: Optional[str] = None):
        """
        Initialize the AI backend.
        
        Args:
            backend_type: Type of backend ("local" or "cloud") - defaults to cloud for deployment
            api_key: API key for cloud services (optional)
            model_name: Specific model to use (for cloud backends)
        """
        self.backend_type = backend_type
        self.model_name = model_name or "gemini-2.5-pro"
        self.conversation_history = []
        self.client = None

        # Defer cloud initialization until an API key is provided via the UI
        if backend_type == "cloud" and api_key:
            try:
                self.client = CloudAIClient(api_key=api_key, model_name=self.model_name)
            except Exception as e:
                # Keep client unset; UI will show connection error
                print(f"Warning: Failed to initialize cloud backend: {e}")
    
    def answer_question(self, question: str, context: str = "", file_uri: Optional[str] = None, mime_type: Optional[str] = None) -> str:
        """
        Answer a question using the configured AI backend.
        
        Args:
            question: The question to answer
            context: Additional context about the data
            
        Returns:
            The AI-generated response
        """
        try:
            if not self.client:
                return "Error: Cloud AI is not configured. Please enter your Google AI API key in the sidebar and click 'Configure Google AI'."
            response = self.client.answer_question(question, context, file_uri=file_uri, mime_type=mime_type)
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": question,
                "timestamp": datetime.now().isoformat()
            })
            self.conversation_history.append({
                "role": "assistant", 
                "content": response,
                "timestamp": datetime.now().isoformat()
            })
            
            return response
        except Exception as e:
            return f"Error getting AI response: {str(e)}"
    
    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation history."""
        if not self.conversation_history:
            return "No conversation history available."
        
        questions = [entry for entry in self.conversation_history if entry["role"] == "user"]
        answers = [entry for entry in self.conversation_history if entry["role"] == "assistant"]
        
        summary = f"Conversation Summary:\n"
        summary += f"- Total questions asked: {len(questions)}\n"
        summary += f"- Total responses given: {len(answers)}\n"
        summary += f"- Conversation started: {self.conversation_history[0]['timestamp']}\n"
        summary += f"- Last activity: {self.conversation_history[-1]['timestamp']}\n"
        
        return summary


class DataAnalystAgent:
    """
    Main application class that orchestrates data analysis workflows.

    This class provides the primary interface for uploading files,
    processing data, and generating AI-powered insights.
    """

    def __init__(self, backend_type: str = "local", api_key: Optional[str] = None):
        """
        Initialize the Data Analyst Agent.

        Args:
            backend_type: Type of AI backend to use
            api_key: API key for cloud services (optional)
        """
        self.backend_type = backend_type
        self.file_processor = FileProcessor()
        self.ai_backend = AIBackend(backend_type, api_key)
        # Track current processed data and file metadata
        self.current_data = None
        self.current_file_info = None

    def update_backend(self, backend_type: str, api_key: Optional[str] = None, model_name: Optional[str] = None):
        """
        Update the AI backend with new configuration.

        Args:
            backend_type: New backend type
            api_key: API key for cloud services (optional)
            model_name: Specific model to use (for cloud backends)
        """
        self.backend_type = backend_type
        self.ai_backend = AIBackend(backend_type, api_key=api_key, model_name=model_name)

    def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process uploaded file based on extension.

        Args:
            file_path: Path to the file to process

        Returns:
            Dictionary containing processed data and metadata
        """
        if not os.path.exists(file_path):
            return {"error": "File not found"}

        file_ext = os.path.splitext(file_path)[1].lower()

        if file_ext == ".csv":
            result = self.file_processor.process_csv(file_path)
        elif file_ext in [".xlsx", ".xls"]:
            result = self.file_processor.process_excel(file_path)
        elif file_ext == ".pdf":
            result = self.file_processor.process_pdf(file_path)
        elif file_ext == ".docx":
            result = self.file_processor.process_docx(file_path)
        elif file_ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
            result = self.file_processor.process_image(file_path)
        elif file_ext == ".txt":
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                result = {"text": content, "info": {"word_count": len(content.split())}, "type": "txt"}
            except Exception as e:
                result = {"error": f"Text file processing failed: {str(e)}"}
        else:
            result = {"error": f"Unsupported file format: {file_ext}"}

        # If PDF or image, try to upload to Gemini File API (optional)
        try:
            if (
                isinstance(result, dict)
                and result.get("type") in ("pdf", "image")
                and getattr(self.ai_backend, "client", None) is not None
                and hasattr(self.ai_backend.client, "upload_file")
            ):
                upload_info = self.ai_backend.client.upload_file(file_path)  # type: ignore[union-attr]
                if isinstance(upload_info, dict) and "name" in upload_info:
                    # Attach file_uri and mime_type to result if present
                    name_val = upload_info.get("name")
                    if isinstance(name_val, str) and name_val:
                        result["file_uri"] = name_val
                    mime_val = upload_info.get("mimeType")
                    if isinstance(mime_val, str) and mime_val:
                        result["mime_type"] = mime_val
        except Exception:
            # Non-fatal: continue without file_uri
            pass

        if isinstance(result, dict) and "data" in result:
            self.current_data = result["data"]
            self.current_file_info = result.get("info", {}) if isinstance(result.get("info", {}), dict) else {}
        elif isinstance(result, dict) and "text" in result:
            # For unstructured content like PDF/TXT/Images
            self.current_data = None
            self.current_file_info = result

        return result

    def get_data_context(self) -> str:
        """
        Generate context string from current data.

        Returns:
            Formatted context string describing the current data
        """
        # Check if we have multi-file results from session state
        try:
            import streamlit as st
            if hasattr(st, 'session_state') and st.session_state.get('successful_results'):
                results = st.session_state['successful_results']
                return self._build_multi_file_context(results)
        except ImportError:
            pass
        
        # Fallback to single-file context
        if self.current_data is not None and isinstance(self.current_data, pd.DataFrame):
            # Structured data context
            context = f"Dataset Overview:\n"
            context += f"- Rows: {len(self.current_data)}\n"
            context += f"- Columns: {len(self.current_data.columns)}\n"
            context += f"- Column names: {', '.join(self.current_data.columns)}\n\n"

            # Data types and basic stats
            context += "Data Types:\n"
            for col in self.current_data.columns:
                context += f"- {col}: {self.current_data[col].dtype}\n"

            context += f"\nFirst 5 rows:\n{self.current_data.head().to_string()}\n"

            # Basic statistics
            if len(self.current_data) > 0:
                context += f"\nBasic Statistics:\n{self.current_data.describe().to_string()}\n"

            return context
        elif isinstance(self.current_file_info, dict) and "text" in self.current_file_info:
            # Unstructured data context
            text = self.current_file_info["text"]
            context = f"Document Content:\n"
            context += f"- Word count: {len(text.split())}\n"
            context += f"- Character count: {len(text)}\n\n"
            context += f"Content preview:\n{text[:1000]}..."
            return context
        else:
            return "No data loaded"

    def _build_multi_file_context(self, results: List[Dict[str, Any]]) -> str:
        """Build context string from multiple processed files."""
        if not results:
            return "No data loaded"
        
        context = f"Multi-File Analysis ({len(results)} files):\n\n"
        
        data_files = []
        text_files = []
        
        for i, result in enumerate(results):
            filename = result.get('original_filename', f'File_{i+1}')
            file_type = result.get('type', 'unknown')
            
            if 'data' in result and result['data'] is not None:
                df = result['data']
                data_files.append({
                    'filename': filename,
                    'type': file_type,
                    'data': df
                })
            elif 'text' in result:
                text_files.append({
                    'filename': filename,
                    'type': file_type,
                    'text': result['text']
                })
        
        # Summarize data files
        if data_files:
            context += f"Data Files ({len(data_files)}):\n"
            total_rows = 0
            all_columns = set()
            
            for df_info in data_files:
                df = df_info['data']
                rows = len(df)
                cols = list(df.columns)
                total_rows += rows
                all_columns.update(cols)
                
                context += f"- {df_info['filename']} ({df_info['type']}): {rows} rows, {len(cols)} columns\n"
                context += f"  Columns: {', '.join(cols[:5])}{'...' if len(cols) > 5 else ''}\n"
            
            context += f"\nAggregate Data Summary:\n"
            context += f"- Total rows across all files: {total_rows}\n"
            context += f"- Unique columns: {len(all_columns)}\n"
            context += f"- All columns: {', '.join(sorted(all_columns)[:10])}{'...' if len(all_columns) > 10 else ''}\n"
            
            # Show sample from first data file
            if data_files:
                first_df = data_files[0]['data']
                context += f"\nSample data from {data_files[0]['filename']}:\n"
                context += f"{first_df.head(3).to_string()}\n"
        
        # Summarize text files
        if text_files:
            context += f"\nText/Document Files ({len(text_files)}):\n"
            total_words = 0
            
            for text_info in text_files:
                text = text_info['text']
                word_count = len(text.split())
                total_words += word_count
                
                context += f"- {text_info['filename']} ({text_info['type']}): {word_count} words, {len(text)} chars\n"
                
                # Show preview of first text file
                if text_info == text_files[0]:
                    preview = text[:500] + "..." if len(text) > 500 else text
                    context += f"  Preview: {preview}\n"
            
            context += f"\nTotal words across text files: {total_words}\n"
        
        return context
