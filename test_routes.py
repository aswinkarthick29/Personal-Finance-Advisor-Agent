import requests

print("Fetching docs to ensure FastAPI is actually running and returning valid schema:")
try:
    response = requests.get("https://personal-finance-advisor-agent-uwjp.onrender.com/openapi.json")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Registered Paths: {list(data.get('paths', {}).keys())}")
    else:
        print("Failed to get OpenAPI schema.")
except Exception as e:
    print(f"Error: {e}")
