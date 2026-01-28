import requests

API_KEY = "AIzaSyBZDSI3cOKh9uKRI0l5Ar9DYfj5AsioZ2g" # <= put your key here

if API_KEY.strip() == "" or "YOUR_" in API_KEY:
    raise ValueError("Bro put your actual DeepSeek API key in the variable.")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

url = "https://generativelanguage.googleapis.com"

try:
    resp = requests.get(url, headers=headers)
    print("Status Code:", resp.status_code)
    print("Balance Info:", resp.json())
except Exception as e:
    print("Error checking balance:", e)
