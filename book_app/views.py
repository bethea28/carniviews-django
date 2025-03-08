from django.http import JsonResponse, HttpResponse
from .models import Books
import json

def book(request):
    myBooks = list(Books.objects.all().values())
    return JsonResponse(myBooks, safe=False)

def bookPost(request):
    if request.method == "POST":
        try:
            # Attempt to parse JSON first
            data = json.loads(request.body)
            title = data.get('title')
            author = data.get('author')
            year = data.get('year')

        except json.JSONDecodeError:
            # If JSON parsing fails, try request.POST (form data)
            title = request.POST.get('title')
            author = request.POST.get('author')
            year = request.POST.get('year')

        if not title:
            return JsonResponse({"error": "Title is required"}, status=400)

        books = Books(title=title, author=author, year=year)
        books.save()
        return JsonResponse({"message": "Book created!"})

    else:
        return JsonResponse({"error": "Invalid method"}, status=405)