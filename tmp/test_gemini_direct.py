import requests

API_KEY = "AIzaSyAib6VS0KfI0e2pYcS8GjOXuqYf55ARSl8"
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

payload = {
    "contents": [{"parts": [{"text": "Say hello in Uzbek"}]}],
    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 100}
}

response = requests.post(url, params={"key": API_KEY}, json=payload, timeout=30)
print("Status:", response.status_code)
print("Body:", response.text[:500])
