import requests

API_KEY = "AIzaSyAKleHBZ3SAlc0qoVMR4dCK4sXAhW1MeTk"

models = [
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash-lite-001",
    "gemini-flash-lite-latest",
    "gemini-flash-latest",
    "gemini-2.0-flash",
]

for model in models:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    payload = {
        "contents": [{"parts": [{"text": "Hi"}]}],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 10}
    }
    r = requests.post(url, params={"key": API_KEY}, json=payload, timeout=15)
    if r.ok:
        text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        print("[OK] " + model + ": " + text.strip()[:50])
        break
    else:
        err = r.json().get("error", {})
        status = err.get("status", "")
        msg = err.get("message", "")[:80]
        print("[FAIL] " + model + ": " + str(r.status_code) + " " + status + " - " + msg)
