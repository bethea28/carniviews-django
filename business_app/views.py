
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# from models import Company
from images_app.models import Image
# from django.contrib.auth.models import User  # Import User model
from django.shortcuts import get_object_or_404 #import get_object_or_404
# from user_app.models import Image
from user_app.models import CustomUser
from django.db.models import F
# from models import Recommendation

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Business
from images_app.models import Image
from django.shortcuts import get_object_or_404
from user_app.models import CustomUser
from django.db.models import F

@csrf_exempt
   

@csrf_exempt
def addBusiness(request, user_id):  # Accept user_id from URL
    """
    Creates a Company object and associated Image objects from a JSON request body,
    with companyInfo stored in separate columns.
    """
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
            company_info = request_data.get('companyInfo', "")
            name = company_info.get('name', "")
            image_urls = request_data.get('imageUrls', [])
            hours_data = request_data.get('hoursData', {})

            # Get the user object based on user_id
            user = get_object_or_404(CustomUser, id=user_id) #get user object by user id.
            all = CustomUser.objects.all()
            print('BUSIENA ADDING NOW',user )
            # Create Company object, populating individual fields
            business = Business(
                name=name,
                address=company_info.get('address', ''),
                city=company_info.get('city', ''),
                state=company_info.get('state', ''),
                zip_code=company_info.get('zip', ''),
                hours=company_info.get('hours', ''),
                contact=company_info.get('contact', ''),
                website=company_info.get('website', ''),
                company_type=company_info.get('type', ''),
                photos=company_info.get('photos', []),
                hoursData=hours_data,
                description=company_info.get('description', ''),
                user=user 
            )
            business.save()

            # Create Image objects and associate them with the Company
            for image_url in image_urls:
                Image.objects.create(company=business, image_url=image_url)

            return JsonResponse({'message': 'Company and images created successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing key in request body: {e}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    



def getBusinesses(request, country):
    """
    Retrieves companies with optional skip and limit parameters, sorted by name.
    """
    print('get')
    if request.method == 'GET':
        try:
            businesses = Business.objects.filter(country=country).order_by('name')  # Sort by name
            print('get all companies', businesses)
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
            # return
            company_list = []


            for business in businesses:
                company_data = {
                    'id': business.id,
                    'companyInfo': {
                        'name': business.name,
                        'address_line1': business.address_line1,
                        'address_line2': business.address_line2,
                        'city': business.city,
                        "region":business.region,
                        'postal_code': business.postal_code,
                        'contact': business.contact,
                        'country': business.country,
                        'hours': business.hours,
                        "website": business.website,
                        'company_type': business.company_type,
                        'photos': business.photos,
                        'description': business.description,
                    },
                    'hoursData': business.hoursData,
                    # 'images': [{'id': image.id, 'image_url': image.image_url} for image in company.images.all()]  
                      }
                company_list.append(company_data)

            return JsonResponse(company_list, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

