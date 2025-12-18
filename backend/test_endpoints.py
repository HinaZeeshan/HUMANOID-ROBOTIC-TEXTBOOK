from fastapi.testclient import TestClient
from unittest.mock import patch
import sys
import os

# Ensure backend path is set
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.api.main import app
from backend.config.settings import settings

print(f"DEBUG: Loaded COHERE_API_KEY: '{settings.COHERE_API_KEY}'")

def test_endpoints():
    client = TestClient(app)

    print("\n--- Testing /query endpoint ---")
    response = client.post("/api/v1/query", json={
        "question": "What is humanoid robotics?",
        # Don't send session_id to let backend generate one, or send one but capture what comes back
        # If we send one, backend will create a NEW one if it doesn't exist.
    })
    print(f"Status Code: {response.status_code}")
    
    session_id_to_check = None
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response keys: {data.keys()}")
        session_id_to_check = data.get("session_id")
        print(f"Returned Session ID: {session_id_to_check}")
        
        if data.get("answer") and "I'm sorry" in data["answer"]:
            print("Note: Received fallback response (expected with invalid key).")
        else:
            print("Received actual response.")
    else:
        print(f"Error: {response.text}")

    print("\n--- Testing /query-selected-text endpoint ---")
    response = client.post("/api/v1/query-selected-text", json={
        "question": "Explain this text",
        "selected_text": "Robots are cool.",
        "session_id": session_id_to_check # Use the same session
    })
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Success.")
    else:
        print(f"Error: {response.text}")

    print(f"\n--- Testing Session Management for {session_id_to_check} ---")
    if session_id_to_check:
        response = client.get(f"/api/v1/sessions/{session_id_to_check}")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            messages = data.get("messages", [])
            print(f"Session Messages: {len(messages)}")
            if len(messages) > 0:
                print("SUCCESS: Session persistence working.")
            else:
                print("FAILURE: Session found but no messages (persistence issue).")
        else:
             print(f"Error: {response.text}")
    else:
        print("Skipping session check because query failed to return session_id")

if __name__ == "__main__":
    test_endpoints()
