#!/usr/bin/env python3
"""
Simple GPT-5 API Test

This script tests basic GPT-5 API connectivity to ensure
the API key and model access are working before running
the full GPT5 Evaluator Agent.

Author: Carlos Lozano
Date: August 11, 2025
Phase: 6 - Evaluation Phase
"""

import os
import openai
from openai import OpenAI


def test_gpt5_api():
    """Test basic GPT-5 API connectivity."""
    
    print("🧪 Testing GPT-5 API Connectivity")
    print("=" * 50)
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your_gpt5_api_key_here'")
        return False
    
    print(f"✅ API Key found: {api_key[:8]}...{api_key[-4:]}")
    
    try:
        # Initialize client
        client = OpenAI(api_key=api_key)
        print("✅ OpenAI client initialized successfully")
        
        # Test with GPT-5
        print("\n🚀 Testing GPT-5 model access...")
        
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Please respond with 'GPT-5 API test successful' and nothing else."}
            ],
            temperature=0.1,
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"✅ GPT-5 API test successful!")
        print(f"Response: {result}")
        
        # Test model variants
        print("\n🔍 Testing GPT-5 model variants...")
        
        models_to_test = ["gpt-5", "gpt-5-mini", "gpt-5-nano"]
        
        for model in models_to_test:
            try:
                print(f"Testing {model}...")
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "user", "content": "Hello"}
                    ],
                    max_tokens=10
                )
                print(f"✅ {model} - Access confirmed")
            except Exception as e:
                print(f"❌ {model} - Access failed: {str(e)}")
        
        print("\n🎉 GPT-5 API integration test completed successfully!")
        return True
        
    except openai.AuthenticationError:
        print("❌ Authentication failed - check your API key")
        return False
    except openai.RateLimitError:
        print("❌ Rate limit exceeded - try again later")
        return False
    except openai.APIError as e:
        print(f"❌ OpenAI API error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False


def test_evaluator_initialization():
    """Test GPT5 Evaluator Agent initialization."""
    
    print("\n🔧 Testing GPT5 Evaluator Agent Initialization")
    print("=" * 50)
    
    try:
        from gpt5_evaluator_agent import GPT5EvaluatorAgent
        
        # Test initialization
        evaluator = GPT5EvaluatorAgent("test_key")
        print("✅ GPT5 Evaluator Agent initialized successfully")
        
        # Test model validation
        try:
            invalid_evaluator = GPT5EvaluatorAgent("test_key", "gpt-4")
            print("❌ Should have rejected invalid model")
        except ValueError as e:
            print(f"✅ Correctly rejected invalid model: {str(e)}")
        
        # Test system prompt loading
        prompt = evaluator.load_system_prompt()
        if prompt and len(prompt) > 100:
            print("✅ System prompt loaded successfully")
        else:
            print("❌ System prompt loading failed")
        
        print("🎉 Evaluator initialization test completed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Initialization error: {str(e)}")
        return False


def main():
    """Main test function."""
    
    print("🚀 GPT-5 API Integration Test Suite")
    print("=" * 60)
    
    # Test 1: Basic API connectivity
    api_test_success = test_gpt5_api()
    
    # Test 2: Evaluator initialization
    evaluator_test_success = test_evaluator_initialization()
    
    # Summary
    print(f"\n📋 Test Summary")
    print("=" * 30)
    print(f"GPT-5 API Test: {'✅ PASSED' if api_test_success else '❌ FAILED'}")
    print(f"Evaluator Init: {'✅ PASSED' if evaluator_test_success else '❌ FAILED'}")
    
    if api_test_success and evaluator_test_success:
        print(f"\n🎉 All tests passed! Ready to proceed with GPT5 Evaluator Agent.")
        print(f"Next step: Run the full evaluation test suite")
    else:
        print(f"\n⚠️  Some tests failed. Please resolve issues before proceeding.")
    
    return api_test_success and evaluator_test_success


if __name__ == "__main__":
    main()
