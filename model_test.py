#!/usr/bin/env python3
"""
Model Test

Test different models to see what's working.
"""

import os
from openai import OpenAI


def test_models():
    """Test different models."""
    
    print("🧪 Testing Different Models")
    print("=" * 40)
    
    # Load environment
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"API Key: {'✅ Found' if api_key else '❌ Missing'}")
    
    if not api_key:
        return
    
    client = OpenAI(api_key=api_key)
    
    # Test different models
    models_to_test = [
        "gpt-4o",
        "gpt-4o-mini", 
        "gpt-5",
        "gpt-5-mini",
        "gpt-5-nano"
    ]
    
    for model in models_to_test:
        print(f"\n🔍 Testing {model}...")
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": "Say 'Hello'"}
                ],
                max_completion_tokens=10
            )
            
            result = response.choices[0].message.content
            print(f"✅ {model}: '{result}'")
            
        except Exception as e:
            print(f"❌ {model}: {str(e)}")
            print(f"   Error type: {type(e).__name__}")


if __name__ == "__main__":
    test_models()
