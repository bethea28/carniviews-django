from django.contrib.contenttypes.models import ContentType
from .models import EditSuggestion
from company_app.models import Company
from business_app.models import Business
from user_app.models import CustomUser
from django.http import JsonResponse
from django.shortcuts import get_object_or_404 #import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json



# from django.contrib.contenttypes.models import ContentType
# from .models import EditSuggestion, Company, Business  # Import your models
# from django.http import JsonResponse
# from django.views.decorators.http import require_POST
# import json
# from users.models import CustomUser #Import CustomUser

@csrf_exempt
@require_POST  # Only allow POST requests to this view
def addEditSuggestion(request):
    """
    View to handle the submission of user edit suggestions.
    """
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body)

        # Get the required data from the request
        suggestion_type = data.get('type')
        object_id = data.get('entity_id')
        user_id = data.get('user_id')
        suggestion_text = data.get('suggestion_text')

        # Validate that required data is present
        if not suggestion_type or not object_id or not suggestion_text or not user_id:
            return JsonResponse({'error': 'Type, ID, user_id, and suggestion_text are required.'}, status=400)

        # Determine the ContentType based on the suggestion type
        user = get_object_or_404(CustomUser, id=user_id)  # Get user object.

        if suggestion_type == 'BAND':
            content_type = ContentType.objects.get_for_model(Company)
            content_type_label = 'BAND'
            # no need to get the Company instance, just check that it exists.
            get_object_or_404(Company, id=object_id)
        elif suggestion_type == 'BUSINESS':
            content_type = ContentType.objects.get_for_model(Business)
            content_type_label = 'BUSINESS'
            get_object_or_404(Business, id=object_id)
        else:
            return JsonResponse({'error': 'Invalid suggestion type.  Must be "BAND" or "BUSINESS".'}, status=400)

        # Create the EditSuggestion instance
        edit_suggestion = EditSuggestion(
            content_type=content_type,
            content_type_label=content_type_label, #set content type label
            object_id=object_id,
            user=user,  # The user making the suggestion. Crucial.
            suggestion_text=suggestion_text,
        )
        edit_suggestion.save()

        return JsonResponse({'message': 'Edit suggestion submitted successfully.'}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data in request body.'}, status=400)
    except Exception as e:
        # Log the error for debugging purposes
        import logging
        logging.exception("Error creating edit suggestion")
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)