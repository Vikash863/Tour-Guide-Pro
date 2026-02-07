import requests
import json

# Test 1: Try to signup with duplicate email
print("Test 1: Duplicate email")
response = requests.post('http://localhost:8000/api/users/register/', json={
    'username': 'testdup',
    'email': 'vs7574258@gmail.com',  # This already exists
    'password': 'Test123456',
    'password_confirm': 'Test123456',
    'first_name': 'Test',
    'last_name': 'User'
})
print(f'Status: {response.status_code}')
print(f'Response: {response.text}')
print()

# Test 2: Try to signup with valid data
print("Test 2: Valid signup")
response = requests.post('http://localhost:8000/api/users/register/', json={
    'username': 'newuser999',
    'email': 'newuser999@test.com',
    'password': 'Test123456',
    'password_confirm': 'Test123456',
    'first_name': 'New',
    'last_name': 'User'
})
print(f'Status: {response.status_code}')
print(f'Response: {response.text}')
print()

# Test 3: Try to signup with mismatched passwords
print("Test 3: Mismatched passwords")
response = requests.post('http://localhost:8000/api/users/register/', json={
    'username': 'testmismatch',
    'email': 'testmismatch@test.com',
    'password': 'Test123456',
    'password_confirm': 'Different123',  # Doesn't match
    'first_name': 'Test',
    'last_name': 'User'
})
print(f'Status: {response.status_code}')
print(f'Response: {response.text}')
