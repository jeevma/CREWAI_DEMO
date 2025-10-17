#!/usr/bin/env python3
"""
Test script to debug Serp API issues
"""

import os
import requests
from dotenv import load_dotenv


def test_serper_api():
    """Test Serp API connection and authentication"""

    # Load environment variables
    load_dotenv()

    # Get API key
    api_key = os.getenv("SERP_API_KEY")

    print("=== Serp API Debug Test ===")
    print(f"API Key found: {'Yes' if api_key else 'No'}")

    if api_key:
        print(f"API Key length: {len(api_key)}")
        print(f"API Key starts with: {api_key[:8]}...")
        print(f"API Key ends with: ...{api_key[-8:]}")
    else:
        print("❌ SERP_API_KEY not found in environment variables")
        print("Available environment variables:")
        for key in os.environ.keys():
            if "SERP_API_KEY" in key.upper():
                print(f"  - {key}")
        return False

    # Test API call
    print("\n=== Testing API Call ===")

    url = "https://serpapi.com/search"
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}

    payload = {"q": "test query", "num": 3}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)

        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")

        if response.status_code == 200:
            print("✅ API call successful!")
            data = response.json()
            print(f"Results found: {len(data.get('organic', []))}")
            return True
        elif response.status_code == 403:
            print("❌ 403 Forbidden Error")
            print("Possible causes:")
            print("  1. Invalid API key")
            print("  2. API key not activated")
            print("  3. Insufficient credits")
            print("  4. Rate limit exceeded")
            print(f"Response: {response.text}")
            return False
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False


def test_crewai_serpapi():
    """Test SerpAPI from CrewAI"""

    print("\n=== Testing CrewAI SerpAPI ===")

    try:
        from crewai_tools import SerpAPI

        # Initialize the tool
        search_tool = SerpAPI()

        # Test search
        result = search_tool.run("test query")
        print("✅ SerpAPI working!")
        print(f"Result type: {type(result)}")
        print(f"Result preview: {str(result)[:200]}...")
        return True

    except Exception as e:
        print(f"❌ SerpAPI failed: {e}")
        return False


if __name__ == "__main__":
    print("Starting Serp API diagnostics...\n")

    # Test direct API
    api_success = test_serp_api()

    # Test CrewAI tool
    if api_success:
        test_crewai_serpapi()

    print("\n=== Troubleshooting Tips ===")
    print("1. Verify your API key at: https://serper.dev/dashboard")
    print("2. Check your account credits and usage limits")
    print("3. Ensure no extra spaces in .env file")
    print("4. Restart your Jupyter kernel after .env changes")
    print("5. Try regenerating your API key if issues persist")
