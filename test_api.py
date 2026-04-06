import requests
import json

url = "https://personal-finance-advisor-agent-uwjp.onrender.com/upload-csv/"

files = {'file': open('sample_expenses.csv', 'rb')}

print(f"Sending request to {url}")
try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
