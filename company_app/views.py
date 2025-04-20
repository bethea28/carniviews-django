# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from .models import Company
# from images_app.models import Image
# from django.contrib.auth.decorators import login_required  # Import login_required

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
from .models import UnverifiedCompany, Company, Recommendation
from images_app.models import Image
from django.shortcuts import get_object_or_404
from user_app.models import CustomUser
from django.db.models import F

@csrf_exempt
def addUnverifiedCompany(request, user_id):
    """
    Creates an UnverifiedCompany object and associated Image objects from a JSON request body.
    """
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
            company_info = request_data.get('companyInfo', {})
            image_urls = request_data.get('imageUrls', [])
            hours_data = request_data.get('hoursData', {})

            # Get the user object based on user_id
            user = get_object_or_404(CustomUser, id=user_id)
            print('HERE IS MY UNVERIFIED COMP', request_data)

        
            # # Create UnverifiedCompany object
            # unverified_company = UnverifiedCompany(
            #     name=company_info.get('name', ''),
            #     address=company_info.get('address', ''),
            #     city=company_info.get('city', ''),
            #     state=company_info.get('state', ''),
            #     zip_code=company_info.get('zip', ''),
            #     hours=company_info.get('hours', ''),
            #     company_type=company_info.get('type', ''),
            #     photos=image_urls,
            #     hoursData=hours_data,
            #     description=company_info.get('description', ''),
            #     user=user  # Associate with the user from URL
            # )

             
            # Create UnverifiedCompany object
            unverified_company = UnverifiedCompany(
                name=company_info.get('name', ''),
                address_line1=company_info.get('addressLine1', ''),
                address_line2=company_info.get('addressLine2', ''),
                city=company_info.get('city', ''),
                region=company_info.get('region', ''),
                postal_code=company_info.get('postal', ''),
                contact=company_info.get('contact', ''),
                website=company_info.get('website', ''),
                country=company_info.get('country', ''),
                hours=company_info.get('hours', ''),
                company_type=company_info.get('type', ''),
                photos=image_urls,
                hoursData=hours_data,
                description=company_info.get('description', ''),
                user=user  # Associate with the user from URL
            )

            unverified_company.save()
            # Create Image objects and associate them with the UnverifiedCompany
            # Create Image objects and associate them with the UnverifiedCompany
            for image_url in image_urls:
                Image.objects.create(
                    unverified_company=unverified_company,
                    user=user,  # Assign the user here
                    image_url=image_url
                )
            return JsonResponse({'message': 'Unverified company and images submitted successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing key in request body: {e}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

@csrf_exempt
def addVerifiedCompany(request, user_id):  # Accept user_id from URL
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
            print('all users bryan',request_data )
            # Create Company object, populating individual fields
            company = Company(
                name=company_info.get('name', ''),
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
    Retrieves companies with optional skip and limit parameters, sorted by name.
    """
    if request.method == 'GET':
        try:
            companies = Company.objects.all().order_by('name')  # Sort by name
            print('get all companies', companies)
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
            print('getting all companies now', companies)
            # return
            company_list = []


            # unverified_company = UnverifiedCompany(
            #     name=company_info.get('name', ''),
            #     address_line1=company_info.get('addressLine1', ''),
            #     address_line2=company_info.get('addressLine2', ''),
            #     city=company_info.get('city', ''),
            #     region=company_info.get('region', ''),
            #     postal_code=company_info.get('postal', ''),
            #     country=company_info.get('country', ''),
            #     hours=company_info.get('hours', ''),
            #     company_type=company_info.get('type', ''),
            #     photos=image_urls,
            #     hoursData=hours_data,
            #     description=company_info.get('description', ''),
            #     user=user  # Associate with the user from URL
            # )
            for company in companies:
                company_data = {
                    'id': company.id,
                    'companyInfo': {
                        'name': company.name,
                        'address_line1': company.address_line1,
                        'address_line2': company.address_line2,
                        'city': company.city,
                        "region":company.region,
                        'postal_code': company.postal_code,
                        'contact': company.contact,
                        'country': company.country,
                        'hours': company.hours,
                        "website": company.website,
                        'company_type': company.company_type,
                        'photos': company.photos,
                        'description': company.description,
                    },
                    'hoursData': company.hoursData,
                    # 'images': [{'id': image.id, 'image_url': image.image_url} for image in company.images.all()]  
                      }
                company_list.append(company_data)

            return JsonResponse(company_list, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    



@csrf_exempt
def addRec(request, user_id, company_id):
    if request.method == 'POST':
        request_data = json.loads(request.body)
        companyId = request_data.get('companyId','')
        userId = request_data.get('userId','')
        rec = request_data.get('rec','')

        user = get_object_or_404(CustomUser, id=userId) #get user object by user id.
        company = get_object_or_404(Company, id=companyId) #get user object by user id.

        rec = Recommendation(
          rec=rec,
          user=user,  
          company=company
        )
        rec.save()
        return JsonResponse({'message': 'Recommondation successfully'}, status=201)
    return JsonResponse({'message': 'Recommondation Failed'}, status=500)

    None


@csrf_exempt
def getCompanyRecs(request, company_id):
    if request.method == 'GET':

        company = Company.objects.get(id=company_id)
        recs = Recommendation.objects.filter(company=company).values(
            'rec',
            'user_id'
        )

        allRecs=list(recs)
        print('show me dictorary list', allRecs)
        return JsonResponse({'message': 'Recommondation successfully retrieved', "allRecs": allRecs}, status=201)
    return JsonResponse({'message': 'Recommondation Failed'}, status=500)

    None