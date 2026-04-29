from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from progress.models import Progress, Submission
from progress.serializers import ProgressSerializer, SubmissionSerializer
from gamification.services import GamificationService
from lessons.models import Task
import subprocess
import sys
import re

class ProgressViewSet(viewsets.ModelViewSet):
    serializer_class = ProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Progress.objects.filter(user=self.request.user)

class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Talabaning o'zini biriktiramiz
        submission = serializer.save(user=request.user)
        
        submitted_answer = submission.submitted_answer
        
        # 1. Havfsizlik tekshiruvi (Minimal Sandboxing)
        forbidden_patterns = [
            r'import\s+os', r'import\s+subprocess', r'import\s+sys', 
            r'__import__', r'eval\(', r'exec\(', r'open\('
        ]
        
        is_safe = True
        for pattern in forbidden_patterns:
            if re.search(pattern, submitted_answer):
                is_safe = False
                break
                
        if not is_safe:
            submission.is_correct = False
            submission.ai_feedback = "Kodingiz bloklandi: 'os', 'sys', 'open' kabi xavfli buyruqlar taqiqlanadi!"
        else:
            # 2. Kodni ishga tushirish (Subprocess)
            try:
                result = subprocess.run(
                    [sys.executable, "-c", submitted_answer],
                    capture_output=True,
                    text=True,
                    timeout=3
                )

                if result.returncode != 0:
                    # Sintaksis yoki runtime xatosi
                    submission.is_correct = False
                    submission.ai_feedback = f"{result.stderr.strip()}"
                else:
                    # Kod ishladi — natijani expected_output bilan taqqoslaymiz
                    actual_output = result.stdout.strip()
                    try:
                        task_obj = Task.objects.get(pk=submission.task_id)
                        expected = task_obj.expected_output.strip()
                    except Task.DoesNotExist:
                        expected = ""

                    if expected and actual_output == expected:
                        submission.is_correct = True
                        submission.ai_feedback = actual_output
                    elif not expected:
                        # expected_output bo'sh qoldirilgan bo'lsa — ishlashi yetarli
                        submission.is_correct = True
                        submission.ai_feedback = actual_output or "Kod muvaffaqiyatli bajarildi."
                    else:
                        submission.is_correct = False
                        submission.ai_feedback = (
                            f"Kutilgan natija:\n{expected}\n\n"
                            f"Sizning natijangiz:\n{actual_output}"
                        )
            except subprocess.TimeoutExpired:
                submission.is_correct = False
                submission.ai_feedback = "Time Limit Exceeded: Kod 3 soniyadan ortiq ishladi."
            except Exception as e:
                submission.is_correct = False
                submission.ai_feedback = f"System Error: {str(e)}"

        submission.save()

        # Progress ni avtomat yangilaymiz
        progress, created = Progress.objects.get_or_create(
            user=request.user,
            task=submission.task
        )
        if submission.is_correct:
            progress.is_completed = True
            progress.score = 100
            progress.ai_feedback = "Muvaffaqiyatli bajarildi!"
        progress.save()

        # ─── Gamification: XP berish va Badge tekshirish ─────────────────
        new_badges = []
        if submission.is_correct:
            profile = GamificationService.award_xp(
                user=request.user,
                amount=GamificationService.XP_CORRECT_SUBMISSION,
                reason=f"Task #{submission.task_id} topshirig'i to'g'ri bajarildi"
            )
            new_badges = GamificationService.check_and_award_badges(request.user)
        # ─────────────────────────────────────────────────────────────────

        # Custom response for frontend
        return Response({
            "is_correct":  submission.is_correct,
            "ai_feedback": submission.ai_feedback,
            "xp_earned":   GamificationService.XP_CORRECT_SUBMISSION if submission.is_correct else 0,
            "new_badges":  [b.name for b in new_badges],
        }, status=status.HTTP_201_CREATED)

from rest_framework.views import APIView
from progress.ai_service import GeminiService

class AIAssistView(APIView):
    """
    Kodni tushuntirish, xatoni tahlil qilish va yordam (hint) so'rash uchun maxsus endpoint.
    URL pattern: /api/progress/ai/<action_type>/ (action_type: 'explain', 'analyze', 'hint')
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, action_type):
        code = request.data.get('code', '')
        task_question = request.data.get('task_question', '')
        error_message = request.data.get('error_message', '')

        try:
            service = GeminiService()
            if action_type == 'explain':
                if not code.strip():
                    return Response({"error": "Tushuntirish uchun kod kiritmadingiz."}, status=400)
                result = service.explain_code(code)

            elif action_type == 'hint':
                result = service.get_hint(task_question, code)

            elif action_type == 'analyze':
                result = service.analyze_error(code, error_message)

            else:
                return Response({"error": "Noto'g'ri action_type ko'rsatildi."}, status=400)

            return Response({"ai_response": result}, status=200)

        except ValueError as ve:
            # API kaliti o'rnatilmagan
            return Response({"error": str(ve)}, status=501)
        except RuntimeError as re:
            # Gemini API xatolari: kvota tugagan (429), timeout, tarmoq xatosi
            err_msg = str(re)
            if '429' in err_msg:
                user_msg = (
                    "⚠️ AI xizmati hozirda vaqtinchalik to'xtab turibdi (API limiti tugadi). "
                    "Bir necha daqiqadan so'ng qayta urinib ko'ring."
                )
            elif 'javob bermadi' in err_msg or 'Timeout' in err_msg.lower():
                user_msg = "⏱️ AI server javob bermadi. Internet aloqangizni tekshirib, qayta urinib ko'ring."
            else:
                user_msg = f"🤖 AI xizmati bilan bog'liqda muammo: {err_msg}"
            return Response({"error": user_msg}, status=503)
        except Exception as e:
            return Response({"error": f"Server xatoligi: {str(e)}"}, status=500)


class QuizXPView(APIView):
    """
    Quiz to'g'ri yechilganda XP berish.
    POST /api/progress/quiz-xp/
    """
    permission_classes = [permissions.IsAuthenticated]

    XP_QUIZ_COMPLETE = 5  # Quiz uchun XP

    def post(self, request):
        try:
            profile = GamificationService.award_xp(
                user=request.user,
                amount=self.XP_QUIZ_COMPLETE,
                reason="Quiz muvaffaqiyatli yakunlandi"
            )
            new_badges = GamificationService.check_and_award_badges(request.user)
            return Response({
                "xp_earned": self.XP_QUIZ_COMPLETE,
                "total_xp": profile.xp,
                "level": profile.level,
                "level_name": profile.level_name,
                "new_badges": [b.name for b in new_badges],
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

