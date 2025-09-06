"""
AI client implementations for the Data Analyst Agent.

This module contains client classes for interacting with different AI backends
including local LM Studio and cloud-based services like Google Gemini AI.
"""

import os
from typing import Dict, Any, Optional
import mimetypes
import warnings
warnings.filterwarnings('ignore')

# Import for local LM Studio - commented out for cloud deployment
# import requests
# import json

# Import for Google Gemini AI REST API
import requests
import json


# class LocalLMStudioClient:
#     """
#     Client for local LM Studio integration - COMMENTED OUT FOR CLOUD DEPLOYMENT.
#     
#     This class provides methods to interact with a local LM Studio server
#     for AI-powered data analysis and question answering.
#     """
#     
#     def __init__(self, base_url: str = "http://localhost:1234"):
#         """
#         Initialize the LM Studio client.
#         
#         Args:
#             base_url: Base URL of the LM Studio server
#         """
#         self.base_url = base_url.rstrip('/')
#         self.headers = {
#             "Content-Type": "application/json"
#         }
#     
#     def check_connection(self) -> bool:
#         """
#         Check if LM Studio server is available.
#         
#         Returns:
#             True if server is available, False otherwise
#         """
#         try:
#             response = requests.get(f"{self.base_url}/v1/models", timeout=5)
#             return response.status_code == 200
#         except Exception:
#             return False
#     
#     def get_models(self) -> Dict[str, Any]:
#         """
#         Get available models from LM Studio.
#         
#         Returns:
#             Dictionary containing model information
#         """
#         try:
#             response = requests.get(f"{self.base_url}/v1/models", timeout=10)
#             if response.status_code == 200:
#                 return response.json()
#             else:
#                 return {"error": f"HTTP {response.status_code}"}
#         except Exception as e:
#             return {"error": str(e)}
#     
#     def answer_question(self, question: str, context: str = "") -> str:
#         """
#         Generate an answer using the local LM Studio model.
#         
#         Args:
#             question: The question to answer
#             context: Additional context about the data
#             
#         Returns:
#             The AI-generated response
#         """
#         try:
#             # Prepare the prompt
#             if context:
#                 prompt = f"""You are a professional data analyst. Based on the following data context, answer the user's question with insights, patterns, and actionable recommendations.
# 
# Data Context:
# {context}
# 
# User Question: {question}
# 
# Please provide a comprehensive analysis with:
# 1. Direct answer to the question
# 2. Key insights from the data
# 3. Patterns or trends you notice
# 4. Actionable recommendations
# 5. Any concerns or limitations
# 
# Response:"""
#             else:
#                 prompt = f"""You are a professional data analyst. Please answer the following question:
# 
# {question}
# 
# Provide a helpful and insightful response."""
#             
#             # Prepare the request
#             data = {
#                 "model": "local-model",
#                 "messages": [
#                     {"role": "user", "content": prompt}
#                 ],
#                 "temperature": 0.7,
#                 "max_tokens": 1000,
#                 "stream": False
#             }
#             
#             # Make the request
#             response = requests.post(
#                 f"{self.base_url}/v1/chat/completions",
#                 headers=self.headers,
#                 json=data,
#                 timeout=60
#             )
#             
#             if response.status_code == 200:
#                 result = response.json()
#                 return result['choices'][0]['message']['content']
#             else:
#                 return f"Error: HTTP {response.status_code} - {response.text}"
#                 
#         except requests.exceptions.ConnectionError:
#             return "Error: Cannot connect to LM Studio server. Please ensure LM Studio is running and the server is started."
#         except requests.exceptions.Timeout:
#             return "Error: Request timed out. The model might be processing a complex query."
#         except Exception as e:
#             return f"Error generating response: {str(e)}"


# LocalLMStudioClient is commented out for cloud deployment - using Google Gemini AI only


class CloudAIClient:
    """
    Client for Google Gemini AI using the REST API.

    Provides methods to interact with Google Gemini AI for data analysis and Q&A
    with selectable models, plus optional File API support.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        """
        Initialize the Google Gemini AI client using REST API.

        Args:
            api_key: Google AI API key
            model_name: Specific model to use (defaults to gemini-2.5-pro)
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google AI API key is required for cloud AI services")

        # REST API base URLs
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.upload_url = "https://generativelanguage.googleapis.com/upload/v1beta/files"

        # Set the model name with latest available Google AI models
        self.available_models = {
            "gemini-2.5-pro": "Gemini 2.5 Pro - Top-end reasoning and multimodal model",
            "gemini-2.5-flash": "Gemini 2.5 Flash - Balanced price-performance",
            "gemini-2.5-flash-lite": "Gemini 2.5 Flash Lite - Cost-efficient, high throughput",
            "gemini-2.0-flash-experimental": "Gemini 2.0 Flash (Experimental) - Early release with better benchmarks",
            "gemini-2.0-flash": "Gemini 2.0 Flash - New multimodal model with advanced capabilities",
            "gemini-2.0-flash-lite": "Gemini 2.0 Flash Lite - Optimized for low latency and cost",
        }

        self.model_name = model_name or "gemini-2.5-pro"  # Default to latest and most capable model

        # Validate model name
        if self.model_name not in self.available_models:
            print(f"Warning: Model {self.model_name} not in available models. Using default.")
            self.model_name = "gemini-2.5-pro"

        # Headers for REST API calls to generateContent
        self.headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": self.api_key,
        }

    def check_connection(self) -> bool:
        """Check basic connectivity to the Gemini API."""
        try:
            url = f"{self.base_url}/{self.model_name}:generateContent"
            payload = {"contents": [{"parts": [{"text": "Hello"}]}]}
            response = requests.post(url, headers=self.headers, json=payload, timeout=10)
            return response.status_code == 200
        except Exception:
            return False
    
    def get_models(self) -> Dict[str, Any]:
        """
        Get available models from Google Gemini AI service.
        
        Returns:
            Dictionary containing model information
        """
        try:
            models_list = []
            for model_id, display_name in self.available_models.items():
                models_list.append({
                    "name": model_id,
                    "display_name": display_name,
                    "description": f"Google {display_name} AI Model"
                })
            
            return {
                "models": models_list,
                "current_model": self.model_name
            }
        except Exception as e:
            return {"error": str(e)}
    
    def upload_file(self, file_path: str) -> Dict[str, Any]:
        """
        Upload a file to Gemini File API and return its metadata.

        Returns a dict with at least {'name': file_uri, 'mimeType': mime}
        or {'error': '...'} on failure.
        """
        try:
            if not os.path.exists(file_path):
                return {"error": "File not found"}

            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = "application/octet-stream"

            # Upload using raw protocol
            headers = {
                "X-goog-api-key": self.api_key,
                "X-Goog-Upload-Protocol": "raw",
                "Content-Type": mime_type,
            }
            with open(file_path, "rb") as f:
                resp = requests.post(
                    f"{self.upload_url}?key={self.api_key}",
                    headers=headers,
                    data=f.read(),
                    timeout=120,
                )

            if resp.status_code in (200, 201):
                data = resp.json()
                # Expecting fields: name (file_uri), mimeType
                return data
            else:
                return {"error": f"HTTP {resp.status_code}: {resp.text}"}
        except Exception as e:
            return {"error": str(e)}

    def answer_question(self, question: str, context: str = "", file_uri: Optional[str] = None, mime_type: Optional[str] = None) -> str:
        """
        Generate an answer using Google Gemini AI REST API.
        
        Args:
            question: The question to answer
            context: Additional context about the data
            file_uri: Optional Gemini file URI to include as multimodal input
            mime_type: Optional MIME type associated with file_uri
            
        Returns:
            The AI-generated response
        """
        try:
            # Prepare the prompt
            if context:
                prompt = f"""You are a professional data analyst. Based on the following data context, answer the user's question with insights, patterns, and actionable recommendations.

Data Context:
{context}

User Question: {question}

Please provide a comprehensive analysis with:
1. Direct answer to the question
2. Key insights from the data
3. Patterns or trends you notice
4. Actionable recommendations
5. Any concerns or limitations

Response:"""
            else:
                prompt = f"""You are a professional data analyst. Please answer the following question:

{question}

Provide a helpful and insightful response."""

            # Construct contents with optional file reference
            parts: list[Any] = []
            if file_uri:
                file_part: Dict[str, Any] = {"file_data": {"file_uri": file_uri}}
                if mime_type:
                    file_part["file_data"]["mime_type"] = mime_type
                parts.append(file_part)
            parts.append({"text": prompt})

            url = f"{self.base_url}/{self.model_name}:generateContent"
            payload = {"contents": [{"parts": parts}]}
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    if 'content' in result['candidates'][0]:
                        if 'parts' in result['candidates'][0]['content']:
                            return result['candidates'][0]['content']['parts'][0]['text']
                
                return "Error: Unexpected response format from Gemini API"
            else:
                return f"Error: HTTP {response.status_code} - {response.text}"
                
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Google Gemini API. Please check your internet connection."
        except requests.exceptions.Timeout:
            return "Error: Request timed out. The model might be processing a complex query."
        except Exception as e:
            # Handle various types of errors
            error_message = str(e)
            if "API_KEY" in error_message.upper():
                return "Error: Invalid or missing Google AI API key. Please check your API key."
            elif "QUOTA" in error_message.upper():
                return "Error: API quota exceeded. Please check your Google AI Studio quota."
            elif "SAFETY" in error_message.upper():
                return "Error: Content was blocked by safety filters. Please try rephrasing your question."
            else:
                return f"Error generating response: {error_message}"
