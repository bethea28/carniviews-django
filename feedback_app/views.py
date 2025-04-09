from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required  # Import login_required
from feedback_app.models import Feedback
from django.shortcuts import get_object_or_404 #import get_object_or_404
from django.db.models import F #field look ups

@csrf_exempt
# @login_required  # Require user to be logged in
def addFeedback(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            feedback_text = data.get('feedback')

            if not feedback_text:
                return JsonResponse({"error": "Feedback text is required"}, status=400)

            feedback = Feedback(feedback=feedback_text) #add user.
            feedback.save()
            return JsonResponse({"message": "Feedback created!"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid method"}, status=405)
    
   