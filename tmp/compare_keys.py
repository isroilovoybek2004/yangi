import requests

# Ikkala kalitni solishtirib tekshirish
keys = {
    "Eski kalit": "AIzaSyAib6VS0KfI0e2pYcS8GjOXuqYf55ARSl8",
    "Yangi kalit": "AIzaSyAKleHBZ3SAlc0qoVMR4dCK4sXAhW1MeTk"
}

for name, key in keys.items():
    # Models ro'yxatini olish — bu ham kvota sarflaydi
    r = requests.get(
        "https://generativelanguage.googleapis.com/v1beta/models",
        params={"key": key},
        timeout=10
    )
    if r.ok:
        data = r.json()
        model_count = len(data.get("models", []))
        print(f"{name}: OK — {model_count} ta model mavjud")
    else:
        err = r.json().get("error", {})
        print(f"{name}: XATO {r.status_code} — {err.get('status', '')} | {err.get('message', '')[:100]}")
