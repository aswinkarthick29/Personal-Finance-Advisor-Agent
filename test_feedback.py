import requests
import json

# Step 1: Upload CSV and get initial advice
print("=== STEP 1: Upload CSV ===")
url = "https://personal-finance-advisor-agent-uwjp.onrender.com/upload-csv/"
files = {'file': open('sample_expenses.csv', 'rb')}
r = requests.post(url, files=files)
print(f"Status: {r.status_code}")
data = r.json()
thread_id = data.get("thread_id")
print(f"Thread ID: {thread_id}")
print(f"Initial Advice: {data.get('advice', '')[:200]}...")

# Step 2: Send feedback and check if advice changes
print("\n=== STEP 2: Send Feedback ===")
feedback_url = "https://personal-finance-advisor-agent-uwjp.onrender.com/provide-feedback"
feedback_payload = {
    "thread_id": thread_id,
    "feedback_text": "I cannot reduce my rent, suggest alternatives for food savings"
}
r2 = requests.post(feedback_url, json=feedback_payload)
print(f"Status: {r2.status_code}")
data2 = r2.json()
print(f"Revised Advice: {data2.get('advice', '')[:400]}...")
