import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import BandStory, Company,CustomUser  # Import your BandStory and Company models

@csrf_exempt
def addBandStory(request):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body.decode('utf-8'))
            print('here in band', request_data)

            user_id = request_data.get('user_id')
            company_id = request_data.get('company_id')
            name = request_data.get('title', '') # Assuming 'title' in request maps to 'name' in model
            intro = request_data.get('intro', '')
            vibe = request_data.get('vibe', '')
            costume = request_data.get('costume', '')
            moments = request_data.get('moments', '')
            reflection = request_data.get('reflection', '')
            photos = request_data.get('photos', {}) # Assuming you might send photos as JSON

            # Basic validation
            if company_id is None or not name:
                return JsonResponse({'error': 'Company ID and Name are required.'}, status=400)

            try:
                company = Company.objects.get(pk=company_id)
            except Company.DoesNotExist:
                return JsonResponse({'error': f'Company with ID {company_id} does not exist.'}, status=400)

            try:
                user = CustomUser.objects.get(pk=user_id)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': f'User with ID {user_id} does not exist.'}, status=400)

            band_story = BandStory(
                user=user,  # Use the logged-in user object
                company=company,
                name=name,
                intro=intro,
                vibe=vibe,
                costume=costume,
                moments=moments,
                reflection=reflection,
                photos=photos
            )
            band_story.save()
            return JsonResponse({'message': 'Band story created successfully!'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data in request body.'}, status=400)
        except Exception as e:
            print('Error creating band story:', e)
            return JsonResponse({'error': 'Failed to create band story.'}, status=500)
    else:
        return render(request, 'your_template_name.html') # Replace with your actual template




@csrf_exempt
def getBandStories(request, company_id):
    if request.method == 'GET':
        company = Company.objects.get(pk=company_id)
        band_stories = BandStory.objects.filter(company=company).order_by('-id')
        print('GETTING STGORIE BAND',band_stories)
        data = [{
            'id': story.id,
            'user_id': story.user.id,
            'company_id': story.company.id,
            'title': story.name,  # Match the 'title' key from the request
            'intro': story.intro,
            'vibe': story.vibe,
            'costume': story.costume,
            'moments': story.moments,
            'reflection': story.reflection,
            'photos': story.photos,
            # Add any other fields you need
        } for story in band_stories]
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed for this endpoint.'}, status=405)