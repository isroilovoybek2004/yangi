import requests
from django.conf import settings


class GeminiService:
    """
    Gemini API ga to'g'ridan-to'g'ri HTTP so'rovlar orqali murojaat qiladi.
    google-genai yoki google-generativeai kutubxonasiga bog'liq emas.
    """
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    MODEL_NAME = "gemini-flash-lite-latest"  # Kvotasi mavjud, tez model

    def __init__(self):
        self.api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not self.api_key or self.api_key == "YOUR_API_KEY_HERE":
            raise ValueError("Tarmoq ma'muri (Admin) settings.py da GEMINI_API_KEY o'rnatmagan.")

    def _generate(self, prompt: str) -> str:
        """Gemini API ga so'rov yuboradi va matnli javob qaytaradi."""
        url = self.GEMINI_API_URL.format(model=self.MODEL_NAME)
        params = {"key": self.api_key}
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1024,
            }
        }
        try:
            response = requests.post(url, params=params, json=payload, timeout=30)
            # 429 yoki boshqa HTTP xatolarni tekshirish
            if response.status_code == 429:
                raise RuntimeError("429: API kvotasi tugadi. Keyinroq qayta urinib ko'ring.")
            if not response.ok:
                try:
                    err_data = response.json()
                    err_msg = err_data.get('error', {}).get('message', response.text[:200])
                except Exception:
                    err_msg = response.text[:200]
                raise RuntimeError(f"AI API xatosi ({response.status_code}): {err_msg}")
            data = response.json()
            # API javobidan matnni olamiz
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except RuntimeError:
            raise  # RuntimeError ni qayta throw qilamiz
        except requests.exceptions.Timeout:
            raise RuntimeError("AI server javob bermadi (30 soniya kutildi).")
        except (KeyError, IndexError):
            raise RuntimeError("AI dan kutilmagan javob formati keldi.")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Tarmoq xatosi: {str(e)}")


    def explain_code(self, code: str) -> str:
        prompt = (
            f"Mana bu Python kod bor:\n```python\n{code}\n```\n"
            f"Iltimos ushbu kod qanday ishlashi va nima vazifani bajarishini "
            f"mutlaqo oddiy so'zlar bilan, tushunarli tilda O'zbek tilida tushuntirib bering."
        )
        return self._generate(prompt)

    def analyze_error(self, code: str, error_message: str) -> str:
        prompt = (
            f"Ushbu kod ishlatilganda quyidagi xatoni (error) bermoqda:\n\n"
            f"Kod:\n```python\n{code}\n```\n\n"
            f"Xatolik:\n{error_message}\n\n"
            f"Iltimos nima xato bo'layotganini va uni qanday to'g'irlash mumkinligini "
            f"O'zbek tilida tushuntiring."
        )
        return self._generate(prompt)

    def get_hint(self, task_question: str, current_code: str) -> str:
        prompt = (
            f"O'quvchi ushbu masalani ishlashga harakat qilmoqda:\n'{task_question}'\n\n"
            f"Hozircha u yozgan kod shunday ko'rinishda:\n```python\n{current_code}\n```\n"
            f"Iltimos, o'quvchiga kodni bitta joyiga (to'g'ridan to'g'ri javobini yozmasdan) "
            f"yo'nalish bering. Yengil yordamchi fikr (Hint) O'zbek tilida bering."
        )
        return self._generate(prompt)
