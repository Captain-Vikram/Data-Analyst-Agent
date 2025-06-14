"""
AI client implementations for the Data Analyst Agent.

This module contains client classes for interacting with different AI backends
including local LM Studio and cloud-based services like Together.ai.
"""

import requests
import json
import os
from typing import Dict, Any, Optional
import warnings
warnings.filterwarnings('ignore')


class LocalLMStudioClient:
    """
    Client for local LM Studio integration.
    
    This class provides methods to interact with a local LM Studio server
    for AI-powered data analysis and question answering.
    """
    
    def __init__(self, base_url: str = "http://localhost:1234"):
        """
        Initialize the LM Studio client.
        
        Args:
            base_url: Base URL of the LM Studio server
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Content-Type": "application/json"
        }
    
    def check_connection(self) -> bool:
        """
        Check if LM Studio server is available.
        
        Returns:
            True if server is available, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/v1/models", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def get_models(self) -> Dict[str, Any]:
        """
        Get available models from LM Studio.
        
        Returns:
            Dictionary containing model information
        """
        try:
            response = requests.get(f"{self.base_url}/v1/models", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def answer_question(self, question: str, context: str = "") -> str:
        """
        Generate an answer using the local LM Studio model.
        
        Args:
            question: The question to answer
            context: Additional context about the data
            
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
            
            # Prepare the request
            data = {
                "model": "local-model",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000,
                "stream": False
            }
            
            # Make the request
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers=self.headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Error: HTTP {response.status_code} - {response.text}"
                
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to LM Studio server. Please ensure LM Studio is running and the server is started."
        except requests.exceptions.Timeout:
            return "Error: Request timed out. The model might be processing a complex query."
        except Exception as e:
            return f"Error generating response: {str(e)}"


class CloudAIClient:
    """
    Client for cloud AI services (Together.ai).
    
    This class provides methods to interact with cloud-based AI services
    for data analysis and question answering.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the cloud AI client.
        
        Args:
            api_key: API key for the cloud service
        """
        self.api_key = api_key or os.getenv("TOGETHER_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required for cloud AI services")
        
        self.base_url = "https://api.together.xyz/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def check_connection(self) -> bool:
        """
        Check if the cloud service is available.
        
        Returns:
            True if service is available, False otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def get_models(self) -> Dict[str, Any]:
        """
        Get available models from the cloud service.
        
        Returns:
            Dictionary containing model information
        """
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def answer_question(self, question: str, context: str = "") -> str:
        """
        Generate an answer using the cloud AI service.
        
        Args:
            question: The question to answer
            context: Additional context about the data
            
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
            
            # Prepare the request
            data = {
                "model": "meta-llama/Llama-2-70b-chat-hf",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000,
                "stream": False
            }
            
            # Make the request
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Error: HTTP {response.status_code} - {response.text}"
                
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to cloud AI service. Please check your internet connection."
        except requests.exceptions.Timeout:
            return "Error: Request timed out. Please try again."
        except Exception as e:
            return f"Error generating response: {str(e)}"
