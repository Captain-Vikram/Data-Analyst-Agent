#!/usr/bin/env python3
"""
Simple test script to verify the modular structure works correctly.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported successfully."""
    print("🧪 Testing module imports...")
    
    try:
        from core import DataAnalystAgent, AIBackend
        print("✅ Core module imported successfully")
    except Exception as e:
        print(f"❌ Core module import failed: {e}")
        return False
    
    try:
        from processors import FileProcessor
        print("✅ Processors module imported successfully")
    except Exception as e:
        print(f"❌ Processors module import failed: {e}")
        return False
    
    try:
        from visualization import VisualizationEngine
        print("✅ Visualization module imported successfully")
    except Exception as e:
        print(f"❌ Visualization module import failed: {e}")
        return False
    
    try:
        from clients import LocalLMStudioClient, CloudAIClient
        print("✅ Clients module imported successfully")
    except Exception as e:
        print(f"❌ Clients module import failed: {e}")
        return False
    
    return True

def test_classes():
    """Test that classes can be instantiated."""
    print("\n🏗️  Testing class instantiation...")
    
    try:
        from core import DataAnalystAgent, AIBackend
        from processors import FileProcessor
        from visualization import VisualizationEngine
        from clients import LocalLMStudioClient
        
        # Test AIBackend
        backend = AIBackend(backend_type="local")
        print("✅ AIBackend instantiated successfully")
        
        # Test FileProcessor
        processor = FileProcessor()
        print("✅ FileProcessor instantiated successfully")
        
        # Test DataAnalystAgent (needed for VisualizationEngine)
        agent = DataAnalystAgent(backend_type="local")
        print("✅ DataAnalystAgent instantiated successfully")
        
        # Test VisualizationEngine with agent
        viz_engine = VisualizationEngine(agent)
        print("✅ VisualizationEngine instantiated successfully")
        
        # Test LocalLMStudioClient
        client = LocalLMStudioClient()
        print("✅ LocalLMStudioClient instantiated successfully")
        
        return True
    except Exception as e:
        print(f"❌ Class instantiation failed: {e}")
        return False

def main():
    print("🔍 AI Data Analyst Agent - Module Testing")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed!")
        return 1
    
    # Test class instantiation
    if not test_classes():
        print("\n❌ Class instantiation tests failed!")
        return 1
    
    print("\n🎉 All tests passed! Modular structure is working correctly.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
