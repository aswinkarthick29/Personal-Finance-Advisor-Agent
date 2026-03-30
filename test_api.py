import requests
import json

url = "http://127.0.0.1:9002/upload-csv/"
files = {'file': open('sample_expenses.csv', 'rb')}

print(f"Sending request to {url}")
try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
