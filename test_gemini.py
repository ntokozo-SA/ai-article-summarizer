import google.generativeai as genai
from config import GEMINI_API_KEY

def test_gemini_api():
    print("Testing Google Gemini API...")
    
    try:
        # Configure the API
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        # Test with a simple prompt
        test_prompt = "Please provide a brief summary of artificial intelligence in 2 sentences."
        
        print("Sending test request to Gemini API...")
        response = model.generate_content(test_prompt)
        
        print("✅ API Response:")
        print(response.text)
        print("\n✅ Gemini API is working correctly!")
        
    except Exception as e:
        print(f"❌ Error with Gemini API: {e}")
        print("\nPossible issues:")
        print("1. API key might be invalid or expired")
        print("2. Network connectivity issues")
        print("3. API rate limits exceeded")
        print("4. API service temporarily unavailable")

if __name__ == "__main__":
    test_gemini_api() 