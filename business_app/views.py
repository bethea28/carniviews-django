
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
from .models import UnverifiedBusiness
from images_app.models import Image
from django.shortcuts import get_object_or_404
from user_app.models import CustomUser
from django.db.models import F

   
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
            user = get_object_or_404(CustomUser, id=user_id)
            print('BUSINESS ADDING NOW', company_info)

            # Create Company object, populating individual fields
            business = Business(
                name=name,
                address_line1=company_info.get('addressLine1', ''),
                address_line2=company_info.get('addressLine2', ''),
                city=company_info.get('city', ''),
                region=company_info.get('region', ''),
                postal_code=company_info.get('postal', ''),
                hours=company_info.get('hours', ''),
                # contact=company_info.get('contact', ''),
                country=company_info.get('country', ''),
                company_type=company_info.get('type', ''),
                website=company_info.get('website', ''),
                photos=company_info.get('photos', {}),
                description=company_info.get('description', ''),
                user=user,

                # New fields
                phone=company_info.get('phone', ''),
                email=company_info.get('email', ''),
                facebook=company_info.get('facebook', ''),
                instagram=company_info.get('instagram', ''),
                twitter=company_info.get('twitter', ''),
                hoursData=hours_data
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

@csrf_exempt
def addUnverifiedBusiness(request, user_id):
    """
    Creates an UnverifiedBusiness object and associated Image objects from a JSON request body.
    """
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
            company_info = request_data.get('companyInfo', {})
            image_urls = request_data.get('imageUrls', [])
            hours_data = request_data.get('hoursData', {})

            # Get the user object based on user_id
            user = get_object_or_404(CustomUser, id=user_id)
            print('HERE IS MY UNVERIFIED COMP', image_urls)

            # Create UnverifiedBusiness object
            business = UnverifiedBusiness(
                name=company_info.get('name', ''),
                address_line1=company_info.get('addressLine1', ''),
                address_line2=company_info.get('addressLine2', ''),
                city=company_info.get('city', ''),
                region=company_info.get('region', ''),
                postal_code=company_info.get('postal', ''),
                country=company_info.get('country', ''),
                hours=company_info.get('hours', ''),
                company_type=company_info.get('type', ''),
                photos=image_urls,  # Initialize with empty dict or replace if provided
                # contact=company_info.get('contact', ''),  # fallback if 'contact' is used
                website=company_info.get('website', ''),
                hoursData=hours_data,
                description=company_info.get('description', ''),
                user=user,

                # New fields
                phone=company_info.get('phone', ''),
                email=company_info.get('email', ''),
                facebook=company_info.get('facebook', ''),
                instagram=company_info.get('instagram', ''),
                twitter=company_info.get('twitter', ''),
            )

            business.save()

            # Create Image objects and associate them with the Business
            for image_url in image_urls:
                Image.objects.create(
                    business=business,
                    user=user,
                    image_url=image_url
                )

            return JsonResponse({'message': 'Business and images created successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing key in request body: {e}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def editVerifiedBusiness(request, biz_id):
    """
    Creates an UnverifiedBusiness object and associated Image objects from a JSON request body.
    """
    if request.method == 'PUT':

        try:
            request_data = json.loads(request.body)
            company_info = request_data.get('companyInfo', {})
            image_urls = request_data.get('imageUrls', [])
            hours_data = request_data.get('hoursData', {})
            print('request body edit', request_data)
            # Get the user object based on user_id
            business = get_object_or_404(Business, id=biz_id)
            print('COMPANY INFO LUCCI', company_info)
            # return 
# Update only provided fields in eventInfo
                    # Update only provided fields from company_info
            if 'name' in company_info:
                business.name = company_info['name']
            if 'addressLine1' in company_info:
                business.address_line1 = company_info['addressLine1']
            if 'addressLine2' in company_info:
                business.address_line2 = company_info['addressLine2']
            if 'city' in company_info:
                business.city = company_info['city']
            if 'region' in company_info:
                business.region = company_info['region']
            if 'postal' in company_info:
                business.postal_code = company_info['postal']
            if 'country' in company_info:
                business.country = company_info['country']
            if 'hours' in company_info:
                business.hours = company_info['hours']
            if 'company_type' in company_info:
                business.company_type = company_info['company_type']
            if 'photos' in company_info:
                business.photos = company_info['photos']
            if 'website' in company_info:
                business.website = company_info['website']
            if 'description' in company_info:
                business.description = company_info['description']
            if 'phone' in company_info:
                business.phone = company_info['phone']
            if 'email' in company_info:
                business.email = company_info['email']
            if 'facebook' in company_info:
                business.facebook = company_info['facebook']
            if 'instagram' in company_info:
                business.instagram = company_info['instagram']
            if 'twitter' in company_info:
                business.twitter = company_info['twitter']

            # Also update these if present
            if hours_data:
                business.hoursData = hours_data
            # if user:
            #     business.user = user

            # Save the updated business object
            business.save()

            # Create UnverifiedBusiness object
            # business = Business(
            #     name=company_info.get('name', ''),
            #     address_line1=company_info.get('addressLine1', ''),
            #     address_line2=company_info.get('addressLine2', ''),
            #     city=company_info.get('city', ''),
            #     region=company_info.get('region', ''),
            #     postal_code=company_info.get('postal', ''),
            #     country=company_info.get('country', ''),
            #     hours=company_info.get('hours', ''),
            #     company_type=company_info.get('type', ''),
            #     photos={},  # Initialize with empty dict or replace if provided
            #     # contact=company_info.get('contact', ''),  # fallback if 'contact' is used
            #     website=company_info.get('website', ''),
            #     hoursData=hours_data,
            #     description=company_info.get('description', ''),
            #     user=user,

            #     # New fields
            #     phone=company_info.get('phone', ''),
            #     email=company_info.get('email', ''),
            #     facebook=company_info.get('facebook', ''),
            #     instagram=company_info.get('instagram', ''),
            #     twitter=company_info.get('twitter', ''),
            # )

            # business.save()

            # Create Image objects and associate them with the Business
            for image_url in image_urls:
                Image.objects.create(
                    business=business,
                    user=user,
                    image_url=image_url
                )

            return JsonResponse({'message': 'Business and images created successfully'}, status=201)

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

            start = int(skip_str) if skip_str and skip_str.isdigit() else 0
            end = start + int(limit_str) if limit_str and limit_str.isdigit() else None

            # Apply slicing
            businesses = businesses[start:end] if end else businesses[start:]

            company_list = []

            for business in businesses:
                company_data = {
                    'id': business.id,
                    'companyInfo': {
                        'name': business.name,
                        'address_line1': business.address_line1,
                        'address_line2': business.address_line2,
                        'city': business.city,
                        'region': business.region,
                        'postal_code': business.postal_code,
                        # 'contact': business.contact,
                        'country': business.country,
                        'hours': business.hours,
                        'website': business.website,
                        'company_type': business.company_type,
                        'photos': business.photos,
                        'description': business.description,
                        'phone': business.phone,
                        'email': business.email,
                        'facebook': business.facebook,
                        'instagram': business.instagram,
                        'twitter': business.twitter,
                    },
                    'hoursData': business.hoursData,
                }
                company_list.append(company_data)

            return JsonResponse(company_list, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
