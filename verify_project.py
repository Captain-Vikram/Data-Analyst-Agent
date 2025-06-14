#!/usr/bin/env python3
"""
🔍 Project Verification Script

This script verifies that the AI Data Analyst Agent is properly set up
and all components are working correctly with the new modular structure.
"""

import sys
import os
import importlib.util
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and report status."""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} (MISSING)")
        return False

def check_module_import(module_path, module_name):
    """Check if a module can be imported."""
    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print(f"✅ Module import successful: {module_name}")
        return True
    except Exception as e:
        print(f"❌ Module import failed: {module_name} - {str(e)}")
        return False

def main():
    """Run comprehensive project verification."""
    print("🔍 AI Data Analyst Agent - Project Verification")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    success_count = 0
    total_checks = 0
    
    # Check core project files
    core_files = [
        ("main.py", "Main application entry point"),
        ("requirements.txt", "Core dependencies"),
        ("requirements-dev.txt", "Development dependencies"),
        ("setup.py", "Package setup configuration"),
        ("README.md", "Project documentation"),
        ("LICENSE", "Project license"),
        (".gitignore", "Git ignore rules"),
        ("Dockerfile", "Docker configuration"),
        ("docker-compose.yml", "Docker Compose configuration"),
    ]
    
    print("\n📁 Core Project Files:")
    for filename, description in core_files:
        file_path = project_root / filename
        if check_file_exists(file_path, description):
            success_count += 1
        total_checks += 1
    
    # Check source code structure
    src_files = [
        ("src/__init__.py", "Source package initialization"),
        ("src/core.py", "Core business logic"),
        ("src/processors.py", "File processing utilities"),
        ("src/visualization.py", "Visualization engine"),
        ("src/clients.py", "AI client implementations"),
    ]
    
    print("\n🏗️  Source Code Structure:")
    for filename, description in src_files:
        file_path = project_root / filename
        if check_file_exists(file_path, description):
            success_count += 1
        total_checks += 1
    
    # Check documentation
    doc_files = [
        ("docs/README.md", "User guide and API reference"),
        ("docs/DEPLOYMENT.md", "Deployment guide"),
        ("docs/API_REFERENCE.md", "Detailed API documentation"),
        ("docs/PROJECT_OVERVIEW.md", "Project overview"),
    ]
    
    print("\n📚 Documentation:")
    for filename, description in doc_files:
        file_path = project_root / filename
        if check_file_exists(file_path, description):
            success_count += 1
        total_checks += 1
    
    # Check examples and tests
    other_files = [
        ("examples/basic_usage.py", "Basic usage example"),
        ("examples/demo_visualizations.py", "Visualization demos"),
        ("tests/test_main.py", "Main test suite"),
        ("GITHUB_SETUP.md", "GitHub setup guide"),
        ("MANIFEST.in", "Package manifest"),
    ]
    
    print("\n🧪 Examples and Tests:")
    for filename, description in other_files:
        file_path = project_root / filename
        if check_file_exists(file_path, description):
            success_count += 1
        total_checks += 1
    
    # Test module imports
    print("\n🔗 Module Import Testing:")
    src_modules = [
        ("src/core.py", "core"),
        ("src/processors.py", "processors"),
        ("src/visualization.py", "visualization"),
        ("src/clients.py", "clients"),
    ]
    
    # Add src to Python path for imports
    sys.path.insert(0, str(project_root / "src"))
    
    for module_path, module_name in src_modules:
        full_path = project_root / module_path
        if full_path.exists():
            if check_module_import(full_path, module_name):
                success_count += 1
        else:
            print(f"❌ Module file missing: {module_path}")
        total_checks += 1
    
    # Check if main.py can be imported
    print("\n🚀 Main Application Testing:")
    main_path = project_root / "main.py"
    if main_path.exists():
        try:
            # Just check syntax, don't run the app
            with open(main_path, 'r') as f:
                compile(f.read(), main_path, 'exec')
            print("✅ Main application syntax check passed")
            success_count += 1
        except SyntaxError as e:
            print(f"❌ Main application syntax error: {e}")
    else:
        print("❌ Main application file missing")
    total_checks += 1
    
    # Final report
    print("\n" + "=" * 50)
    print(f"📊 Verification Summary:")
    print(f"   ✅ Successful checks: {success_count}")
    print(f"   ❌ Failed checks: {total_checks - success_count}")
    print(f"   📈 Success rate: {(success_count/total_checks)*100:.1f}%")
    
    if success_count == total_checks:
        print("\n🎉 Perfect! Your AI Data Analyst Agent is ready for GitHub!")
        return 0
    elif success_count >= total_checks * 0.9:
        print("\n✨ Great! Minor issues detected, but project is mostly ready.")
        return 0
    else:
        print("\n⚠️  Several issues detected. Please fix them before proceeding.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
