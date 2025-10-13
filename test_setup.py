#!/usr/bin/env python3
"""
Test script for Resume Parser with Ollama integration
Run this to verify your setup is working correctly
"""

import os
import sys
import requests
import json

def test_ollama_connection():
    """Test if Ollama is running and accessible"""
    print("🔍 Testing Ollama connection...")
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"✅ Ollama is running with {len(models)} models")
            
            if models:
                print("📋 Available models:")
                for model in models:
                    print(f"   • {model['name']} ({model.get('size', 'unknown size')})")
                return True, models
            else:
                print("⚠️ Ollama is running but no models are installed")
                return False, []
        else:
            print(f"❌ Ollama returned status code: {response.status_code}")
            return False, []
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama (not running or wrong port)")
        return False, []
    except Exception as e:
        print(f"❌ Error connecting to Ollama: {e}")
        return False, []

def test_model_inference(model_name="llama3.2:3b"):
    """Test model inference with a simple prompt"""
    print(f"\n🧠 Testing model inference with {model_name}...")
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": "Hello, can you respond with just 'AI model working correctly'?",
                "stream": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            output = result.get("response", "").strip()
            print(f"✅ Model response: {output}")
            return True
        else:
            print(f"❌ Model inference failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing model: {e}")
        return False

def test_requirements():
    """Test if required Python packages are installed"""
    print("\n📦 Testing Python requirements...")
    
    required_packages = [
        "streamlit",
        "requests", 
        "PyMuPDF",
        "sentence-transformers",
        "scikit-learn",
        "numpy"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        return False
    
    return True

def test_sample_resume_parsing():
    """Test with a sample resume text"""
    print("\n📄 Testing sample resume parsing...")
    
    sample_text = """
    John Smith
    Senior Software Engineer
    john.smith@email.com | (555) 123-4567
    
    EXPERIENCE
    Senior Python Developer - Tech Corp (2020-2024)
    • Developed scalable web applications using Python and Django
    • Led a team of 5 developers on microservices architecture
    • Implemented CI/CD pipelines with Docker and Kubernetes
    
    EDUCATION
    Master of Computer Science - Stanford University (2018)
    Bachelor of Engineering - MIT (2016)
    
    SKILLS
    Python, JavaScript, React, Docker, Kubernetes, AWS, Machine Learning
    """
    
    try:
        # Test offline parser
        from utils.offline_parser import parse_resume_offline
        offline_result = parse_resume_offline(sample_text)
        print(f"✅ Offline parser: Found {len(offline_result.get('skills', []))} skills")
        
        # Test Ollama parser if available
        ollama_available, models = test_ollama_connection()
        if ollama_available and models:
            from utils.ollama_parser import OllamaParser
            parser = OllamaParser()
            model_name = models[0]['name']
            ollama_result = parser.parse_resume(sample_text, model_name)
            
            if "error" not in ollama_result:
                print(f"✅ Ollama parser: Successfully parsed with {model_name}")
            else:
                print(f"⚠️ Ollama parser error: {ollama_result.get('error', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Resume parsing test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Resume Parser Ollama Test Suite")
    print("=" * 50)
    
    # Test results
    results = {
        "requirements": test_requirements(),
        "ollama_connection": test_ollama_connection()[0],
        "model_inference": False,
        "resume_parsing": False
    }
    
    # Test model inference if Ollama is available
    if results["ollama_connection"]:
        results["model_inference"] = test_model_inference()
    
    # Test resume parsing
    results["resume_parsing"] = test_sample_resume_parsing()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name.replace('_', ' ').title()}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("Run: streamlit run app.py")
    else:
        print("\n⚠️ Some tests failed. Please check the issues above.")
        
        if not results["ollama_connection"]:
            print("\n💡 To install and setup Ollama:")
            print("1. Download from: https://ollama.ai/download")
            print("2. Install a model: ollama pull llama3.2:3b")
            print("3. Start Ollama service")
        
        if not results["requirements"]:
            print("\n💡 Install missing packages:")
            print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()