"""
AI Data Analyst Agent - A powerful AI-powered data analysis application.

This package provides comprehensive data analysis capabilities with support for
multiple file formats, AI-powered insights, and rich visualizations.
"""

__version__ = "1.0.0"
__author__ = "AI Data Analyst Team"
__license__ = "MIT"

from .core import DataAnalystAgent, AIBackend
from .processors import FileProcessor
from .visualization import VisualizationEngine
from .clients import LocalLMStudioClient, CloudAIClient

__all__ = [
    "DataAnalystAgent",
    "AIBackend", 
    "FileProcessor",
    "VisualizationEngine",
    "LocalLMStudioClient",
    "CloudAIClient"
]
