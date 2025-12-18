import requests
import json

# Test the query endpoint
def test_query_endpoint():
    url = "http://localhost:8000/api/v1/query"

    # Test data
    test_data = {
        "question": "What is humanoid robotics?",
        "selected_text": None,
        "query_type": "full_book"
    }

    try:
        response = requests.post(url, json=test_data, headers={"Content-Type": "application/json"})
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            data = response.json()
            print(f"Answer: {data.get('answer', 'No answer field')}")
            print(f"Source Citations: {data.get('source_citations', [])}")
            print("SUCCESS: Query endpoint test passed")
        else:
            print(f"FAILURE: Query endpoint test failed with status {response.status_code}")
    except Exception as e:
        print(f"FAILURE: Query endpoint test failed with error: {e}")

# Test the query-selected-text endpoint
def test_query_selected_text_endpoint():
    url = "http://localhost:8000/api/v1/query-selected-text"

    # Test data
    test_data = {
        "question": "Based on this text, what is the main concept?",
        "selected_text": "Humanoid robotics is a branch of robotics that focuses on creating robots with human-like characteristics.",
        "query_type": "selected_text_only"
    }

    try:
        response = requests.post(url, json=test_data, headers={"Content-Type": "application/json"})
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            data = response.json()
            print(f"Answer: {data.get('answer', 'No answer field')}")
            print(f"Source Citations: {data.get('source_citations', [])}")
            print("SUCCESS: Query selected text endpoint test passed")
        else:
            print(f"FAILURE: Query selected text endpoint test failed with status {response.status_code}")
    except Exception as e:
        print(f"FAILURE: Query selected text endpoint test failed with error: {e}")

# Test the get session endpoint
def test_get_session_endpoint():
    url = "http://localhost:8000/api/v1/sessions/test_session_123"

    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code in [200, 404]:  # 404 is expected for non-existent session
            print("SUCCESS: Get session endpoint test passed")
        else:
            print(f"FAILURE: Get session endpoint test failed with status {response.status_code}")
    except Exception as e:
        print(f"FAILURE: Get session endpoint test failed with error: {e}")

if __name__ == "__main__":
    print("Testing backend endpoints...")
    print("\n1. Testing /api/v1/query endpoint:")
    test_query_endpoint()

    print("\n2. Testing /api/v1/query-selected-text endpoint:")
    test_query_selected_text_endpoint()

    print("\n3. Testing /api/v1/sessions/{session_id} endpoint:")
    test_get_session_endpoint()

    print("\nTesting completed.")