# 📚 AI Data Analyst Agent - Documentation

Welcome to the comprehensive documentation for the AI Data Analyst Agent, a powerful AI-powered data analysis application that supports multiple file formats and provides intelligent insights.

## 📋 Table of Contents

1. [Quick Start](#-quick-start)
2. [Architecture Overview](#-architecture-overview)
3. [API Reference](#-api-reference)
4. [File Format Support](#-file-format-support)
5. [Visualization Features](#-visualization-features)
6. [Configuration Guide](#-configuration-guide)
7. [Development Guide](#-development-guide)
8. [Troubleshooting](#-troubleshooting)

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-data-analyst-agent.git
cd ai-data-analyst-agent

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Basic Usage

```python
from src import DataAnalystAgent

# Initialize the agent
agent = DataAnalystAgent(backend_type="local")

# Process a file
result = agent.process_file("data.csv")

# Ask questions about your data
context = agent.get_data_context()
response = agent.ai_backend.answer_question("What are the main trends?", context)
print(response)
```

## 🏗️ Architecture Overview

The AI Data Analyst Agent follows a modular architecture:

```
ai-data-analyst-agent/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── core.py              # Main classes (DataAnalystAgent, AIBackend)
│   ├── processors.py        # File processing utilities
│   ├── visualization.py     # Visualization engine
│   └── clients.py           # AI client implementations
├── main.py                  # Application entry point
├── tests/                   # Test suite
└── examples/                # Usage examples
```

### Core Components

#### DataAnalystAgent
The main orchestrator class that coordinates all operations.

#### AIBackend
Unified interface for both local and cloud AI services.

#### FileProcessor
Handles reading and processing various file formats.

#### VisualizationEngine
Creates professional-quality visualizations and charts.

## 📖 API Reference

### DataAnalystAgent Class

```python
class DataAnalystAgent:
    def __init__(self, backend_type: str = "local", api_key: str = None)
    def process_file(self, file_path: str) -> Dict[str, Any]
    def get_data_context(self) -> str
    def update_backend(self, backend_type: str, api_key: str = None)
```

**Methods:**

- `process_file(file_path)`: Process uploaded file and extract data
- `get_data_context()`: Generate context string from current data
- `update_backend(backend_type, api_key)`: Switch between AI backends

### VisualizationEngine Class

```python
class VisualizationEngine:
    def __init__(self, agent: DataAnalystAgent)
    def create_summary_dashboard(self) -> Optional[plt.Figure]
    def create_correlation_matrix(self) -> Optional[plt.Figure]
    def create_distribution_plot(self, column: str) -> Optional[plt.Figure]
    def create_scatter_plot(self, x_col: str, y_col: str) -> Optional[plt.Figure]
```

**Methods:**

- `create_summary_dashboard()`: 4-panel data overview
- `create_correlation_matrix()`: Correlation heatmap for numeric variables
- `create_distribution_plot(column)`: Distribution plot for specific column
- `create_scatter_plot(x_col, y_col)`: Scatter plot between two variables

### FileProcessor Class

```python
class FileProcessor:
    def process_csv(self, file_path: str) -> Dict[str, Any]
    def process_excel(self, file_path: str) -> Dict[str, Any]
    def process_pdf(self, file_path: str) -> Dict[str, Any]
    def process_docx(self, file_path: str) -> Dict[str, Any]
    def process_image(self, file_path: str) -> Dict[str, Any]
```

## 📄 File Format Support

| Format | Extension | Features | Requirements |
|--------|-----------|----------|--------------|
| **CSV** | `.csv` | Full data analysis, statistics, visualizations | pandas |
| **Excel** | `.xlsx`, `.xls` | Multi-sheet support, metadata extraction | pandas, openpyxl |
| **PDF** | `.pdf` | Text extraction, metadata parsing | PyPDF2 |
| **Word** | `.docx` | Document structure analysis, table extraction | python-docx |
| **Images** | `.png`, `.jpg`, `.jpeg` | OCR text extraction | Pillow, pytesseract |
| **Text** | `.txt` | Content analysis, word frequency | Built-in |

### Processing Results

Each file processor returns a standardized dictionary:

```python
{
    'data': DataFrame,      # For structured data (CSV, Excel)
    'text': str,           # For unstructured data (PDF, DOCX, Images)
    'info': dict,          # Metadata and statistics
    'type': str,           # File type identifier
    'error': str           # Error message if processing failed
}
```

## 📊 Visualization Features

### Summary Dashboard
A comprehensive 4-panel overview including:
- **Data Types Distribution**: Pie chart of column types
- **Missing Data Pattern**: Heatmap of missing values
- **Numeric Distributions**: Histograms of numeric columns
- **Dataset Information**: Key statistics and metadata

### Correlation Matrix
Professional correlation heatmap showing:
- Pearson correlation coefficients between numeric variables
- Color-coded visualization (-1 to +1 scale)
- Annotated values for precise analysis

### Interactive Charts
- **Scatter Plots**: Relationship analysis between variables
- **Distribution Plots**: Histogram and density plots
- **Box Plots**: Statistical distribution analysis

### Usage Example

```python
from src import DataAnalystAgent, VisualizationEngine

# Initialize
agent = DataAnalystAgent()
agent.process_file("sales_data.csv")

# Create visualizations
viz = VisualizationEngine(agent)

# Generate dashboard
fig1 = viz.create_summary_dashboard()
fig1.savefig("dashboard.png", dpi=300, bbox_inches='tight')

# Generate correlation matrix
fig2 = viz.create_correlation_matrix()
fig2.savefig("correlations.png", dpi=300, bbox_inches='tight')
```

## ⚙️ Configuration Guide

### Environment Variables

```bash
# For cloud AI backend
export TOGETHER_API_KEY="your_api_key_here"

# For local LM Studio (optional)
export LM_STUDIO_URL="http://localhost:1234"
```

### LM Studio Setup

1. **Download and Install**: [LM Studio](https://lmstudio.ai/)
2. **Download a Model**: Recommended models:
   - `meta-llama/Llama-2-7b-chat-hf`
   - `meta-llama/Llama-2-13b-chat-hf`
   - `mistralai/Mistral-7B-Instruct-v0.1`
3. **Start Server**: Use the LM Studio interface or CLI
4. **Verify Connection**: The app will auto-detect the running server

### Cloud AI Setup (Together.ai)

1. **Get API Key**: Visit [Together.ai](https://api.together.xyz/)
2. **Set Environment Variable** or enter in the web interface
3. **Verify Connection**: The app will validate the key automatically

## 🛠️ Development Guide

### Project Structure

```
src/
├── __init__.py          # Package exports
├── core.py              # Main application logic
├── processors.py        # File processing utilities
├── visualization.py     # Visualization engine
└── clients.py           # AI client implementations
```

### Adding New File Processors

```python
class FileProcessor:
    def process_new_format(self, file_path: str) -> Dict[str, Any]:
        try:
            # Your processing logic here
            data = process_file(file_path)
            
            return {
                'data': data,           # or 'text' for unstructured
                'info': metadata,       # File metadata
                'type': 'new_format'    # Format identifier
            }
        except Exception as e:
            return {'error': f'Processing failed: {str(e)}'}
```

### Adding New Visualizations

```python
class VisualizationEngine:
    def create_custom_plot(self, **kwargs) -> Optional[plt.Figure]:
        if self.agent.current_data is None:
            return None
        
        df = self.agent.current_data
        
        # Create your visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        # ... plotting code ...
        
        plt.tight_layout()
        return fig
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_processors.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

## 🔧 Troubleshooting

### Common Issues

#### 1. LM Studio Connection Failed
**Problem**: Cannot connect to LM Studio server
**Solutions**:
- Ensure LM Studio is running
- Check server URL (default: http://localhost:1234)
- Verify model is loaded in LM Studio
- Check firewall settings

#### 2. Cloud AI Authentication Error
**Problem**: Invalid API key for Together.ai
**Solutions**:
- Verify API key is correct
- Check internet connection
- Ensure API key has proper permissions
- Try regenerating the API key

#### 3. File Processing Errors
**Problem**: Cannot process uploaded files
**Solutions**:
- Check file format is supported
- Verify file is not corrupted
- Ensure required libraries are installed
- Check file permissions

#### 4. Visualization Not Showing
**Problem**: Plots not displaying in interface
**Solutions**:
- Ensure matplotlib backend is configured
- Check if data contains numeric columns (for correlations)
- Verify data is loaded successfully
- Try clearing browser cache (for web interface)

#### 5. OCR/Image Processing Fails
**Problem**: Cannot extract text from images
**Solutions**:
- Install Tesseract OCR engine
- Verify pytesseract is installed
- Check image quality and resolution
- Try different image formats

### Performance Tips

1. **Large Files**: For files >100MB, consider sampling data first
2. **Memory Usage**: Monitor RAM usage with large datasets
3. **Processing Speed**: CSV files process faster than Excel
4. **Visualization**: Limit correlation matrix to <50 variables for performance

### Getting Help

1. **Check Documentation**: Review this guide and inline docstrings
2. **Search Issues**: Look for similar problems in GitHub Issues
3. **Create Issue**: Report bugs with detailed reproduction steps
4. **Community Discussion**: Use GitHub Discussions for questions

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)
- [LM Studio Documentation](https://lmstudio.ai/docs)
- [Together.ai API Documentation](https://docs.together.ai/)

---

**Need more help?** Check our [GitHub repository](https://github.com/yourusername/ai-data-analyst-agent) or open an issue!
