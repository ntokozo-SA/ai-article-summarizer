import requests
import time

def test_server():
    print("Testing Flask server...")
    
    # Wait a moment for server to start
    time.sleep(2)
    
    try:
        response = requests.get('http://localhost:5000/health')
        if response.status_code == 200:
            print("✅ Server is running!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Server responded with status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_server() 