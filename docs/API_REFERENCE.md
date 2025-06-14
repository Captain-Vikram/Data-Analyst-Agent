# 🔌 API Reference

Complete API reference for the AI Data Analyst Agent components.

## 📋 Table of Contents

1. [Core Classes](#core-classes)
2. [File Processors](#file-processors)
3. [Visualization Engine](#visualization-engine)
4. [AI Clients](#ai-clients)
5. [Error Handling](#error-handling)
6. [Type Definitions](#type-definitions)

## 🏗️ Core Classes

### DataAnalystAgent

The main orchestrator class for all data analysis operations.

```python
class DataAnalystAgent:
    def __init__(self, backend_type: str = "local", api_key: str = None)
```

**Parameters:**
- `backend_type` (str): AI backend type - "local" or "cloud"
- `api_key` (str, optional): API key for cloud services

**Attributes:**
- `backend_type` (str): Current backend type
- `current_data` (pd.DataFrame): Currently loaded structured data
- `current_file_info` (dict): Metadata about current file
- `file_processor` (FileProcessor): File processing instance
- `ai_backend` (AIBackend): AI backend instance

#### Methods

##### `process_file(file_path: str) -> Dict[str, Any]`
Process uploaded file and extract data/text.

**Parameters:**
- `file_path` (str): Path to the file to process

**Returns:**
- `Dict[str, Any]`: Processing result with data/text and metadata

**Example:**
```python
agent = DataAnalystAgent()
result = agent.process_file("sales_data.csv")

if 'error' not in result:
    print(f"Loaded {result['info']['rows']} rows")
    print(f"Columns: {list(result['data'].columns)}")
```

##### `get_data_context() -> str`
Generate formatted context string from current data.

**Returns:**
- `str`: Formatted context describing the data

**Example:**
```python
context = agent.get_data_context()
print(context)
# Output: Dataset Overview, Data Types, Statistics, etc.
```

##### `update_backend(backend_type: str, api_key: str = None) -> None`
Switch between AI backends.

**Parameters:**
- `backend_type` (str): New backend type
- `api_key` (str, optional): API key for cloud backend

**Example:**
```python
# Switch to cloud backend
agent.update_backend("cloud", "your_api_key")

# Switch back to local
agent.update_backend("local")
```

### AIBackend

Unified interface for AI services.

```python
class AIBackend:
    def __init__(self, backend_type: str = "local", api_key: str = None)
```

**Attributes:**
- `backend_type` (str): Current backend type
- `conversation_history` (List[Dict]): Chat history
- `client` (Union[LocalLMStudioClient, CloudAIClient]): AI client instance

#### Methods

##### `answer_question(question: str, context: str = "") -> str`
Generate AI response to a question.

**Parameters:**
- `question` (str): User's question
- `context` (str, optional): Data context for better answers

**Returns:**
- `str`: AI-generated response

**Example:**
```python
response = agent.ai_backend.answer_question(
    "What trends do you see in this data?",
    context=agent.get_data_context()
)
print(response)
```

##### `clear_conversation_history() -> None`
Clear the conversation history.

**Example:**
```python
agent.ai_backend.clear_conversation_history()
```

##### `get_conversation_summary() -> str`
Get summary of conversation history.

**Returns:**
- `str`: Formatted conversation summary

## 📄 File Processors

### FileProcessor

Handles processing of various file formats.

```python
class FileProcessor:
    def __init__(self)
```

#### Methods

##### `process_csv(file_path: str) -> Dict[str, Any]`
Process CSV files with automatic encoding detection.

**Parameters:**
- `file_path` (str): Path to CSV file

**Returns:**
- `Dict[str, Any]`: Result with DataFrame and metadata

**Return Structure:**
```python
{
    'data': pd.DataFrame,           # Parsed data
    'info': {
        'rows': int,                # Number of rows
        'columns': int,             # Number of columns
        'memory_usage': int,        # Memory usage in bytes
        'dtypes': dict,             # Column data types
        'missing_values': dict,     # Missing values per column
        'shape': tuple              # (rows, columns)
    },
    'type': 'csv'
}
```

##### `process_excel(file_path: str) -> Dict[str, Any]`
Process Excel files with multi-sheet support.

**Parameters:**
- `file_path` (str): Path to Excel file

**Returns:**
- `Dict[str, Any]`: Result with DataFrame(s) and metadata

**Return Structure:**
```python
{
    'data': pd.DataFrame,           # Data from first/main sheet
    'info': {
        'sheets': List[str],        # Sheet names
        'sheet_details': dict,      # Per-sheet metadata
        # ... other metadata
    },
    'type': 'excel',
    'all_sheets': dict              # All sheets data (if multiple)
}
```

##### `process_pdf(file_path: str) -> Dict[str, Any]`
Extract text and metadata from PDF files.

**Parameters:**
- `file_path` (str): Path to PDF file

**Returns:**
- `Dict[str, Any]`: Result with extracted text and metadata

**Return Structure:**
```python
{
    'text': str,                    # Extracted text content
    'info': {
        'pages': int,               # Number of pages
        'word_count': int,          # Word count
        'character_count': int,     # Character count
        'metadata': dict            # PDF metadata
    },
    'type': 'pdf'
}
```

##### `process_docx(file_path: str) -> Dict[str, Any]`
Extract text and structure from Word documents.

**Parameters:**
- `file_path` (str): Path to DOCX file

**Returns:**
- `Dict[str, Any]`: Result with extracted text and metadata

##### `process_image(file_path: str) -> Dict[str, Any]`
Extract text from images using OCR.

**Parameters:**
- `file_path` (str): Path to image file

**Returns:**
- `Dict[str, Any]`: Result with extracted text and image metadata

**Requirements:**
- Tesseract OCR engine
- pytesseract Python package

## 📊 Visualization Engine

### VisualizationEngine

Creates professional visualizations.

```python
class VisualizationEngine:
    def __init__(self, agent: DataAnalystAgent)
```

**Parameters:**
- `agent` (DataAnalystAgent): Agent instance with loaded data

#### Methods

##### `create_summary_dashboard() -> Optional[plt.Figure]`
Create comprehensive 4-panel data overview.

**Returns:**
- `Optional[plt.Figure]`: Matplotlib figure or None if no data

**Panels:**
1. Data types distribution (pie chart)
2. Missing data pattern (heatmap)
3. Numeric columns distribution (histograms)
4. Dataset information (text summary)

**Example:**
```python
viz = VisualizationEngine(agent)
fig = viz.create_summary_dashboard()
if fig:
    fig.savefig("dashboard.png", dpi=300, bbox_inches='tight')
    plt.show()
```

##### `create_correlation_matrix() -> Optional[plt.Figure]`
Create correlation heatmap for numeric variables.

**Returns:**
- `Optional[plt.Figure]`: Matplotlib figure or None if no numeric data

**Example:**
```python
fig = viz.create_correlation_matrix()
if fig:
    fig.savefig("correlations.png", dpi=300, bbox_inches='tight')
    plt.show()
```

##### `create_distribution_plot(column: str) -> Optional[plt.Figure]`
Create distribution plot for a specific column.

**Parameters:**
- `column` (str): Column name to plot

**Returns:**
- `Optional[plt.Figure]`: Matplotlib figure or None if column not found

##### `create_scatter_plot(x_col: str, y_col: str) -> Optional[plt.Figure]`
Create scatter plot between two numeric columns.

**Parameters:**
- `x_col` (str): X-axis column name
- `y_col` (str): Y-axis column name

**Returns:**
- `Optional[plt.Figure]`: Matplotlib figure or None if columns invalid

##### `create_box_plot(column: str, group_by: str = None) -> Optional[plt.Figure]`
Create box plot for numeric column, optionally grouped.

**Parameters:**
- `column` (str): Numeric column to plot
- `group_by` (str, optional): Column to group by

**Returns:**
- `Optional[plt.Figure]`: Matplotlib figure or None if column invalid

## 🤖 AI Clients

### LocalLMStudioClient

Client for local LM Studio integration.

```python
class LocalLMStudioClient:
    def __init__(self, base_url: str = "http://localhost:1234")
```

**Parameters:**
- `base_url` (str): LM Studio server URL

#### Methods

##### `check_connection() -> bool`
Check if LM Studio server is available.

**Returns:**
- `bool`: True if server accessible

##### `get_models() -> Dict[str, Any]`
Get available models from LM Studio.

**Returns:**
- `Dict[str, Any]`: Model information or error details

##### `answer_question(question: str, context: str = "") -> str`
Generate response using local model.

**Parameters:**
- `question` (str): User's question
- `context` (str, optional): Additional context

**Returns:**
- `str`: AI-generated response

### CloudAIClient

Client for cloud AI services (Together.ai).

```python
class CloudAIClient:
    def __init__(self, api_key: str = None)
```

**Parameters:**
- `api_key` (str, optional): API key (can also use environment variable)

**Raises:**
- `ValueError`: If no API key provided

#### Methods

##### `check_connection() -> bool`
Check if cloud service is available.

**Returns:**
- `bool`: True if service accessible and API key valid

##### `get_models() -> Dict[str, Any]`
Get available models from cloud service.

**Returns:**
- `Dict[str, Any]`: Model information or error details

##### `answer_question(question: str, context: str = "") -> str`
Generate response using cloud model.

**Parameters:**
- `question` (str): User's question
- `context` (str, optional): Additional context

**Returns:**
- `str`: AI-generated response

## ⚠️ Error Handling

### Common Error Patterns

All methods return standardized error information:

```python
{
    'error': str,                   # Error message
    'message': str,                 # Additional help text (optional)
}
```

### Exception Types

#### File Processing Errors
- **FileNotFoundError**: File doesn't exist
- **UnicodeDecodeError**: Encoding issues with text files
- **ImportError**: Missing required libraries
- **PermissionError**: File access denied

#### AI Backend Errors
- **ConnectionError**: Cannot reach AI service
- **TimeoutError**: Request took too long
- **AuthenticationError**: Invalid API key
- **RateLimitError**: API rate limit exceeded

#### Visualization Errors
- **ValueError**: Invalid data for visualization
- **MemoryError**: Dataset too large for visualization
- **ImportError**: Missing visualization libraries

### Error Handling Examples

```python
# File processing with error handling
try:
    result = agent.process_file("data.csv")
    if 'error' in result:
        print(f"Processing failed: {result['error']}")
        if 'message' in result:
            print(f"Help: {result['message']}")
    else:
        print("File processed successfully!")
except Exception as e:
    print(f"Unexpected error: {e}")

# AI response with error handling
try:
    response = agent.ai_backend.answer_question("What insights do you see?")
    if response.startswith("Error:"):
        print(f"AI request failed: {response}")
    else:
        print(f"AI Response: {response}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 📝 Type Definitions

### Common Types

```python
from typing import Dict, List, Any, Optional, Union
import pandas as pd
import matplotlib.pyplot as plt

# File processing result
FileResult = Dict[str, Any]

# Data context
DataContext = str

# AI response
AIResponse = str

# Visualization figure
VisualizationFigure = Optional[plt.Figure]

# Backend types
BackendType = Union["local", "cloud"]

# File types
FileType = Union["csv", "excel", "pdf", "docx", "image", "txt"]
```

### Custom Exceptions

```python
class DataAnalystError(Exception):
    """Base exception for Data Analyst Agent"""
    pass

class FileProcessingError(DataAnalystError):
    """Error in file processing"""
    pass

class AIBackendError(DataAnalystError):
    """Error in AI backend communication"""
    pass

class VisualizationError(DataAnalystError):
    """Error in visualization creation"""
    pass
```

---

**For more examples and advanced usage, check the [examples directory](../examples/) in the repository.**
