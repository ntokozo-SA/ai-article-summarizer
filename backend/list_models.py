import google.generativeai as genai
from config import GEMINI_API_KEY

def list_available_models():
    print("Listing available Gemini models...")
    
    try:
        # Configure the API
        genai.configure(api_key=GEMINI_API_KEY)
        
        # List all available models
        models = genai.list_models()
        
        print("✅ Available models:")
        for model in models:
            print(f"- {model.name}")
            
    except Exception as e:
        print(f"❌ Error listing models: {e}")

if __name__ == "__main__":
    list_available_models() 