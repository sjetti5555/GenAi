import requests
import json

# The Flask app's URL
url = "http://127.0.0.1:5000/analyze"

# JSON payload for the request
payload = {
    "urls": [
        "https://www.youtube.com/watch?v=abc123",  # Replace with real video IDs
        "https://www.youtube.com/watch?v=def456"   # Replace with real video IDs
    ],
    "limit": 2
}

# Send POST request
response = requests.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})

# Print the response
print("Response Status Code:", response.status_code)
print("Response JSON:", response.json())
