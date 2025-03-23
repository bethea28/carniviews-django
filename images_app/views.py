from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from company_app.models import Company  # Correct import for Company
from images_app.models import Image

@csrf_exempt
def addCompanyImages(request, company_id):
    """API endpoint to add images to an existing company."""

    if request.method == 'POST':
        try:
            company = Company.objects.get(id=company_id) # Retrieve the company object.

            request_data = json.loads(request.body)
            image_urls = request_data.get('imageUrls', [])

            for image_url in image_urls:
                Image.objects.create(company=company, image_url=image_url) # create images.

            return JsonResponse({'message': 'Images added successfully'}, status=201)

        except Company.DoesNotExist:
            return JsonResponse({'error': 'Company not found'}, status=404)
        except (json.JSONDecodeError, KeyError) as e:
            return JsonResponse({'error': f'Invalid request: {e}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)