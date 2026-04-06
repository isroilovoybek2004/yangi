import requests

API_KEY = "AIzaSyAKleHBZ3SAlc0qoVMR4dCK4sXAhW1MeTk"
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent"

payload = {
    "contents": [{"parts": [{"text": "Python kodini tushuntir: print('Salom, dunyo!')"}]}],
    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 300}
}

r = requests.post(url, params={"key": API_KEY}, json=payload, timeout=20)
print("Status:", r.status_code)
if r.ok:
    text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
    print("AI javobi:\n" + text[:500])
else:
    err = r.json().get("error", {})
    print("Xato: " + str(r.status_code) + " " + err.get("status", "") + " - " + err.get("message", "")[:200])
