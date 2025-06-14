#!/usr/bin/env python3
"""
Setup configuration for AI Data Analyst Agent
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
def read_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Version
VERSION = "1.0.0"

setup(
    name="ai-data-analyst-agent",
    version=VERSION,
    author="Your Name",
    author_email="your.email@example.com",
    description="A powerful AI-powered data analysis application with multi-format support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-data-analyst-agent",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/ai-data-analyst-agent/issues",
        "Documentation": "https://github.com/yourusername/ai-data-analyst-agent/wiki",
        "Source Code": "https://github.com/yourusername/ai-data-analyst-agent",    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Data Scientists", 
        "Intended Audience :: Business Analysts",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Office/Business :: Financial :: Spreadsheet",
        "Topic :: Text Processing :: General",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements('requirements.txt'),
    extras_require={
        "dev": read_requirements('requirements-dev.txt'),
        "all": read_requirements('requirements.txt') + read_requirements('requirements-dev.txt'),    },    
    entry_points={
        "console_scripts": [
            "ai-data-analyst=main:main",
        ],
    } if os.path.exists("main.py") else {},
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml", "*.json"],
        "src": ["*.py"],
        "docs": ["*.md"],
        "examples": ["*.py"],
    },
    keywords=[
        "data analysis", "artificial intelligence", "machine learning", 
        "data science", "business intelligence", "csv", "excel", "pdf", 
        "ocr", "streamlit", "gradio", "local ai", "lm studio"
    ],
    zip_safe=False,
)
