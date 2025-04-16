from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from company_app.models import Company  # Correct import for Company
from user_app.models import CustomUser  # Correct import for CustomUser
from images_app.models import Image
from django.shortcuts import get_object_or_404

@csrf_exempt
def addCompanyImages(request, company_id, user_id):
    """API endpoint to add images to an existing company."""

    if request.method == 'POST':
        try:
            company = Company.objects.get(id=company_id) # Retrieve the company object.
            user = CustomUser.objects.get(id=user_id) # Retrieve the company object.
            request_data = json.loads(request.body)
            image_urls = request_data.get('imageUrls', [])
            print('adding image money', image_urls)

            for image_url in image_urls:
                Image.objects.create(company=company, image_url=image_url, user=user) # create images.

            return JsonResponse({'message': 'Images added successfully'}, status=201)

        except Company.DoesNotExist:
            return JsonResponse({'error': 'Company not found'}, status=404)
        except (json.JSONDecodeError, KeyError) as e:
            return JsonResponse({'error': f'Invalid request: {e}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)





@csrf_exempt  # Consider removing this in production and handling CSRF properly
def getCompanyImages(request, company_id):  # Removed POST-specific logic, user_id might not be needed
    """API endpoint to GET all images associated with a specific company."""

    if request.method == 'GET':
        try:
            company = get_object_or_404(Company, id=company_id)

            # Filter images based on the company
            images = Image.objects.filter(company=company)  # Assuming your Image model has a 'company' ForeignKey

            # Serialize the image data into a list of dictionaries
            image_data = [{'id': img.id, 'image_url': img.image_url, 'alt_text': img.alt_text} for img in images]

            return JsonResponse({'images': image_data}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)