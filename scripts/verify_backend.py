import requests
import json
import sys

base_url = "http://127.0.0.1:8000"

print("Starting verification...")

# Test Root
try:
    resp = requests.get(f"{base_url}/")
    print(f"Root: {resp.status_code} {resp.json()}")
except Exception as e:
    print(f"Root failed: {e}")
    sys.exit(1)

# Test Query
try:
    payload = {
        "question": "What is a robot?",
        "session_id": None,
        "query_type": "full_book"
    }
    print(f"Sending query: {payload}")
    resp = requests.post(f"{base_url}/api/v1/query", json=payload)
    print(f"Query Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"Answer: {data.get('answer')[:100]}...")
        session_id = data.get('session_id')
        print(f"Session ID: {session_id}")
        
        # Test Session History
        if session_id:
            print(f"Fetching history for session {session_id}...")
            resp_hist = requests.get(f"{base_url}/api/v1/sessions/{session_id}")
            print(f"History Status: {resp_hist.status_code}")
            if resp_hist.status_code == 200:
                msgs = resp_hist.json().get('messages', [])
                print(f"History: {len(msgs)} messages")
                print("Verification SUCCESS")
            else:
                print(f"History Error: {resp_hist.text}")
    else:
        print(f"Query Error: {resp.text}")

except Exception as e:
    print(f"Query failed: {e}")
