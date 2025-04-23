from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Review
from company_app.models import Company
from django.contrib.auth.decorators import login_required  # Import login_required
from user_app.models import CustomUser
from django.shortcuts import get_object_or_404 #import get_object_or_404
from django.db.models import F #field look ups

@csrf_exempt
# @login_required  # Require user to be logged in
def addReview(request, company_id, user_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            review_text = data.get('review')
            rating = data.get('rating')
            price = data.get('price')
            music = data.get('music')
            amenities = data.get('amenities')
            food = data.get('food')
            vibes = data.get('vibes')
            pickup = data.get('pickup')
            costume = data.get('costume')
            value = data.get('value')
            service = data.get('service')
            if not review_text:
                return JsonResponse({"error": "Review text is required"}, status=400)

            if rating is None:
                return JsonResponse({"error": "Rating is required"}, status=400)

            company = get_object_or_404(Company, id=company_id)
            user = get_object_or_404(CustomUser, id=user_id) #get user object.

            review = Review(review=review_text, music=music, pickup=pickup, service=service, price=price, food=food, vibes=vibes,costume=costume, value=value, amenities=amenities,  company=company, user=user) #add user.
            print('this si add review', data)
            # return
            review.save()
            return JsonResponse({"message": "Review created!"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid method"}, status=405)
    
    
# @csrf_exempt
# from django.http import JsonResponse
# from .models import Company, Review

def getReviews(request, company_id):
    if request.method == "GET":
        try:
            company = Company.objects.get(id=company_id)
            reviews = Review.objects.filter(company=company).values(
                'review',
                'music',
                'service',
                'price',
                'food',
                'value',
                'amenities',
                'vibes',
                'costume',
                'pickup',
                'rating',
                'review_date',
                displayName=F('user__name')  # Access username from CustomUser
            )
            reviews_list = list(reviews)
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