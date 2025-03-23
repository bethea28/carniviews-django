from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Review
from company_app.models import Company

@csrf_exempt
def addReview(request, company_id):  # Add company_id as a parameter
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            review_text = data.get('review')
            rating = data.get('rating')

            if not review_text:
                return JsonResponse({"error": "Review text is required"}, status=400)

            if rating is None:
                return JsonResponse({"error": "Rating is required"}, status=400)

            try:
                company = Company.objects.get(id=company_id)  # Use company_id from URL
            except Company.DoesNotExist:
                return JsonResponse({"error": "Company not found"}, status=404)

            review = Review(review=review_text, rating=rating, company=company)
            review.save()
            return JsonResponse({"message": "Review created!"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid method"}, status=405)