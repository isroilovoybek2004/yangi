import requests, sys

API_KEY = "AIzaSyD1nwUwF1W4lXAzgZ7I9lR7Ake38sH2pUM"

models = [
    "gemini-2.0-flash",
    "gemini-flash-lite-latest",
    "gemini-2.0-flash-lite",
]

for model in models:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    payload = {
        "contents": [{"parts": [{"text": "Python: print('Salom!') kodini tushuntir"}]}],
        "generationConfig": {"temperature": 0.5, "maxOutputTokens": 200}
    }
    r = requests.post(url, params={"key": API_KEY}, json=payload, timeout=20)
    if r.ok:
        text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        sys.stdout.buffer.write(("[OK] " + model + ":\n" + text[:300] + "\n").encode("utf-8"))
        break
    else:
        err = r.json().get("error", {})
        msg = err.get("status", "") + " - " + err.get("message", "")[:80]
        sys.stdout.buffer.write(("[FAIL] " + model + ": " + msg + "\n").encode("utf-8"))
