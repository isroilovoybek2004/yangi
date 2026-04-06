import requests

API_KEY = "AIzaSyAib6VS0KfI0e2pYcS8GjOXuqYf55ARSl8"

# Mavjud modellar ro'yxatini olish
response = requests.get(
    "https://generativelanguage.googleapis.com/v1beta/models",
    params={"key": API_KEY},
    timeout=15
)
print("Status:", response.status_code)
if response.ok:
    data = response.json()
    for m in data.get("models", []):
        if "generateContent" in m.get("supportedGenerationMethods", []):
            print("MODEL:", m["name"], "|", m.get("displayName", ""))
else:
    print("Error:", response.text[:300])
