#!/usr/bin/env python3
"""
Example: Basic Data Analysis Workflow

This example demonstrates how to use the AI Data Analyst Agent
to perform basic data analysis tasks programmatically.
"""

import sys
import os
import pandas as pd
from pathlib import Path

# Add parent directory to path to import main module
sys.path.append(str(Path(__file__).parent.parent))

from main import DataAnalystAgent, FileProcessor


def main():
    """Demonstrate basic usage of the AI Data Analyst Agent"""
    
    print("🤖 AI Data Analyst Agent - Example Usage\n")
    
    # Initialize the agent
    print("1. Initializing AI Data Analyst Agent...")
    agent = DataAnalystAgent(backend_type="local")
    print("   ✅ Agent initialized with local backend\n")
    
    # Check if sample data exists
    sample_file = Path(__file__).parent.parent / "sample_sales_data.csv"
    
    if not sample_file.exists():
        print("❌ Sample data file not found. Creating one...")
        create_sample_data(sample_file)
        print("   ✅ Sample data created\n")
    
    # Process the file
    print("2. Processing sample data file...")
    result = agent.process_file(str(sample_file))
    
    if 'error' in result:
        print(f"   ❌ Error processing file: {result['error']}")
        return
    
    print("   ✅ File processed successfully!")
    print(f"   📊 Dataset info: {result['info']['rows']} rows, {result['info']['columns']} columns\n")
    
    # Generate data context
    print("3. Generating data context...")
    context = agent.get_data_context()
    print("   ✅ Context generated")
    print(f"   📄 Context preview:\n{context[:500]}...\n")
    
    # Demonstrate conversation features
    print("4. Demonstrating conversation features...")
    
    # Add some mock conversation history
    agent.ai_backend.conversation_history = [
        {
            "role": "user",
            "content": "What is the average sales amount?",
            "timestamp": "2025-06-14T10:00:00"
        },
        {
            "role": "assistant", 
            "content": "Based on the data, the average sales amount is $1,234.56.",
            "timestamp": "2025-06-14T10:00:30"
        }
    ]
    
    # Get conversation summary
    summary = agent.ai_backend.get_conversation_summary()
    print("   ✅ Conversation summary:")
    print(f"   {summary}\n")
    
    # Find similar questions
    similar = agent.ai_backend.get_similar_questions("What's the mean sales value?")
    print("   ✅ Similar questions found:")
    for i, question in enumerate(similar, 1):
        print(f"   {i}. {question}")
    
    print("\n5. File processing capabilities:")
    
    # Demonstrate different file processors
    processors = {
        'CSV': FileProcessor.process_csv,
        'Excel': FileProcessor.process_excel,
        'PDF': FileProcessor.process_pdf,
        'DOCX': FileProcessor.process_docx,
        'Image': FileProcessor.process_image
    }
    
    for name, processor in processors.items():
        print(f"   📁 {name} Processor: Available")
    
    print("\n✅ Example completed successfully!")
    print("\nNext steps:")
    print("- Run 'python main.py' to start the web interface")
    print("- Upload your own data files for analysis")
    print("- Ask questions about your data using natural language")


def create_sample_data(file_path: Path):
    """Create sample sales data for demonstration"""
    
    sample_data = pd.DataFrame({
        'product': ['Widget A', 'Widget B', 'Widget C', 'Gadget X', 'Gadget Y'] * 20,
        'category': ['Widgets', 'Widgets', 'Widgets', 'Gadgets', 'Gadgets'] * 20,
        'price': [10.99, 15.50, 8.75, 25.00, 32.99] * 20,
        'quantity': [1, 2, 3, 1, 2] * 20,
        'sales_date': pd.date_range('2025-01-01', periods=100, freq='D'),
        'region': ['North', 'South', 'East', 'West', 'Central'] * 20,
        'sales_rep': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'] * 20
    })
    
    # Calculate sales amount
    sample_data['sales_amount'] = sample_data['price'] * sample_data['quantity']
    
    # Add some realistic variations
    import numpy as np
    np.random.seed(42)
    sample_data['sales_amount'] *= np.random.uniform(0.8, 1.2, len(sample_data))
    sample_data['sales_amount'] = sample_data['sales_amount'].round(2)
    
    # Save to CSV
    sample_data.to_csv(file_path, index=False)
    print(f"   📄 Created sample data with {len(sample_data)} records")


if __name__ == "__main__":
    main()
