#!/usr/bin/env python3
"""
Advanced GPT-5 Debug

Systematic troubleshooting of GPT-5 API issues.
"""

import os
import json
from openai import OpenAI


def debug_gpt5_systematically():
    """Systematically debug GPT-5 API issues."""
    
    print("🔍 Advanced GPT-5 Debug - Systematic Troubleshooting")
    print("=" * 60)
    
    # Load environment
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"API Key: {'✅ Found' if api_key else '❌ Missing'}")
    
    if not api_key:
        return
    
    client = OpenAI(api_key=api_key)
    
    # Test 1: Basic GPT-5 with minimal parameters
    print("\n🧪 Test 1: Basic GPT-5 (minimal parameters)")
    print("-" * 40)
    try:
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "user", "content": "Hello"}
            ]
        )
        result = response.choices[0].message.content
        print(f"✅ Basic GPT-5: '{result}'")
        print(f"   Usage: {response.usage}")
    except Exception as e:
        print(f"❌ Basic GPT-5: {str(e)}")
    
    # Test 2: GPT-5 with different message format
    print("\n🧪 Test 2: GPT-5 with system message")
    print("-" * 40)
    try:
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello World'"}
            ]
        )
        result = response.choices[0].message.content
        print(f"✅ GPT-5 with system: '{result}'")
        print(f"   Usage: {response.usage}")
    except Exception as e:
        print(f"❌ GPT-5 with system: {str(e)}")
    
    # Test 3: Check if it's a parameter issue
    print("\n🧪 Test 3: GPT-5 with max_completion_tokens")
    print("-" * 40)
    try:
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "user", "content": "Hello"}
            ],
            max_completion_tokens=50
        )
        result = response.choices[0].message.content
        print(f"✅ GPT-5 with max_completion_tokens: '{result}'")
        print(f"   Usage: {response.usage}")
    except Exception as e:
        print(f"❌ GPT-5 with max_completion_tokens: {str(e)}")
    
    # Test 4: Check if it's a model access issue
    print("\n🧪 Test 4: List available models")
    print("-" * 40)
    try:
        models = client.models.list()
        gpt5_models = [model.id for model in models.data if 'gpt-5' in model.id]
        print(f"✅ Available GPT-5 models: {gpt5_models}")
        
        # Check specific model details
        for model_id in gpt5_models:
            try:
                model_info = client.models.retrieve(model_id)
                print(f"   {model_id}: {model_info.object} - {getattr(model_info, 'status', 'N/A')}")
            except Exception as e:
                print(f"   {model_id}: Error retrieving info - {str(e)}")
                
    except Exception as e:
        print(f"❌ Error listing models: {str(e)}")
    
    # Test 5: Try different GPT-5 variants
    print("\n🧪 Test 5: Different GPT-5 variants")
    print("-" * 40)
    variants = ["gpt-5", "gpt-5-mini", "gpt-5-nano"]
    
    for variant in variants:
        try:
            response = client.chat.completions.create(
                model=variant,
                messages=[
                    {"role": "user", "content": "Hello"}
                ]
            )
            result = response.choices[0].message.content
            print(f"✅ {variant}: '{result}'")
        except Exception as e:
            print(f"❌ {variant}: {str(e)}")
    
    # Test 6: Check if it's a response format issue
    print("\n🧪 Test 6: Check response structure")
    print("-" * 40)
    try:
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "user", "content": "Hello"}
            ]
        )
        
        print(f"✅ Response object type: {type(response)}")
        print(f"   Choices count: {len(response.choices)}")
        if response.choices:
            choice = response.choices[0]
            print(f"   Choice type: {type(choice)}")
            print(f"   Message type: {type(choice.message)}")
            print(f"   Content: '{choice.message.content}'")
            print(f"   Content type: {type(choice.message.content)}")
            print(f"   Content length: {len(choice.message.content) if choice.message.content else 0}")
            
            # Check if content is None vs empty string
            if choice.message.content is None:
                print("   ⚠️  Content is None (not empty string)")
            elif choice.message.content == "":
                print("   ⚠️  Content is empty string")
            else:
                print("   ✅ Content has value")
                
    except Exception as e:
        print(f"❌ Response structure check failed: {str(e)}")


if __name__ == "__main__":
    debug_gpt5_systematically()
