# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from .models import Company
# from images_app.models import Image
# from django.contrib.auth.decorators import login_required  # Import login_required
from django.db.models import Avg

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# from models import Company
from images_app.models import Image
from review_app.models import Review
# from django.contrib.auth.models import User  # Import User model
from django.shortcuts import get_object_or_404 #import get_object_or_404
# from user_app.models import Image
from user_app.models import CustomUser
from django.db.models import F
# from models import Recommendation

import json
from .models import UnverifiedCompany, Company, Recommendation
from user_app.models import CustomUser

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
                normalized_country=company_info.get('country', '').lower().replace(' ', ''),               
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
            print('all users bryan',request_data )
            # Create Company object, populating individual fields
            company = Company(
                name=company_info.get('name', ''),
                address=company_info.get('address', ''),
                city=company_info.get('city', ''),
                state=company_info.get('state', ''),
                zip_code=company_info.get('zip', ''),
                hours=company_info.get('hours', ''),
                country=company_info.get('country', ''),
                normalized_country=company_info.get('country', '').lower().replace(' ', ''),                contact=company_info.get('contact', ''),
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




def getCompanies(request, country):
    """
    Retrieves companies with optional skip and limit parameters, sorted by name.
    """
    # return 
    if request.method == 'GET':
        try:
            norm_country = country.lower().replace(" ", ""), 
            companies = Company.objects.filter(country=country).order_by('name')  # Filter by 'USA' and then sort by name            print('get all companies', companies)
            # companies = Company.objects.filter(normalized_country=norm_country).order_by('name')  # Filter by 'USA' and then sort by name            print('get all companies', companies)
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
            # print('GET COMPANIES SOCIALS', company)
            for company in companies:
                overall_avg = company.reviews.aggregate(avg=Avg('overall'))['avg']
                overall_avg = round(overall_avg, 2) if overall_avg else 0.0
                company_data = {
                    'id': company.id,
                    'companyInfo': {
                        'socials': company.socials,
                        'name': company.name,
                        'address_line1': company.address_line1,
                        'address_line2': company.address_line2,
                        'city': company.city,
                        "region":company.region,
                        'postal_code': company.postal_code,
                        'contact': company.contact,
                        'country': company.country,
                        'claps': company.claps,
                        'hours': company.hours,
                        "website": company.website,
                        'company_type': company.company_type,
                        'photos': company.photos,
                        'description': company.description,
                        'overall_avg': overall_avg,
                        'bandStories': company.bandStories,
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
def addRec(request):
    if request.method == 'POST':
        request_data = json.loads(request.body)
        companyId = request_data.get('company_id','')
        userId = request_data.get('user_id','')
        rec = request_data.get('rec','')
        
        user = get_object_or_404(CustomUser, id=userId)
        company = get_object_or_404(Company, id=companyId)

        # Check if a recommendation already exists for this user and company
        existing_recommendation = Recommendation.objects.filter(user=user, company=company).first()

        if existing_recommendation:
            # Update the existing recommendation
            existing_recommendation.rec = rec
            existing_recommendation.save()
            return JsonResponse({'message': 'Recommendation successfully updated.'}, status=200)  # Use 200 for update
        else:
            # Create a new recommendation
            recommendation = Recommendation(rec=rec, user=user, company=company)
            recommendation.save()
            return JsonResponse({'message': 'Recommendation successfully created.'}, status=201) # 201 for create
    return JsonResponse({'message': 'Recommendation Failed'}, status=500)



@csrf_exempt
def getCompanyRecs(request, company_id):
    if request.method == 'GET':
        companyId = company_id
        company = Company.objects.get(id=companyId)
        recs = Recommendation.objects.filter(company=company).values(
            'rec',
            'user_id'
        )

        allRecs=list(recs)
        print('show me dictorary list DAREN', allRecs)
        return JsonResponse({'message': 'Recommondation successfully retrieved', "allRecs": allRecs}, status=201)
    return JsonResponse({'message': 'Recommondation Failed'}, status=500)

    None