#!/usr/bin/env python3
"""
Simple GPT-5 Test

Very basic test to see if GPT-5 is working.
"""

import os
from openai import OpenAI


def simple_test():
    """Very simple GPT-5 test."""
    
    print("🧪 Simple GPT-5 Test")
    print("=" * 30)
    
    # Load environment
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"API Key: {'✅ Found' if api_key else '❌ Missing'}")
    
    if not api_key:
        return
    
    try:
        client = OpenAI(api_key=api_key)
        print("✅ Client initialized")
        
        # Very simple request
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "user", "content": "Say 'Hello World' and nothing else."}
            ],
            max_completion_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"✅ Response received: '{result}'")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print(f"Error type: {type(e)}")


if __name__ == "__main__":
    simple_test()
