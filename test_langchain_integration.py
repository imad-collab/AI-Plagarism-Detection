#!/usr/bin/env python
"""
Test script for LangChain Plagiarism Detection Service
Validates the LangChain integration and all APIs
"""

import requests
import json
import time
from pathlib import Path

BASE_URL = "http://localhost:5001/api"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_health():
    """Test health check endpoint"""
    print_section("Testing Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_upload():
    """Test document upload"""
    print_section("Testing Document Upload")
    
    # Create a test document
    test_content = """
    This is a test document for plagiarism detection.
    It contains several sentences that will be used to test
    the similarity detection algorithms.
    The LangChain integration provides semantic embeddings
    for more accurate plagiarism detection.
    """
    
    # Write to temporary file
    test_file = Path("test_document.txt")
    test_file.write_text(test_content)
    
    # Upload file
    with open(test_file, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/upload", files=files)
    
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    # Clean up
    test_file.unlink()
    
    if response.status_code == 200:
        return result.get('file_id')
    return None

def test_analyze(file_id):
    """Test plagiarism analysis with LangChain"""
    print_section("Testing Plagiarism Analysis (with LangChain)")
    
    payload = {
        "file_id": file_id,
        "comparison_text": """
        This is very similar text for plagiarism detection.
        It contains many sentences that test the
        detection algorithms.
        The LangChain framework provides semantic embeddings
        for accurate detection.
        """,
        "use_langchain": True
    }
    
    response = requests.post(f"{BASE_URL}/analyze", json=payload)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    
    if result.get('success'):
        analysis = result.get('analysis', {})
        print(f"\nAnalysis Results:")
        print(f"  Overall Score: {analysis.get('overall_score', 'N/A'):.2%}")
        print(f"  Confidence: {analysis.get('confidence_score', 'N/A'):.2%}")
        print(f"  Risk Level: {analysis.get('risk_level', 'N/A')}")
        print(f"  Methodology: {analysis.get('methodology', 'N/A')}")
        print(f"  LangChain Enabled: {analysis.get('langchain_enabled', False)}")
        
        print(f"\nSimilarity Breakdown:")
        breakdown = analysis.get('similarity_breakdown', {})
        for algorithm, score in breakdown.items():
            print(f"  {algorithm}: {score:.3f}")
        
        print(f"\nDetailed Response: {json.dumps(result, indent=2)}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    return response.status_code == 200

def test_langchain_direct():
    """Test direct LangChain analysis endpoint"""
    print_section("Testing Direct LangChain Analysis Endpoint")
    
    payload = {
        "document_text": """
        LangChain is a powerful framework for developing applications
        powered by language models. It enables applications that are:
        Data-aware: connect a language model to other sources of data
        Agentic: allow a language model to interact with its environment
        """,
        "comparison_text": """
        LangChain represents a significant framework for building
        applications that leverage language models. The platform allows
        for applications that are contextually aware and can interact
        with various data sources and environments.
        """
    }
    
    response = requests.post(f"{BASE_URL}/langchain-analysis", json=payload)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    
    if result.get('success'):
        print(f"\nLangChain Results:")
        langchain_results = result.get('langchain_results', {})
        print(f"  Overall Score: {langchain_results.get('overall', 'N/A'):.3f}")
        print(f"  Semantic: {langchain_results.get('semantic', 'N/A'):.3f}")
        
        print(f"\nAdvanced ML Results:")
        advanced_results = result.get('advanced_results', {})
        print(f"  Overall Score: {advanced_results.get('overall', 'N/A'):.3f}")
        
        print(f"\nComparison:")
        comparison = result.get('comparison', {})
        print(f"  LangChain Semantic: {comparison.get('langchain_semantic', 'N/A'):.3f}")
        print(f"  Advanced Overall: {comparison.get('advanced_overall', 'N/A'):.3f}")
        print(f"  Difference: {comparison.get('difference', 'N/A'):.3f}")
        
        print(f"\nFull Response: {json.dumps(result, indent=2)}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    return response.status_code == 200

def run_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("  LangChain Plagiarism Detection - Test Suite")
    print("  API Base URL: " + BASE_URL)
    print("="*60)
    
    results = {}
    
    # Test health
    results['health'] = test_health()
    if not results['health']:
        print("❌ Health check failed. API may not be running.")
        return
    
    print("✅ Health check passed")
    
    # Test upload
    print("\nWaiting for embeddings to load...")
    time.sleep(2)
    
    file_id = test_upload()
    results['upload'] = file_id is not None
    if file_id:
        print(f"✅ Upload successful - File ID: {file_id}")
    else:
        print("❌ Upload failed")
        return
    
    # Test analyze
    time.sleep(1)
    results['analyze'] = test_analyze(file_id)
    print("✅ Analysis completed" if results['analyze'] else "❌ Analysis failed")
    
    # Test direct LangChain endpoint
    time.sleep(1)
    results['langchain_direct'] = test_langchain_direct()
    print("✅ Direct LangChain endpoint works" if results['langchain_direct'] else "❌ Direct endpoint failed")
    
    # Summary
    print_section("Test Summary")
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    print(f"Tests Passed: {passed}/{total}")
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} - {test_name}")

if __name__ == "__main__":
    try:
        run_tests()
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to API at " + BASE_URL)
        print("Please make sure the Flask application is running: python app.py")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
