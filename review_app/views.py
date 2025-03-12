from django.http import JsonResponse, HttpResponse
from .models import Review
import json

# def book(request):
#     myBooks = list(Books.objects.all().values())
#     return JsonResponse(myBooks, safe=False)

def addReview(request):
    if request.method == "POST":
        try:
            # Attempt to parse JSON first
            data = json.loads(request.body)
            review = data.get('review')
            # author = data.get('author')
            # year = data.get('year')

        except json.JSONDecodeError:
            # If JSON parsing fails, try request.POST (form data)
            review = request.POST.get('review')
            # author = request.POST.get('author')
            # year = request.POST.get('year')

        if not review:
            return JsonResponse({"error": "Title is required"}, status=400)

        reviews = Review(review=review)
        reviews.save()
        return JsonResponse({"message": "review created!"})

    else:
        return JsonResponse({"error": "Invalid method"}, status=405)