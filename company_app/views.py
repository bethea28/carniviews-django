from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Company
from images_app.models import Image  # Import the Image model

@csrf_exempt
def addCompany(request):
    """
    Creates a Company object and associated Image objects from a JSON request body.
    """
    if request.method == 'POST':
        print('add Company now', request.body)
        try:
            request_data = json.loads(request.body)
            company_info = request_data.get('companyInfo', {})
            image_urls = request_data.get('imageUrls', [])  # Corrected line
            hours_data = request_data.get('hoursData', {})

            company = Company()
            company.set_companyInfo(company_info)
            company.set_hoursData(hours_data)
            company.save()

            # Create Image objects and associate them with the Company
            for image_url in image_urls:
                Image.objects.create(company=company, image_url=image_url)

            return JsonResponse({'message': 'Company and images created successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing key in request body: {e}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def getCompanies(request):
    """
    Retrieves all companies and their associated images.
    """
    if request.method == 'GET':
        try:
            companies = Company.objects.all()
            company_list = []

            for company in companies:
                company_data = {
                    'id': company.id,
                    'companyInfo': company.get_companyInfo(),
                    'hoursData': company.get_hoursData(),
                    'images': [{'id': image.id, 'image_url': image.image_url} for image in company.images.all()] #Gets all related images.
                }
                company_list.append(company_data)

            return JsonResponse(company_list, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)