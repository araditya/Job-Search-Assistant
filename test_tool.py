#!/usr/bin/env python3
"""
Simple test script to verify Job Search Assistant is working correctly.
This script tests the core functionality without requiring a full setup.
"""

import sys
import os
import json
import time
import subprocess
import requests
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_section(text):
    """Print a section header"""
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}")

def print_success(text):
    """Print success message"""
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    """Print error message"""
    print(f"{RED}✗ {text}{RESET}")

def print_info(text):
    """Print info message"""
    print(f"{YELLOW}ℹ {text}{RESET}")

def check_dependencies():
    """Check if required dependencies are installed"""
    print_section("Checking Dependencies")
    
    required_packages = [
        ('flask', 'flask'),
        ('flask-cors', 'flask_cors'),
        ('requests', 'requests'),
        ('python-dotenv', 'dotenv'),
        ('flask-sqlalchemy', 'flask_sqlalchemy'),
        ('flask-jwt-extended', 'flask_jwt_extended')
    ]
    missing = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print_success(f"{package_name} is installed")
        except ImportError:
            missing.append(package_name)
            print_error(f"{package_name} is NOT installed")
    
    if missing:
        print_error(f"\nMissing packages: {', '.join(missing)}")
        print_info("Install with: pip install -r requirements.txt")
        return False
    return True

def check_env_file():
    """Check if .env file exists and has required keys"""
    print_section("Checking Environment Configuration")
    
    env_path = Path(__file__).parent / '.env'
    
    if not env_path.exists():
        print_error(".env file not found")
        print_info("Copy .env.example to .env and add your RAPIDAPI_KEY")
        return False
    
    print_success(".env file exists")
    
    # Check for RAPIDAPI_KEY
    with open(env_path) as f:
        env_content = f.read()
        if 'RAPIDAPI_KEY=' in env_content:
            # Check if it's not the example value
            if 'your_rapidapi_key_here' not in env_content:
                print_success("RAPIDAPI_KEY is configured")
                return True
            else:
                print_error("RAPIDAPI_KEY is set to example value")
                print_info("Please add your actual RapidAPI key to .env file")
                return False
        else:
            print_error("RAPIDAPI_KEY not found in .env")
            return False

def test_import():
    """Test if the app can be imported"""
    print_section("Testing Module Import")
    
    try:
        import app
        print_success("app.py can be imported successfully")
        return True
    except Exception as e:
        print_error(f"Failed to import app.py: {e}")
        return False

def test_server():
    """Test if the Flask server can start and respond"""
    print_section("Testing Flask Server")
    
    # Start the server in the background
    print_info("Starting Flask server...")
    
    process = subprocess.Popen(
        [sys.executable, 'app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=Path(__file__).parent
    )
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        # Test health endpoint
        print_info("Testing /health endpoint...")
        response = requests.get('http://127.0.0.1:5000/health', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'ok':
                print_success("Health check passed")
            else:
                print_error(f"Unexpected health response: {data}")
                return False
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
        
        # Test search endpoint with a simple query
        print_info("Testing /search_jobs endpoint...")
        response = requests.post(
            'http://127.0.0.1:5000/search_jobs',
            json={'query': 'python developer', 'page': 1, 'num_pages': 1},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'jobs' in data:
                print_success(f"Search endpoint working - found {len(data['jobs'])} jobs")
                
                # Display first job if available
                if data['jobs']:
                    job = data['jobs'][0]
                    print_info(f"\nSample job result:")
                    print(f"  Title: {job.get('Job Name', 'N/A')}")
                    print(f"  Company: {job.get('Company', 'N/A')}")
                    print(f"  Location: {job.get('Location', 'N/A')}")
            else:
                print_error(f"Unexpected response format: {data}")
                return False
        else:
            print_error(f"Search endpoint failed with status {response.status_code}")
            try:
                print_info(f"Response: {response.text}")
            except:
                pass
            return False
        
        print_success("All server tests passed!")
        return True
        
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to server - it may not have started")
        return False
    except requests.exceptions.Timeout:
        print_error("Request timed out - server may be slow or unresponsive")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False
    finally:
        # Clean up: kill the server process
        print_info("Stopping Flask server...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

def main():
    """Run all tests"""
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}Job Search Assistant - Test Tool{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}")
    
    results = []
    
    # Run tests
    results.append(("Dependencies", check_dependencies()))
    results.append(("Environment", check_env_file()))
    results.append(("Module Import", test_import()))
    results.append(("Server Functionality", test_server()))
    
    # Print summary
    print_section("Test Summary")
    
    all_passed = True
    for test_name, passed in results:
        if passed:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
            all_passed = False
    
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    if all_passed:
        print_success("All tests passed! ✨")
        print_info("\nThe Job Search Assistant is ready to use!")
        print_info("You can start the server with: python app.py")
        print_info("Then visit: http://localhost:5000/health")
        return 0
    else:
        print_error("Some tests failed. Please fix the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
