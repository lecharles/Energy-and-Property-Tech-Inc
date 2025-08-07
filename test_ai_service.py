"""
Test AI Service for debugging
"""

import asyncio
from ai_service import AIService

async def test_ai_service():
    """Test the AI service"""
    print("🧪 Testing AI Service...")
    
    try:
        # Initialize AI service
        ai_service = AIService()
        print("✅ AI Service initialized")
        
        # Test query analysis
        print("\n🧠 Testing query analysis...")
        result = await ai_service.analyze_query("Analyze Q2 2025 performance")
        print(f"✅ Analysis result: {result}")
        
    except Exception as error:
        print(f"❌ Error: {error}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_ai_service()) 