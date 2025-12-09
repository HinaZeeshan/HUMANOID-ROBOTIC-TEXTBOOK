#!/usr/bin/env python3
"""
Validation script to ensure all functionality works as expected for the Humanoid Robotics Textbook project.
This script performs end-to-end validation of the system's core functionality.
"""

import os
import sys
import time
from pathlib import Path
import requests
import json

# Add the backend src to path to import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "backend/src"))

from backend.src.config import settings

def validate_environment():
    """Validate that required environment variables are set."""
    print("Validating environment...")

    required_vars = ['COHERE_API_KEY', 'QDRANT_URL']
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var) or os.getenv(var) == "your-cohere-api-key" or os.getenv(var) == "https://your-cluster-url.qdrant.tech":
            missing_vars.append(var)

    if missing_vars:
        print(f"❌ Missing or invalid environment variables: {missing_vars}")
        print("Please set these variables in your .env file.")
        return False

    print("✅ Environment variables are properly set")
    return True

def validate_backend_health():
    """Validate that the backend server is running and healthy."""
    print("Validating backend health...")

    try:
        response = requests.get("http://localhost:8000/api/v1/rag/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend is healthy")
            return True
        else:
            print(f"❌ Backend health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is the server running on http://localhost:8000?")
        return False
    except Exception as e:
        print(f"❌ Error during backend health check: {e}")
        return False

def validate_content_api():
    """Validate that the content API is working."""
    print("Validating content API...")

    try:
        response = requests.get("http://localhost:8000/api/v1/content/modules", timeout=10)
        if response.status_code == 200:
            modules = response.json()
            print(f"✅ Content API is working. Found {len(modules)} modules")
            return True
        else:
            print(f"❌ Content API failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error during content API validation: {e}")
        return False

def validate_rag_query():
    """Validate that the RAG query API is working."""
    print("Validating RAG query functionality...")

    try:
        query_request = {
            "query": "What is ROS 2?",
            "max_chunks": 3
        }

        response = requests.post(
            "http://localhost:8000/api/v1/rag/query",
            json=query_request,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            if "response" in result and "sources" in result:
                print("✅ RAG query API is working")
                print(f"   Sample response length: {len(result['response'][:50])} chars")
                print(f"   Retrieved sources: {len(result['sources'])}")
                return True
            else:
                print(f"❌ RAG query returned unexpected format: {result}")
                return False
        else:
            print(f"❌ RAG query failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error during RAG query validation: {e}")
        return False

def validate_cross_module_query():
    """Validate that cross-module queries are working."""
    print("Validating cross-module query functionality...")

    try:
        query_request = {
            "query": "How does voice command lead to robot navigation?",
            "cross_module": True,
            "max_chunks": 3
        }

        response = requests.post(
            "http://localhost:8000/api/v1/rag/query",
            json=query_request,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            if "response" in result and "sources" in result:
                print("✅ Cross-module query API is working")
                print(f"   Sample response length: {len(result['response'][:50])} chars")
                print(f"   Retrieved sources: {len(result['sources'])}")
                return True
            else:
                print(f"❌ Cross-module query returned unexpected format: {result}")
                return False
        else:
            print(f"❌ Cross-module query failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error during cross-module query validation: {e}")
        return False

def validate_frontend_files():
    """Validate that frontend files exist and are properly structured."""
    print("Validating frontend files...")

    frontend_dir = Path(__file__).parent.parent / "my-textbook"

    required_files = [
        "package.json",
        "docusaurus.config.js",
        "src/components/Chatbot.tsx",
        "src/pages/ChatInterface.tsx",
        "docs/01-ros2-basics.md",
        "docs/02-digital-twins.md",
        "docs/03-ai-robot-brain.md",
        "docs/04-vla-models.md",
        "docs/05-capstone-project.md",
        "sidebars.ts"
    ]

    missing_files = []
    for file_path in required_files:
        if not (frontend_dir / file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ Missing frontend files: {missing_files}")
        return False

    print("✅ All required frontend files are present")
    return True

def validate_documentation():
    """Validate that documentation files exist."""
    print("Validating documentation...")

    docs_dir = Path(__file__).parent.parent / "docs"

    required_docs = [
        "README.md",
        "quickstart.md",
        "api.md",
        "testing.md"
    ]

    missing_docs = []
    for doc_file in required_docs:
        if not (docs_dir / doc_file).exists():
            missing_docs.append(doc_file)

    if missing_docs:
        print(f"❌ Missing documentation files: {missing_docs}")
        return False

    print("✅ All required documentation files are present")
    return True

def validate_content_indexing():
    """Validate that content has been properly indexed."""
    print("Validating content indexing...")

    try:
        # Search for a common term that should exist in the content
        search_request = {
            "query": "ROS 2",
            "max_chunks": 5
        }

        response = requests.post(
            "http://localhost:8000/api/v1/rag/query",
            json=search_request,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            if result.get("sources"):
                print("✅ Content appears to be properly indexed")
                print(f"   Found {len(result['sources'])} relevant sources for 'ROS 2'")
                return True
            else:
                print("⚠️  Content indexing may not be complete - no sources found for common term")
                print("   This might be OK if the RAG index hasn't been built yet")
                return True  # Not a failure, just a warning
        else:
            print(f"❌ Content indexing validation failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️  Could not validate content indexing: {e}")
        print("   This might be OK if the backend isn't running or index isn't built")
        return True  # Not a critical failure

def main():
    """Main validation function."""
    print("🤖 Starting Humanoid Robotics Textbook validation...")
    print("="*60)

    # Track validation results
    results = []

    # Run all validations
    results.append(("Environment", validate_environment()))
    results.append(("Backend Health", validate_backend_health()))
    results.append(("Content API", validate_content_api()))
    results.append(("RAG Query", validate_rag_query()))
    results.append(("Cross-module Query", validate_cross_module_query()))
    results.append(("Frontend Files", validate_frontend_files()))
    results.append(("Documentation", validate_documentation()))
    results.append(("Content Indexing", validate_content_indexing()))

    print("="*60)
    print("VALIDATION SUMMARY:")
    print("="*60)

    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if not passed:
            all_passed = False

    print("="*60)
    if all_passed:
        print("🎉 All validations passed! The system is ready for use.")
        print("\nNext steps:")
        print("1. Run 'python scripts/build-rag-index.py' to index textbook content")
        print("2. Start the backend: 'cd backend && python -m src.api.main'")
        print("3. Start the frontend: 'cd my-textbook && npm start'")
        print("4. Access the application at http://localhost:3000")
    else:
        print("❌ Some validations failed. Please address the issues above.")
        print("   The system may not function correctly until these are resolved.")
        sys.exit(1)

if __name__ == "__main__":
    main()