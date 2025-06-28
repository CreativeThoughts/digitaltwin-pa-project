#!/usr/bin/env python3
"""
Setup script for the Agentic AI Solution.
This script installs dependencies and prepares the environment.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command: str, description: str):
    """Run a command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(f"  Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("✗ Python 3.8 or higher is required")
        print(f"  Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("\nInstalling dependencies...")
    
    # Upgrade pip
    if not run_command("pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        return False
    
    return True

def create_directories():
    """Create necessary directories."""
    print("\nCreating directories...")
    
    directories = [
        "logs",
        "output",
        "tests"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    return True

def create_env_file():
    """Create .env file if it doesn't exist."""
    env_file = Path(".env")
    if env_file.exists():
        print("✓ .env file already exists")
        return True
    
    print("\nCreating .env file...")
    
    env_content = """# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Logging
LOG_LEVEL=INFO

# Output Configuration
OUTPUT_FILE_PATH=./output/responses.json

# Agent Configuration
MAX_CONVERSATION_TURNS=10
TIMEOUT=60

# AutoGen Configuration (optional - for production use)
# AUTOGEN_CONFIG_LIST=[{"model": "gpt-4", "api_key": "your-api-key"}]
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print("✓ Created .env file")
    return True

def test_imports():
    """Test if all modules can be imported."""
    print("\nTesting imports...")
    
    try:
        import fastapi
        import uvicorn
        import pydantic
        import autogen
        import loguru
        print("✓ All required packages imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def main():
    """Main setup function."""
    print("=" * 60)
    print("AGENTIC AI SOLUTION - SETUP")
    print("=" * 60)
    print()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n✗ Setup failed during dependency installation")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("\n✗ Setup failed during directory creation")
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        print("\n✗ Setup failed during .env file creation")
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        print("\n✗ Setup failed during import testing")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✓ SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Review and customize the .env file if needed")
    print("2. Start the API server: python main.py")
    print("3. Test the API: python test_api.py")
    print("4. Access the API documentation: http://localhost:8000/docs")
    print()
    print("For production use:")
    print("- Configure AutoGen with your API keys in .env")
    print("- Set appropriate log levels and timeouts")
    print("- Consider using a production WSGI server")

if __name__ == "__main__":
    main() 