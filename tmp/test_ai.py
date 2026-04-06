import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from progress.ai_service import GeminiService

s = GeminiService()
try:
    result = s.explain_code('print("hello")')
    print('SUCCESS:', result[:200])
except RuntimeError as e:
    print('RuntimeError (kutilgan):', e)
except Exception as e:
    print('Kutilmagan xato:', type(e).__name__, ':', e)
