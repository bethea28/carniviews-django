from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Review
from .models import RevAgreement
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
            overall = data.get('overall')
            if not review_text:
                return JsonResponse({"error": "Review text is required"}, status=400)

            if rating is None:
                return JsonResponse({"error": "Rating is required"}, status=400)

            company = get_object_or_404(Company, id=company_id)
            user = get_object_or_404(CustomUser, id=user_id) #get user object.

            review = Review(overall=overall, review=review_text, music=music, pickup=pickup, service=service, price=price, food=food, vibes=vibes,costume=costume, value=value, amenities=amenities,  company=company, user=user) #add user.
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
from django.db.models import F

def getReviews(request, company_id):
    if request.method == "GET":
        try:
            company = Company.objects.get(id=company_id)
            reviews = Review.objects.filter(company=company).annotate(
                displayName=F('user__name')
            ).values(
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
                'id',
                'displayName'
            )

            reviews_list = list(reviews)

            # Get all RevAgreements for the reviews at once
            review_ids = [review['id'] for review in reviews_list]
            rev_agreements = RevAgreement.objects.filter(review_id__in=review_ids).values(
                'id', 'review_id', 'user_id', 'agreement'
            )

            # Organize agreements by review ID
            agreements_by_review = {}
            for agreement in rev_agreements:
                review_id = agreement['review_id']
                if review_id not in agreements_by_review:
                    agreements_by_review[review_id] = []
                agreements_by_review[review_id].append({
                    'id': agreement['id'],
                    'user_id': agreement['user_id'],
                    'agreement': agreement['agreement']
                })

            # Attach agreements to each review
            for review in reviews_list:
                review_id = review['id']
                review['revAgreements'] = agreements_by_review.get(review_id, [])

            return JsonResponse({"reviews": reviews_list})
        
        except Company.DoesNotExist:
            return JsonResponse({"error": "Company not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Invalid method"}, status=405)

    
@csrf_exempt
def addRevAgreement(request):
    if request.method == 'POST':
        request_data = json.loads(request.body)
        # companyId = request_data.get('company_id','')
        reviewId = request_data.get('reviewId','')
        userId = request_data.get('user_id','')
        agreement = request_data.get('agreement','')
        
        user = get_object_or_404(CustomUser, id=userId)
        review = get_object_or_404(Review, id=reviewId)

        # Check if a recommendation already exists for this user and company
        existing_revAgreement = RevAgreement.objects.filter(user=user, review=review).first()

        if existing_revAgreement:
            # Update the existing recommendation
            existing_revAgreement.agreement = agreement
            existing_revAgreement.save()
            return JsonResponse({'message': 'newRevAgreement successfully updated.'}, status=200)  # Use 200 for update
        else:
            # Create a new recommendation
            newRevAgreement = RevAgreement(agreement=agreement, user=user, review=review)
            newRevAgreement.save()
            return JsonResponse({'message': 'newRevAgreement successfully created.'}, status=201) # 201 for create
    return JsonResponse({'message': 'newRevAgreement Failed'}, status=500)


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
    





# @csrf_exempt
# def getReviewAgreements(request, company_id):
#     if request.method == 'GET':
#         companyId = company_id
#         company = RevAgreement.objects.get(id=companyId)
#         recs = Recommendation.objects.filter(company=company).values(
#             'rec',
#             'user_id'
#         )

#         allRecs=list(recs)
#         print('show me dictorary list DAREN', allRecs)
#         return JsonResponse({'message': 'Recommondation successfully retrieved', "allRecs": allRecs}, status=201)
#     return JsonResponse({'message': 'Recommondation Failed'}, status=500)

#     None