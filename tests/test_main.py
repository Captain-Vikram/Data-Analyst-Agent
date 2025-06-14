<<<<<<< HEAD
"""
Test suite for AI Data Analyst Agent
"""
import pytest
import tempfile
import os
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
import sys
import json

# Add the parent directory to the path to import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import FileProcessor, AIBackend, DataAnalystAgent, LocalLMStudioClient, CloudAIClient


class TestFileProcessor:
    """Test file processing functionality"""
    
    def test_process_csv_success(self):
        """Test successful CSV processing"""
        # Create a temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("name,age,city\nJohn,25,NYC\nJane,30,LA")
            temp_path = f.name
        
        try:
            result = FileProcessor.process_csv(temp_path)
            
            assert 'data' in result
            assert 'info' in result
            assert result['info']['rows'] == 2
            assert result['info']['columns'] == 3
            assert 'encoding' in result['info']
        finally:
            os.unlink(temp_path)
    
    def test_process_csv_invalid_file(self):
        """Test CSV processing with invalid file"""
        result = FileProcessor.process_csv('nonexistent.csv')
        assert 'error' in result
    
    def test_process_excel_mock(self):
        """Test Excel processing with mock data"""
        with patch('pandas.ExcelFile') as mock_excel:
            mock_file = Mock()
            mock_file.sheet_names = ['Sheet1']
            mock_excel.return_value = mock_file
            
            with patch('pandas.read_excel') as mock_read:
                mock_df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
                mock_read.return_value = mock_df
                
                result = FileProcessor.process_excel('test.xlsx')
                
                assert 'data' in result
                assert 'info' in result
                assert result['info']['rows'] == 3
                assert result['info']['columns'] == 2
    
    @patch('main.PyPDF2')
    def test_process_pdf_not_installed(self, mock_pypdf2):
        """Test PDF processing when PyPDF2 is not installed"""
        mock_pypdf2 = None
        
        with patch('main.PyPDF2', None):
            result = FileProcessor.process_pdf('test.pdf')
            
            assert 'error' in result
            assert 'PyPDF2 not installed' in result['error']
    
    @patch('main.pytesseract')
    def test_process_image_not_installed(self, mock_tesseract):
        """Test image processing when pytesseract is not installed"""
        with patch('main.pytesseract', None):
            result = FileProcessor.process_image('test.jpg')
            
            assert 'error' in result
            assert 'pytesseract not installed' in result['error']


class TestAIBackend:
    """Test AI backend functionality"""
    
    def test_backend_initialization_local(self):
        """Test local backend initialization"""
        backend = AIBackend(backend_type="local")
        
        assert backend.backend_type == "local"
        assert isinstance(backend.client, LocalLMStudioClient)
        assert backend.conversation_history == []
    
    def test_backend_initialization_cloud(self):
        """Test cloud backend initialization"""
        with patch.dict(os.environ, {'TOGETHER_API_KEY': 'test_key'}):
            with patch('main.together'):
                backend = AIBackend(backend_type="cloud")
                
                assert backend.backend_type == "cloud"
                assert isinstance(backend.client, CloudAIClient)
    
    def test_conversation_history_management(self):
        """Test conversation history operations"""
        backend = AIBackend(backend_type="local")
        
        # Test adding to history
        backend.conversation_history.append({
            "role": "user",
            "content": "Test question",
            "timestamp": "2025-06-14T12:00:00"
        })
        
        assert len(backend.conversation_history) == 1
        
        # Test clearing history
        backend.clear_conversation_history()
        assert len(backend.conversation_history) == 0
    
    def test_get_conversation_summary(self):
        """Test conversation summary generation"""
        backend = AIBackend(backend_type="local")
        
        # Test empty history
        summary = backend.get_conversation_summary()
        assert "No conversation history" in summary
        
        # Test with history
        backend.conversation_history = [
            {"role": "user", "content": "Question 1", "timestamp": "2025-06-14T12:00:00"},
            {"role": "assistant", "content": "Answer 1", "timestamp": "2025-06-14T12:01:00"}
        ]
        
        summary = backend.get_conversation_summary()
        assert "Total questions asked: 1" in summary
        assert "Total responses given: 1" in summary
    
    def test_get_similar_questions(self):
        """Test similar questions finding"""
        backend = AIBackend(backend_type="local")
        
        # Test empty history
        similar = backend.get_similar_questions("test question")
        assert similar == []
        
        # Test with history
        backend.conversation_history = [
            {"role": "user", "content": "What is the data distribution?", "timestamp": "2025-06-14T12:00:00"},
            {"role": "user", "content": "How is the data distributed?", "timestamp": "2025-06-14T12:02:00"}
        ]
        
        similar = backend.get_similar_questions("Show me data distribution", limit=2)
        assert len(similar) <= 2


class TestLocalLMStudioClient:
    """Test Local LM Studio client"""
    
    def test_client_initialization(self):
        """Test client initialization"""
        client = LocalLMStudioClient()
        
        assert client.base_url == "http://localhost:1234"
        assert client.model_name == "meta-llama-3.1-8b-instruct"
    
    @patch('requests.get')
    def test_check_connection_success(self, mock_get):
        """Test successful connection check"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        client = LocalLMStudioClient()
        assert client.check_connection() == True
    
    @patch('requests.get')
    def test_check_connection_failure(self, mock_get):
        """Test failed connection check"""
        mock_get.side_effect = Exception("Connection failed")
        
        client = LocalLMStudioClient()
        assert client.check_connection() == False
    
    @patch('requests.post')
    def test_chat_completion_success(self, mock_post):
        """Test successful chat completion"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'Test response'}}]
        }
        mock_post.return_value = mock_response
        
        client = LocalLMStudioClient()
        messages = [{"role": "user", "content": "Test message"}]
        
        response = client.chat_completion(messages)
        assert response == 'Test response'
    
    @patch('requests.post')
    def test_chat_completion_failure(self, mock_post):
        """Test failed chat completion"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        
        client = LocalLMStudioClient()
        messages = [{"role": "user", "content": "Test message"}]
        
        with pytest.raises(Exception):
            client.chat_completion(messages)


class TestCloudAIClient:
    """Test Cloud AI client"""
    
    def test_client_initialization_no_key(self):
        """Test client initialization without API key"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError):
                CloudAIClient()
    
    def test_client_initialization_no_library(self):
        """Test client initialization without together library"""
        with patch.dict(os.environ, {'TOGETHER_API_KEY': 'test_key'}):
            with patch('main.together', None):
                with pytest.raises(ImportError):
                    CloudAIClient()
    
    def test_format_messages(self):
        """Test message formatting"""
        with patch.dict(os.environ, {'TOGETHER_API_KEY': 'test_key'}):
            with patch('main.together'):
                client = CloudAIClient()
                
                messages = [
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": "Hello"},
                    {"role": "assistant", "content": "Hi there!"}
                ]
                
                formatted = client._format_messages(messages)
                assert "System: You are a helpful assistant" in formatted
                assert "Human: Hello" in formatted
                assert "Assistant: Hi there!" in formatted


class TestDataAnalystAgent:
    """Test main application class"""
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        agent = DataAnalystAgent(backend_type="local")
        
        assert agent.backend_type == "local"
        assert isinstance(agent.ai_backend, AIBackend)
        assert isinstance(agent.file_processor, FileProcessor)
        assert agent.current_data is None
        assert agent.current_file_info is None
    
    def test_process_file_not_found(self):
        """Test processing non-existent file"""
        agent = DataAnalystAgent()
        result = agent.process_file('nonexistent.txt')
        
        assert 'error' in result
        assert 'File not found' in result['error']
    
    def test_process_unsupported_format(self):
        """Test processing unsupported file format"""
        agent = DataAnalystAgent()
        
        # Create a temporary file with unsupported extension
        with tempfile.NamedTemporaryFile(suffix='.xyz', delete=False) as f:
            f.write(b'test content')
            temp_path = f.name
        
        try:
            result = agent.process_file(temp_path)
            assert 'error' in result
            assert 'Unsupported file format' in result['error']
        finally:
            os.unlink(temp_path)
    
    def test_process_text_file(self):
        """Test processing text file"""
        agent = DataAnalystAgent()
        
        # Create a temporary text file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write('This is a test file with some content.')
            temp_path = f.name
        
        try:
            result = agent.process_file(temp_path)
            
            assert 'text' in result
            assert 'info' in result
            assert result['info']['word_count'] == 8
            assert agent.current_file_info == result
        finally:
            os.unlink(temp_path)
    
    def test_get_data_context_no_data(self):
        """Test getting data context with no data loaded"""
        agent = DataAnalystAgent()
        context = agent.get_data_context()
        
        assert context == "No data loaded"
    
    def test_get_data_context_with_structured_data(self):
        """Test getting data context with structured data"""
        agent = DataAnalystAgent()
        
        # Mock structured data
        agent.current_data = pd.DataFrame({
            'A': [1, 2, 3],
            'B': ['x', 'y', 'z']
        })
        
        context = agent.get_data_context()
        
        assert "Dataset Overview:" in context
        assert "Rows: 3" in context
        assert "Columns: 2" in context
        assert "Column names: A, B" in context
    
    def test_get_data_context_with_text_data(self):
        """Test getting data context with text data"""
        agent = DataAnalystAgent()
        
        # Mock text data
        agent.current_file_info = {
            'text': 'This is a sample text document with multiple words.'
        }
        
        context = agent.get_data_context()
        
        assert "Document Content:" in context
        assert "Word count: 9" in context
        assert "Character count:" in context
        assert "Content preview:" in context


class TestIntegration:
    """Integration tests"""
    
    def test_csv_to_analysis_workflow(self):
        """Test complete workflow: CSV upload -> processing -> analysis"""
        # Create a sample CSV
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("product,price,sales\nWidget A,10.50,100\nWidget B,15.75,85\nWidget C,8.25,120")
            temp_path = f.name
        
        try:
            agent = DataAnalystAgent(backend_type="local")
            
            # Process file
            result = agent.process_file(temp_path)
            
            assert 'data' in result
            assert not result['data'].empty
            assert len(result['data']) == 3
            assert list(result['data'].columns) == ['product', 'price', 'sales']
            
            # Check data context generation
            context = agent.get_data_context()
            assert "Dataset Overview:" in context
            assert "Rows: 3" in context
            assert "Columns: 3" in context
            
        finally:
            os.unlink(temp_path)
    
    @patch('requests.get')
    def test_backend_switching(self, mock_get):
        """Test switching between backends"""
        # Mock LM Studio connection
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        agent = DataAnalystAgent(backend_type="local")
        assert agent.backend_type == "local"
        assert agent.ai_backend.client.check_connection() == True
        
        # Switch to cloud backend (would require API key in real scenario)
        # This test just verifies the structure


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
=======
"""
Test suite for AI Data Analyst Agent
"""
import pytest
import tempfile
import os
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
import sys
import json

# Add the parent directory to the path to import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import FileProcessor, AIBackend, DataAnalystAgent, LocalLMStudioClient, CloudAIClient


class TestFileProcessor:
    """Test file processing functionality"""
    
    def test_process_csv_success(self):
        """Test successful CSV processing"""
        # Create a temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("name,age,city\nJohn,25,NYC\nJane,30,LA")
            temp_path = f.name
        
        try:
            result = FileProcessor.process_csv(temp_path)
            
            assert 'data' in result
            assert 'info' in result
            assert result['info']['rows'] == 2
            assert result['info']['columns'] == 3
            assert 'encoding' in result['info']
        finally:
            os.unlink(temp_path)
    
    def test_process_csv_invalid_file(self):
        """Test CSV processing with invalid file"""
        result = FileProcessor.process_csv('nonexistent.csv')
        assert 'error' in result
    
    def test_process_excel_mock(self):
        """Test Excel processing with mock data"""
        with patch('pandas.ExcelFile') as mock_excel:
            mock_file = Mock()
            mock_file.sheet_names = ['Sheet1']
            mock_excel.return_value = mock_file
            
            with patch('pandas.read_excel') as mock_read:
                mock_df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
                mock_read.return_value = mock_df
                
                result = FileProcessor.process_excel('test.xlsx')
                
                assert 'data' in result
                assert 'info' in result
                assert result['info']['rows'] == 3
                assert result['info']['columns'] == 2
    
    @patch('main.PyPDF2')
    def test_process_pdf_not_installed(self, mock_pypdf2):
        """Test PDF processing when PyPDF2 is not installed"""
        mock_pypdf2 = None
        
        with patch('main.PyPDF2', None):
            result = FileProcessor.process_pdf('test.pdf')
            
            assert 'error' in result
            assert 'PyPDF2 not installed' in result['error']
    
    @patch('main.pytesseract')
    def test_process_image_not_installed(self, mock_tesseract):
        """Test image processing when pytesseract is not installed"""
        with patch('main.pytesseract', None):
            result = FileProcessor.process_image('test.jpg')
            
            assert 'error' in result
            assert 'pytesseract not installed' in result['error']


class TestAIBackend:
    """Test AI backend functionality"""
    
    def test_backend_initialization_local(self):
        """Test local backend initialization"""
        backend = AIBackend(backend_type="local")
        
        assert backend.backend_type == "local"
        assert isinstance(backend.client, LocalLMStudioClient)
        assert backend.conversation_history == []
    
    def test_backend_initialization_cloud(self):
        """Test cloud backend initialization"""
        with patch.dict(os.environ, {'TOGETHER_API_KEY': 'test_key'}):
            with patch('main.together'):
                backend = AIBackend(backend_type="cloud")
                
                assert backend.backend_type == "cloud"
                assert isinstance(backend.client, CloudAIClient)
    
    def test_conversation_history_management(self):
        """Test conversation history operations"""
        backend = AIBackend(backend_type="local")
        
        # Test adding to history
        backend.conversation_history.append({
            "role": "user",
            "content": "Test question",
            "timestamp": "2025-06-14T12:00:00"
        })
        
        assert len(backend.conversation_history) == 1
        
        # Test clearing history
        backend.clear_conversation_history()
        assert len(backend.conversation_history) == 0
    
    def test_get_conversation_summary(self):
        """Test conversation summary generation"""
        backend = AIBackend(backend_type="local")
        
        # Test empty history
        summary = backend.get_conversation_summary()
        assert "No conversation history" in summary
        
        # Test with history
        backend.conversation_history = [
            {"role": "user", "content": "Question 1", "timestamp": "2025-06-14T12:00:00"},
            {"role": "assistant", "content": "Answer 1", "timestamp": "2025-06-14T12:01:00"}
        ]
        
        summary = backend.get_conversation_summary()
        assert "Total questions asked: 1" in summary
        assert "Total responses given: 1" in summary
    
    def test_get_similar_questions(self):
        """Test similar questions finding"""
        backend = AIBackend(backend_type="local")
        
        # Test empty history
        similar = backend.get_similar_questions("test question")
        assert similar == []
        
        # Test with history
        backend.conversation_history = [
            {"role": "user", "content": "What is the data distribution?", "timestamp": "2025-06-14T12:00:00"},
            {"role": "user", "content": "How is the data distributed?", "timestamp": "2025-06-14T12:02:00"}
        ]
        
        similar = backend.get_similar_questions("Show me data distribution", limit=2)
        assert len(similar) <= 2


class TestLocalLMStudioClient:
    """Test Local LM Studio client"""
    
    def test_client_initialization(self):
        """Test client initialization"""
        client = LocalLMStudioClient()
        
        assert client.base_url == "http://localhost:1234"
        assert client.model_name == "meta-llama-3.1-8b-instruct"
    
    @patch('requests.get')
    def test_check_connection_success(self, mock_get):
        """Test successful connection check"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        client = LocalLMStudioClient()
        assert client.check_connection() == True
    
    @patch('requests.get')
    def test_check_connection_failure(self, mock_get):
        """Test failed connection check"""
        mock_get.side_effect = Exception("Connection failed")
        
        client = LocalLMStudioClient()
        assert client.check_connection() == False
    
    @patch('requests.post')
    def test_chat_completion_success(self, mock_post):
        """Test successful chat completion"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'Test response'}}]
        }
        mock_post.return_value = mock_response
        
        client = LocalLMStudioClient()
        messages = [{"role": "user", "content": "Test message"}]
        
        response = client.chat_completion(messages)
        assert response == 'Test response'
    
    @patch('requests.post')
    def test_chat_completion_failure(self, mock_post):
        """Test failed chat completion"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        
        client = LocalLMStudioClient()
        messages = [{"role": "user", "content": "Test message"}]
        
        with pytest.raises(Exception):
            client.chat_completion(messages)


class TestCloudAIClient:
    """Test Cloud AI client"""
    
    def test_client_initialization_no_key(self):
        """Test client initialization without API key"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError):
                CloudAIClient()
    
    def test_client_initialization_no_library(self):
        """Test client initialization without together library"""
        with patch.dict(os.environ, {'TOGETHER_API_KEY': 'test_key'}):
            with patch('main.together', None):
                with pytest.raises(ImportError):
                    CloudAIClient()
    
    def test_format_messages(self):
        """Test message formatting"""
        with patch.dict(os.environ, {'TOGETHER_API_KEY': 'test_key'}):
            with patch('main.together'):
                client = CloudAIClient()
                
                messages = [
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": "Hello"},
                    {"role": "assistant", "content": "Hi there!"}
                ]
                
                formatted = client._format_messages(messages)
                assert "System: You are a helpful assistant" in formatted
                assert "Human: Hello" in formatted
                assert "Assistant: Hi there!" in formatted


class TestDataAnalystAgent:
    """Test main application class"""
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        agent = DataAnalystAgent(backend_type="local")
        
        assert agent.backend_type == "local"
        assert isinstance(agent.ai_backend, AIBackend)
        assert isinstance(agent.file_processor, FileProcessor)
        assert agent.current_data is None
        assert agent.current_file_info is None
    
    def test_process_file_not_found(self):
        """Test processing non-existent file"""
        agent = DataAnalystAgent()
        result = agent.process_file('nonexistent.txt')
        
        assert 'error' in result
        assert 'File not found' in result['error']
    
    def test_process_unsupported_format(self):
        """Test processing unsupported file format"""
        agent = DataAnalystAgent()
        
        # Create a temporary file with unsupported extension
        with tempfile.NamedTemporaryFile(suffix='.xyz', delete=False) as f:
            f.write(b'test content')
            temp_path = f.name
        
        try:
            result = agent.process_file(temp_path)
            assert 'error' in result
            assert 'Unsupported file format' in result['error']
        finally:
            os.unlink(temp_path)
    
    def test_process_text_file(self):
        """Test processing text file"""
        agent = DataAnalystAgent()
        
        # Create a temporary text file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write('This is a test file with some content.')
            temp_path = f.name
        
        try:
            result = agent.process_file(temp_path)
            
            assert 'text' in result
            assert 'info' in result
            assert result['info']['word_count'] == 8
            assert agent.current_file_info == result
        finally:
            os.unlink(temp_path)
    
    def test_get_data_context_no_data(self):
        """Test getting data context with no data loaded"""
        agent = DataAnalystAgent()
        context = agent.get_data_context()
        
        assert context == "No data loaded"
    
    def test_get_data_context_with_structured_data(self):
        """Test getting data context with structured data"""
        agent = DataAnalystAgent()
        
        # Mock structured data
        agent.current_data = pd.DataFrame({
            'A': [1, 2, 3],
            'B': ['x', 'y', 'z']
        })
        
        context = agent.get_data_context()
        
        assert "Dataset Overview:" in context
        assert "Rows: 3" in context
        assert "Columns: 2" in context
        assert "Column names: A, B" in context
    
    def test_get_data_context_with_text_data(self):
        """Test getting data context with text data"""
        agent = DataAnalystAgent()
        
        # Mock text data
        agent.current_file_info = {
            'text': 'This is a sample text document with multiple words.'
        }
        
        context = agent.get_data_context()
        
        assert "Document Content:" in context
        assert "Word count: 9" in context
        assert "Character count:" in context
        assert "Content preview:" in context


class TestIntegration:
    """Integration tests"""
    
    def test_csv_to_analysis_workflow(self):
        """Test complete workflow: CSV upload -> processing -> analysis"""
        # Create a sample CSV
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("product,price,sales\nWidget A,10.50,100\nWidget B,15.75,85\nWidget C,8.25,120")
            temp_path = f.name
        
        try:
            agent = DataAnalystAgent(backend_type="local")
            
            # Process file
            result = agent.process_file(temp_path)
            
            assert 'data' in result
            assert not result['data'].empty
            assert len(result['data']) == 3
            assert list(result['data'].columns) == ['product', 'price', 'sales']
            
            # Check data context generation
            context = agent.get_data_context()
            assert "Dataset Overview:" in context
            assert "Rows: 3" in context
            assert "Columns: 3" in context
            
        finally:
            os.unlink(temp_path)
    
    @patch('requests.get')
    def test_backend_switching(self, mock_get):
        """Test switching between backends"""
        # Mock LM Studio connection
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        agent = DataAnalystAgent(backend_type="local")
        assert agent.backend_type == "local"
        assert agent.ai_backend.client.check_connection() == True
        
        # Switch to cloud backend (would require API key in real scenario)
        # This test just verifies the structure


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
>>>>>>> 0f3fe5ae72e1e543da9128827c74b2ea0a92d9d6
