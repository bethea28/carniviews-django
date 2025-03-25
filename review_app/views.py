from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Review
from company_app.models import Company
from django.http import JsonResponse
from django.db.models import Avg
import math
# from .models import Company, Review  # Assuming your models are in the same app


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
            # if review_text == None |  rating == None:
            #     return JsonResponse({"error": "Both can't be empty"}, status=400)
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
    

@csrf_exempt
def getReviews(request, company_id):
    if request.method == "GET":
        try:
            company = Company.objects.get(id=company_id)
            reviews = Review.objects.filter(company=company).values('review', 'rating')  # Fetch reviews and serialize them
            reviews_list = list(reviews)  # Convert QuerySet to list for JSON serialization
            return JsonResponse({"reviews": reviews_list})
        except Company.DoesNotExist:
            return JsonResponse({"error": "Company not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid method"}, status=405)
    
    
@csrf_exempt
def getRatings(request, company_id):
    if request.method == "GET":
        try:
            company = Company.objects.get(id=company_id)
            average_rating = Review.objects.filter(company=company).aggregate(Avg('rating'))['rating__avg']

            if average_rating is not None:
                rounded_average = round(average_rating * 2) / 2.0  # Round to nearest 0.5
                return JsonResponse({'average_rating': rounded_average})
            else:
                return JsonResponse({'average_rating': 0.0})

        except Company.DoesNotExist:
            return JsonResponse({"error": "Company not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid method"}, status=405)