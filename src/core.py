<<<<<<< HEAD
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

from processors import FileProcessor
from clients import LocalLMStudioClient, CloudAIClient


class AIBackend:
    """
    Unified AI backend supporting both local and cloud providers.
    
    This class provides a consistent interface for interacting with both
    local LM Studio and cloud-based AI services like Together.ai.
    """
    
    def __init__(self, backend_type: str = "local", api_key: str = None):
        """
        Initialize the AI backend.
        
        Args:
            backend_type: Type of backend ("local" or "cloud")
            api_key: API key for cloud services (optional)
        """
        self.backend_type = backend_type
        self.conversation_history = []
        
        try:
            if backend_type == "cloud" and api_key:
                self.client = CloudAIClient(api_key=api_key)
            elif backend_type == "local":
                self.client = LocalLMStudioClient()
            else:
                # Fallback to local
                self.client = LocalLMStudioClient()
                self.backend_type = "local"
        except Exception as e:
            print(f"Warning: Failed to initialize {backend_type} backend: {e}")
            # Fallback to local backend
            self.client = LocalLMStudioClient()
            self.backend_type = "local"
    
    def answer_question(self, question: str, context: str = "") -> str:
        """
        Answer a question using the configured AI backend.
        
        Args:
            question: The question to answer
            context: Additional context about the data
            
        Returns:
            The AI-generated response
        """
        try:
            response = self.client.answer_question(question, context)
            
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
    
    def __init__(self, backend_type: str = "local", api_key: str = None):
        """
        Initialize the Data Analyst Agent.
        
        Args:
            backend_type: Type of AI backend to use
            api_key: API key for cloud services (optional)
        """
        self.backend_type = backend_type
        self.file_processor = FileProcessor()
        self.ai_backend = AIBackend(backend_type, api_key)
        self.current_data = None
        self.current_file_info = None
    
    def update_backend(self, backend_type: str, api_key: str = None):
        """
        Update the AI backend with new configuration.
        
        Args:
            backend_type: New backend type
            api_key: API key for cloud services (optional)
        """
        self.backend_type = backend_type
        self.ai_backend = AIBackend(backend_type, api_key=api_key)
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process uploaded file based on extension.
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            Dictionary containing processed data and metadata
        """
        if not os.path.exists(file_path):
            return {'error': 'File not found'}
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.csv':
            result = self.file_processor.process_csv(file_path)
        elif file_ext in ['.xlsx', '.xls']:
            result = self.file_processor.process_excel(file_path)
        elif file_ext == '.pdf':
            result = self.file_processor.process_pdf(file_path)
        elif file_ext == '.docx':
            result = self.file_processor.process_docx(file_path)
        elif file_ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            result = self.file_processor.process_image(file_path)
        elif file_ext == '.txt':
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                result = {'text': content, 'info': {'word_count': len(content.split())}}
            except Exception as e:
                result = {'error': f'Text file processing failed: {str(e)}'}
        else:
            result = {'error': f'Unsupported file format: {file_ext}'}
        
        if 'data' in result:
            self.current_data = result['data']
            self.current_file_info = result.get('info', {})
        elif 'text' in result:
            self.current_file_info = result
        
        return result
    
    def get_data_context(self) -> str:
        """
        Generate context string from current data.
        
        Returns:
            Formatted context string describing the current data
        """
        if self.current_data is not None:
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
        elif self.current_file_info and 'text' in self.current_file_info:
            # Unstructured data context
            text = self.current_file_info['text']
            context = f"Document Content:\n"
            context += f"- Word count: {len(text.split())}\n"
            context += f"- Character count: {len(text)}\n\n"
            context += f"Content preview:\n{text[:1000]}..."
            return context
        else:
            return "No data loaded"
=======
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

from processors import FileProcessor
from clients import LocalLMStudioClient, CloudAIClient


class AIBackend:
    """
    Unified AI backend supporting both local and cloud providers.
    
    This class provides a consistent interface for interacting with both
    local LM Studio and cloud-based AI services like Together.ai.
    """
    
    def __init__(self, backend_type: str = "local", api_key: str = None):
        """
        Initialize the AI backend.
        
        Args:
            backend_type: Type of backend ("local" or "cloud")
            api_key: API key for cloud services (optional)
        """
        self.backend_type = backend_type
        self.conversation_history = []
        
        try:
            if backend_type == "cloud" and api_key:
                self.client = CloudAIClient(api_key=api_key)
            elif backend_type == "local":
                self.client = LocalLMStudioClient()
            else:
                # Fallback to local
                self.client = LocalLMStudioClient()
                self.backend_type = "local"
        except Exception as e:
            print(f"Warning: Failed to initialize {backend_type} backend: {e}")
            # Fallback to local backend
            self.client = LocalLMStudioClient()
            self.backend_type = "local"
    
    def answer_question(self, question: str, context: str = "") -> str:
        """
        Answer a question using the configured AI backend.
        
        Args:
            question: The question to answer
            context: Additional context about the data
            
        Returns:
            The AI-generated response
        """
        try:
            response = self.client.answer_question(question, context)
            
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
    
    def __init__(self, backend_type: str = "local", api_key: str = None):
        """
        Initialize the Data Analyst Agent.
        
        Args:
            backend_type: Type of AI backend to use
            api_key: API key for cloud services (optional)
        """
        self.backend_type = backend_type
        self.file_processor = FileProcessor()
        self.ai_backend = AIBackend(backend_type, api_key)
        self.current_data = None
        self.current_file_info = None
    
    def update_backend(self, backend_type: str, api_key: str = None):
        """
        Update the AI backend with new configuration.
        
        Args:
            backend_type: New backend type
            api_key: API key for cloud services (optional)
        """
        self.backend_type = backend_type
        self.ai_backend = AIBackend(backend_type, api_key=api_key)
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process uploaded file based on extension.
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            Dictionary containing processed data and metadata
        """
        if not os.path.exists(file_path):
            return {'error': 'File not found'}
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.csv':
            result = self.file_processor.process_csv(file_path)
        elif file_ext in ['.xlsx', '.xls']:
            result = self.file_processor.process_excel(file_path)
        elif file_ext == '.pdf':
            result = self.file_processor.process_pdf(file_path)
        elif file_ext == '.docx':
            result = self.file_processor.process_docx(file_path)
        elif file_ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            result = self.file_processor.process_image(file_path)
        elif file_ext == '.txt':
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                result = {'text': content, 'info': {'word_count': len(content.split())}}
            except Exception as e:
                result = {'error': f'Text file processing failed: {str(e)}'}
        else:
            result = {'error': f'Unsupported file format: {file_ext}'}
        
        if 'data' in result:
            self.current_data = result['data']
            self.current_file_info = result.get('info', {})
        elif 'text' in result:
            self.current_file_info = result
        
        return result
    
    def get_data_context(self) -> str:
        """
        Generate context string from current data.
        
        Returns:
            Formatted context string describing the current data
        """
        if self.current_data is not None:
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
        elif self.current_file_info and 'text' in self.current_file_info:
            # Unstructured data context
            text = self.current_file_info['text']
            context = f"Document Content:\n"
            context += f"- Word count: {len(text.split())}\n"
            context += f"- Character count: {len(text)}\n\n"
            context += f"Content preview:\n{text[:1000]}..."
            return context
        else:
            return "No data loaded"
>>>>>>> 0f3fe5ae72e1e543da9128827c74b2ea0a92d9d6
