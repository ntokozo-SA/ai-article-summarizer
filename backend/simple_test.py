import google.generativeai as genai
from config import GEMINI_API_KEY

def simple_test():
    print("Testing Gemini API with minimal content...")
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Very simple prompt
        response = model.generate_content("Say hello in one sentence.")
        
        print("✅ Success!")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    simple_test() 