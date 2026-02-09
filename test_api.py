import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Test registration
print("Testing registration...")
try:
    response = requests.post(
        f"{BASE_URL}/api/users/register/",
        json={
            "username": "testuser",
            "email": "test@test.com",
            "password": "testpass123",
            "password_confirm": "testpass123"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}")
except Exception as e:
    print(f"Error: {e}")

# Test login
print("\nTesting login...")
try:
    response = requests.post(
        f"{BASE_URL}/api/users/login/",
        json={
            "username": "testuser",
            "password": "testpass123"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}")
except Exception as e:
    print(f"Error: {e}")
