# Contributing to AI Data Analyst Agent

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [Issues](https://github.com/yourusername/ai-data-analyst-agent/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/yourusername/ai-data-analyst-agent/issues/new); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

People *love* thorough bug reports. I'm not even kidding.

## Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ai-data-analyst-agent.git
   cd ai-data-analyst-agent
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up LM Studio:**
   - Download and install LM Studio
   - Download a compatible model (e.g., meta-llama-3.1-8b-instruct)
   - Start the server: `lms server start`

5. **Run tests:**
   ```bash
   pytest
   ```

## Code Style

We use several tools to maintain code quality:

- **Black** for code formatting
- **Flake8** for linting
- **Type hints** where appropriate

Run these before submitting:
```bash
black .
flake8 .
```

## Project Structure

```
ai-data-analyst-agent/
├── main_local.py           # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── LICENSE                # MIT License
├── .gitignore            # Git ignore rules
├── sample_sales_data.csv  # Sample data for testing
└── tests/                # Test files (if any)
```

## Adding New Features

When adding new features:

1. **File Processors**: Add new file type support in the `FileProcessor` class
2. **Analysis Methods**: Extend the `DataAnalystAgent` class
3. **Visualizations**: Add new charts to the `VisualizationEngine` class
4. **UI Components**: Update both Streamlit and Gradio interfaces

## Testing

- Test with different file formats
- Test with various LM Studio models
- Test error handling scenarios
- Test both interfaces (Streamlit and Gradio)

## Documentation

- Update README.md for new features
- Add docstrings to new functions/classes
- Update requirements.txt if adding dependencies
- Add usage examples for new features

## Commit Messages

Use clear and meaningful commit messages:

- `feat: add support for JSON files`
- `fix: handle empty CSV files gracefully`
- `docs: update installation instructions`
- `refactor: improve error handling`

## Questions?

Don't hesitate to ask questions by opening an issue or starting a discussion. We're here to help!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
