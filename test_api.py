"""
Quick test script to debug Sunbird API calls
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("SUNBIRD_API_TOKEN")
BASE_URL = "https://api.sunbird.ai"

print(f"Token exists: {bool(API_TOKEN)}")
print(f"Token (first 20 chars): {API_TOKEN[:20] if API_TOKEN else 'MISSING'}...")

# Test 1: Simple Inference (Summarization)
print("\n=== Testing Sunflower Simple (Summarization) ===")
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "instruction": "Summarize this text: The quick brown fox jumps over the lazy dog."
}

response = requests.post(f"{BASE_URL}/tasks/sunflower_simple", json=payload, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

# Test 2: Try with model_type parameter
print("\n=== Testing with model_type parameter ===")
payload2 = {
    "instruction": "Summarize this text: The quick brown fox jumps over the lazy dog.",
    "model_type": "qwen"
}

response2 = requests.post(f"{BASE_URL}/tasks/sunflower_simple", json=payload2, headers=headers)
print(f"Status: {response2.status_code}")
print(f"Response: {response2.text}")

# Test 3: Try chat endpoint instead
print("\n=== Testing Chat Inference ===")
payload3 = {
    "messages": [
        {"role": "user", "content": "Summarize this text: The quick brown fox jumps over the lazy dog."}
    ]
}

response3 = requests.post(f"{BASE_URL}/tasks/sunflower_inference", json=payload3, headers=headers)
print(f"Status: {response3.status_code}")
print(f"Response: {response3.text}")

# Test 4: Check what endpoints are available
print("\n=== Checking available endpoints ===")
response4 = requests.get(f"{BASE_URL}/", headers=headers)
print(f"Status: {response4.status_code}")
print(f"Response: {response4.text[:500]}")
