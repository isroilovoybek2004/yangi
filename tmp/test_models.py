import requests

API_KEY = "AIzaSyAib6VS0KfI0e2pYcS8GjOXuqYf55ARSl8"

# gemini-2.0-flash-lite sinash
for model in ["gemini-2.0-flash-lite", "gemini-2.0-flash"]:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    payload = {
        "contents": [{"parts": [{"text": "Say 'Salom!' only."}]}],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 20}
    }
    r = requests.post(url, params={"key": API_KEY}, json=payload, timeout=20)
    print(f"Model: {model} | Status: {r.status_code}")
    if r.ok:
        data = r.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        print(f"  Response: {text[:100]}")
        break
    else:
        err = r.json().get("error", {})
        print(f"  Error: {err.get('status', '')} - {err.get('message', '')[:100]}")
