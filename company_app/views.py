from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Company
from images_app.models import Image

@csrf_exempt
def addCompany(request):
    """
    Creates a Company object and associated Image objects from a JSON request body,
    with companyInfo stored in separate columns.
    """
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
            company_info = request_data.get('companyInfo', {})
            image_urls = request_data.get('imageUrls', [])
            hours_data = request_data.get('hoursData', {})

            # Create Company object, populating individual fields
            company = Company(
                name=company_info.get('name', ''),
                address=company_info.get('address', ''),
                city=company_info.get('city', ''),
                state=company_info.get('state', ''),
                zip_code=company_info.get('zip', ''),
                hours=company_info.get('hours', ''),
                company_type=company_info.get('type', ''),
                photos=company_info.get('photos', []),
                hoursData=hours_data,
                description=company_info.get('description', '')  # Include description here
            )
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
    Retrieves all companies and their associated images, with companyInfo from separate columns.
    """
    if request.method == 'GET':
        try:
            companies = Company.objects.all()
            company_list = []

            for company in companies:
                company_data = {
                    'id': company.id,
                    'companyInfo': {
                        'name': company.name,
                        'address': company.address,
                        'city': company.city,
                        'state': company.state,
                        'zip': company.zip_code,
                        'hours': company.hours,
                        'type': company.company_type,
                        'photos': company.photos,
                        'description': company.description,  # Include description here
                    },
                    'hoursData': company.hoursData,
                    'images': [{'id': image.id, 'image_url': image.image_url} for image in company.images.all()]
                }
                company_list.append(company_data)

            return JsonResponse(company_list, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)