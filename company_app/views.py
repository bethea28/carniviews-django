# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from .models import Company
# from images_app.models import Image
# from django.contrib.auth.decorators import login_required  # Import login_required

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Company
from images_app.models import Image
# from django.contrib.auth.models import User  # Import User model
from django.shortcuts import get_object_or_404 #import get_object_or_404
# from user_app.models import Image
from user_app.models import CustomUser
@csrf_exempt
def addCompany(request, user_id):  # Accept user_id from URL
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

            # Get the user object based on user_id
            user = get_object_or_404(CustomUser, id=user_id) #get user object by user id.
            all = CustomUser.objects.all()
            print('all users bryan',all )
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
                description=company_info.get('description', ''),
                user=user  # Associate with the user from URL
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
    Retrieves companies with optional skip and limit parameters for pagination.
    """
    if request.method == 'GET':
        try:
            companies = Company.objects.all()
            skip_str = request.GET.get('skip')
            limit_str = request.GET.get('limit')

            start = 0
            if skip_str is not None and skip_str.isdigit():
                start = int(skip_str)
                companies = companies[start:]

            end = None
            if limit_str is not None and limit_str.isdigit():
                end = int(limit_str)
                companies = companies[:end]

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
                        'description': company.description,
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