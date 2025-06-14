<<<<<<< HEAD
# 🤖 AI Data Analyst Agent

A powerful AI-powered data analysis application that supports multiple file formats, provides intelligent insights, and offers both local and cloud-based AI integration.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com)

## ✨ Features

- **📊 Multi-format File Support**: CSV, Excel, PDF, DOCX, TXT, Images with OCR
- **🤖 AI-Powered Analysis**: Intelligent insights and recommendations
- **💬 Multi-turn Q&A**: Context-aware conversations about your data
- **📈 Rich Visualizations**: Correlation matrices, summary dashboards, and charts
- **🔄 Dual Backend Support**: Local LM Studio or cloud Together.ai
- **🎨 Dual Interface**: Streamlit web app and Gradio interface
- **🐳 Docker Ready**: Containerized for easy deployment
- **🔒 Privacy First**: Local processing option available

## 🚀 Quick Start

### Option 1: Streamlit Web Interface (Recommended)
```bash
git clone <your-repo-url>
cd ai-data-analyst-agent
pip install -r requirements.txt
python main.py
```

### Option 2: Gradio Interface
```bash
python main.py --interface gradio
```

### Option 3: Docker
```bash
docker build -t ai-data-analyst .
docker run -p 8501:8501 ai-data-analyst
```

## 📋 Requirements

- Python 3.8+
- 4GB+ RAM recommended
- For OCR: Tesseract installation (optional)
- For cloud AI: Together.ai API key

## 🔧 Configuration

### Cloud Backend (Together.ai)
1. Get your API key from [Together.ai](https://api.together.xyz/)
2. Enter it in the web interface or set environment variable:
```bash
export TOGETHER_API_KEY="your_api_key_here"
```

### Local Backend (LM Studio)
1. Install [LM Studio](https://lmstudio.ai/)
2. Download a model (recommended: meta-llama-3.1-8b-instruct)
3. Start the server:
```bash
lms server start
```

## 📊 Supported File Formats

| Format | Features | Example Use Cases |
|--------|----------|-------------------|
| **CSV/Excel** | Full statistical analysis, correlations | Sales data, survey results |
| **PDF** | Text extraction, metadata analysis | Reports, research papers |
| **DOCX** | Document structure analysis | Contracts, proposals |
| **TXT** | Content analysis, word frequency | Logs, transcripts |
| **Images** | OCR text extraction | Scanned documents, screenshots |

## 🎯 Key Capabilities

### 📈 Data Analysis
- Statistical summaries and distributions
- Correlation analysis and pattern detection
- Missing data analysis and recommendations
- Outlier detection and data quality assessment

### 🖼️ Visualizations
- **📊 Summary Dashboard**: 4-panel data overview
- **🔗 Correlation Matrix**: Professional heatmaps
- **📈 Quick Plots**: Automatic scatter plots and histograms
- **📋 Data Quality Reports**: Missing values and type analysis

### 💬 AI Q&A
- Natural language questions about your data
- Multi-turn conversations with context
- Follow-up questions and clarifications
- Business insights and recommendations

## 🛠️ Development

### Setup Development Environment
```bash
make install-dev
pre-commit install
```

### Run Tests
```bash
make test
make test-cov
```

### Code Quality
```bash
make lint
make format
```

## 📁 Project Structure

```
ai-data-analyst-agent/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── .env.example          # Environment variables template
├── examples/             # Usage examples and demos
├── tests/               # Test suite
├── .github/             # GitHub Actions CI/CD
└── docs/                # Documentation
```

## 🔒 Privacy & Security

- **Local Processing**: All data can be processed locally with LM Studio
- **No Data Storage**: Files are processed in memory and deleted
- **Secure API**: Environment variables for API keys
- **Optional OCR**: Image processing is optional and local

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

## 📞 Support

- 📧 [Create an Issue](../../issues)
- 📖 [Documentation](docs/)
- 💬 [Discussions](../../discussions)

## 🎉 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Together.ai](https://together.ai/) for cloud AI services
- [LM Studio](https://lmstudio.ai/) for local AI capabilities
- All the open-source libraries that make this possible

---

<div align="center">
  <strong>⭐ Star this repo if you find it helpful!</strong>
</div>
=======
# 🤖 AI Data Analyst Agent

A powerful AI-powered data analysis application that supports multiple file formats, provides intelligent insights, and offers both local and cloud-based AI integration.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com)

## ✨ Features

- **📊 Multi-format File Support**: CSV, Excel, PDF, DOCX, TXT, Images with OCR
- **🤖 AI-Powered Analysis**: Intelligent insights and recommendations
- **💬 Multi-turn Q&A**: Context-aware conversations about your data
- **📈 Rich Visualizations**: Correlation matrices, summary dashboards, and charts
- **🔄 Dual Backend Support**: Local LM Studio or cloud Together.ai
- **🎨 Dual Interface**: Streamlit web app and Gradio interface
- **🐳 Docker Ready**: Containerized for easy deployment
- **🔒 Privacy First**: Local processing option available

## 🚀 Quick Start

### Option 1: Streamlit Web Interface (Recommended)
```bash
git clone <your-repo-url>
cd ai-data-analyst-agent
pip install -r requirements.txt
python main.py
```

### Option 2: Gradio Interface
```bash
python main.py --interface gradio
```

### Option 3: Docker
```bash
docker build -t ai-data-analyst .
docker run -p 8501:8501 ai-data-analyst
```

## 📋 Requirements

- Python 3.8+
- 4GB+ RAM recommended
- For OCR: Tesseract installation (optional)
- For cloud AI: Together.ai API key

## 🔧 Configuration

### Cloud Backend (Together.ai)
1. Get your API key from [Together.ai](https://api.together.xyz/)
2. Enter it in the web interface or set environment variable:
```bash
export TOGETHER_API_KEY="your_api_key_here"
```

### Local Backend (LM Studio)
1. Install [LM Studio](https://lmstudio.ai/)
2. Download a model (recommended: meta-llama-3.1-8b-instruct)
3. Start the server:
```bash
lms server start
```

## 📊 Supported File Formats

| Format | Features | Example Use Cases |
|--------|----------|-------------------|
| **CSV/Excel** | Full statistical analysis, correlations | Sales data, survey results |
| **PDF** | Text extraction, metadata analysis | Reports, research papers |
| **DOCX** | Document structure analysis | Contracts, proposals |
| **TXT** | Content analysis, word frequency | Logs, transcripts |
| **Images** | OCR text extraction | Scanned documents, screenshots |

## 🎯 Key Capabilities

### 📈 Data Analysis
- Statistical summaries and distributions
- Correlation analysis and pattern detection
- Missing data analysis and recommendations
- Outlier detection and data quality assessment

### 🖼️ Visualizations
- **📊 Summary Dashboard**: 4-panel data overview
- **🔗 Correlation Matrix**: Professional heatmaps
- **📈 Quick Plots**: Automatic scatter plots and histograms
- **📋 Data Quality Reports**: Missing values and type analysis

### 💬 AI Q&A
- Natural language questions about your data
- Multi-turn conversations with context
- Follow-up questions and clarifications
- Business insights and recommendations

## 🛠️ Development

### Setup Development Environment
```bash
make install-dev
pre-commit install
```

### Run Tests
```bash
make test
make test-cov
```

### Code Quality
```bash
make lint
make format
```

## 📁 Project Structure

```
ai-data-analyst-agent/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── .env.example          # Environment variables template
├── examples/             # Usage examples and demos
├── tests/               # Test suite
├── .github/             # GitHub Actions CI/CD
└── docs/                # Documentation
```

## 🔒 Privacy & Security

- **Local Processing**: All data can be processed locally with LM Studio
- **No Data Storage**: Files are processed in memory and deleted
- **Secure API**: Environment variables for API keys
- **Optional OCR**: Image processing is optional and local

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

## 📞 Support

- 📧 [Create an Issue](../../issues)
- 📖 [Documentation](docs/)
- 💬 [Discussions](../../discussions)

## 🎉 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Together.ai](https://together.ai/) for cloud AI services
- [LM Studio](https://lmstudio.ai/) for local AI capabilities
- All the open-source libraries that make this possible

---

<div align="center">
  <strong>⭐ Star this repo if you find it helpful!</strong>
</div>
>>>>>>> 0f3fe5ae72e1e543da9128827c74b2ea0a92d9d6
