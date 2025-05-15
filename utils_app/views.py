from django.db.models import F
from django.http import JsonResponse
from django.db import connection
from company_app.models import Company
from event_app.models import Event
from band_story_app.models import BandStory
from django.shortcuts import get_object_or_404 #import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def duplicationCheck(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', '')
            country = data.get('country', '')
            type = data.get('type', '')  # Get the 'type' from the request

            print('DUPS CHECK', data)
            if not name or not country or not type:
                return JsonResponse({'error': 'Please provide name, country, and type.'}, status=400)

            sql = ""
            table_name = ""
            if type.lower() == 'business':
                table_name = 'business_app_unverifiedbusiness'  # Replace with your actual business table name
                sql = f"""
                    SELECT id, name, country,
                           similarity(name, %s) AS name_similarity
                    FROM {table_name}
                    WHERE similarity(name, %s) > 0.4 AND country = %s
                    ORDER BY name_similarity DESC
                    LIMIT 10;
                """
                cursor_params = [name, name, country]
            elif type.lower() == 'event':
                table_name = 'event_app_event'  # Replace with your actual event table name
                sql = f"""
                    SELECT id, name, country,  -- Adjust column names as needed
                           similarity(name, %s) AS name_similarity
                    FROM {table_name}
                    WHERE similarity(name, %s) > 0.4 AND country = %s
                    ORDER BY name_similarity DESC
                    LIMIT 10;
                """
                cursor_params = [name, name, country] # Assuming 'name' maps to event title and 'country' to location
            else:
                return JsonResponse({'error': f'Unsupported type: {type}'}, status=400)

            with connection.cursor() as cursor:
                cursor.execute(sql, cursor_params)
                columns = [col[0] for col in cursor.description]
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]

            return JsonResponse({'results': results})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def addClaps(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            entity_id = data.get('entity_id')
            entity_type = data.get('type')

            if not entity_id or not entity_type:
                return JsonResponse({'error': 'Missing entity_id or type in request body'}, status=400)

            if entity_type == 'company':
                try:
                    company = get_object_or_404(Company, id=entity_id)
                    company.claps = F('claps') + 1
                    company.save()
                    print('this my CLAPPING', entity_type, entity_id)
                    return JsonResponse({'message': 'Clap added successfully to Band'})
                except Company.DoesNotExist:
                    return JsonResponse({'error': f'Band with id {entity_id} not found'}, status=404)
            elif entity_type == 'story':
                try:
                    bandStory = get_object_or_404(BandStory, id=entity_id)
                    print('show me BAND STORY',bandStory, entity_type, entity_id)
                    # return
                    bandStory.claps = F('claps') + 1
                    bandStory.save()
                    print('this my CLAPPING', entity_type, entity_id)
                    return JsonResponse({'message': 'Clap added successfully to Story'})
                except Company.DoesNotExist:
                    return JsonResponse({'error': f'Company with id {entity_id} not found'}, status=404)
            else:
                return JsonResponse({'error': f'Unsupported entity type: {entity_type}'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)