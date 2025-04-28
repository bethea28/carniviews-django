from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Event, EventImage  # Import both Event and EventImage
from user_app.models import CustomUser
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


# @csrf_exempt
# def addEvent(request, user_id):
#     """
#     Creates an Event object and associated Image objects from a JSON request body.
#     """
#     logger.debug('this is my add event request.body: %s', request.body)
#     if request.method == 'POST':
#         try:
#             request_data = json.loads(request.body)
#             event_info = request_data.get('eventInfo', {})
#             image_data_list = request_data.get('allImages', [])  # Changed variable name
#             event_hours = request_data.get('eventHours', {})
#             logger.debug('this is my add event request_data: %s', request_data)

#             # Get the user object based on user_id from the URL
#             user = get_object_or_404(CustomUser, id=user_id)

#             # Parse time strings into datetime.time objects
#             def parse_time(time_str):
#                 if not time_str:
#                     return None
#                 try:
#                     return datetime.strptime(time_str, "%I:%M %p").time()
#                 except ValueError:
#                     try:
#                         return datetime.strptime(time_str, "%H:%M:%S").time()
#                     except ValueError:
#                         logger.error(f"Invalid time format: {time_str}")
#                         raise ValueError(
#                             f"Invalid time format: {time_str}.  Use HH:MM:SS or H:MM AM/PM"
#                         )

#             start_time_obj = parse_time(event_hours.get('start'))
#             end_time_obj = parse_time(event_hours.get('end'))

#             # Create Event object
#             event = Event(
#                 user=user,
#                 name=event_info.get('name', ''),
#                 address=event_info.get('address', ''),
#                 city=event_info.get('city', ''),
#                 state=event_info.get('state', ''),
#                 zip_code=event_info.get('zip', ''),
#                 hours=event_hours,  # Store the event_hours dictionary
#                 start_time=start_time_obj,  # Store as TimeField
#                 end_time=end_time_obj,  # Store as TimeField
#                 type=event_info.get('type', ''),
#                 description=event_info.get('description', ''),
#             )
#             event.save()

#             # Create EventImage objects and associate them with the Event
#             for image_data in image_data_list:  # Iterate through the list of image data
#                 image_uri = image_data.get('uri')  # Extract the URI
#                 if image_uri:  # Only create EventImage if URI is present
#                     event_image = EventImage(
#                         event=event,
#                         image={'uri': image_uri},  # Store the URI in the JSONField
#                     )
#                     event_image.save()
#                 else:
#                     logger.warning(
#                         f"Image URI is missing for an image in event {event.id}")  # Log warning

#             return JsonResponse({'message': 'Event and images created successfully'},
#                                 status=201)
#         except json.JSONDecodeError as e:
#             logger.error('JSONDecodeError: %s', e)
#             return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
#         except ValueError as e:
#             return JsonResponse({'error': str(e)}, status=400)
#         except KeyError as e:
#             logger.error('KeyError: %s', e)
#             return JsonResponse({'error': f'Missing key in request body: {e}'},
#                                 status=400)
#         except Exception as e:
#             logger.error('Exception: %s', e, exc_info=True)
#             return JsonResponse({'error': str(e)}, status=500)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)





@csrf_exempt
def addEvent(request, user_id):
    """
    Creates an Event object and associated Image objects from a JSON request body.
    """
    logger.debug('this is my add event request.body: %s', request.body)
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
            event_info = request_data.get('eventInfo', {})
            image_data_list = request_data.get('allImages', [])  # Changed variable name
            event_hours = request_data.get('eventHours', {})
            logger.debug('this is my add event request_data: %s', request_data)

            # Get the user object based on user_id from the URL
            user = get_object_or_404(CustomUser, id=user_id)
            print('event info now requestData', request_data)
            # Parse time strings into datetime.time objects
            def parse_time(time_str):
                if not time_str:
                    return None
                try:
                    return datetime.strptime(time_str, "%I:%M %p").time()
                except ValueError:
                    try:
                        return datetime.strptime(time_str, "%H:%M:%S").time()
                    except ValueError:
                        logger.error(f"Invalid time format: {time_str}")
                        raise ValueError(
                            f"Invalid time format: {time_str}.  Use HH:MM:SS or H:MM AM/PM"
                        )

            start_time_obj = event_hours.get('start')
            end_time_obj = event_hours.get('end')
            print('test hour n start adding' , event_hours.get('start'))
            # print('test hour n start ow  the full obj', start_time_obj)
            # Create Event object
            # return
            event = Event(
                user=user,
                name=event_info.get('name', ''),
                address_line1=event_info.get('addressLine1', ''),
                address_line2=event_info.get('addressLine2', ''),
                city=event_info.get('city', ''),
                region=event_info.get('region', ''),
                postal_code=event_info.get('postal', ''),
                country=event_info.get('country', ''),
                price=event_info.get('price', ''),
                ticket=event_info.get('ticket', ''),
                start_time=start_time_obj,  # Store as TimeField
                end_time=end_time_obj,  # Store as TimeField
                type=event_info.get('type', ''),
                description=event_info.get('description', ''),
            )
            event.save()

            # Create EventImage objects and associate them with the Event
            for image_data in image_data_list:  # Iterate through the list of image data
                image_uri = image_data.get('uri')  # Extract the URI
                if image_uri:  # Only create EventImage if URI is present
                    event_image = EventImage(
                        event=event,
                        image={'uri': image_uri},  # Store the URI in the JSONField
                    )
                    event_image.save()
                else:
                    logger.warning(
                        f"Image URI is missing for an image in event {event.id}")  # Log warning

            return JsonResponse({'message': 'Event and images created successfully'},
                                status=201)
        except json.JSONDecodeError as e:
            logger.error('JSONDecodeError: %s', e)
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except KeyError as e:
            logger.error('KeyError: %s', e)
            return JsonResponse({'error': f'Missing key in request body: {e}'},
                                status=400)
        except Exception as e:
            logger.error('Exception: %s', e, exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def getAllEvents(request, country):
    """
    Retrieves all events and returns them as JSON.
    Matches the structure used in addEvent view (with extended address fields).
    """
    logger.debug('Entering getAllEvents view')

    if request.method == 'GET':
        try:
            events = Event.objects.filter(country=country).order_by('name')
            events_data = []
            for event in events:
                # Get all associated images
                images = EventImage.objects.filter(event=event)
                image_uris = []
                for image in images:
                    if isinstance(image.image, dict) and 'uri' in image.image:
                        image_uris.append({'uri': image.image['uri']})
                    else:
                        logger.warning(f"Invalid image data for EventImage {image.id}")
                        image_uris.append({'uri': None})

                # Get user info
                user = event.user
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }

                event_data = {
                    'id': event.id,
                    'name': event.name,
                    'addressLine1': event.address_line1,
                    'addressLine2': event.address_line2,
                    'city': event.city,
                    'region': event.region,
                    'postal': event.postal_code,
                    'country': event.country,
                    'price': event.price,
                    'ticket': event.ticket,
                    'start_time': str(event.start_time),
                    'end_time': str(event.end_time),
                    'type': event.type,
                    'description': event.description,
                    'images': image_uris,
                    'user': user_data,
                }

                events_data.append(event_data)
            return JsonResponse({'events': events_data}, status=200, safe=False)

        except Exception as e:
            logger.error(f'Error in getAllEvents: {e}', exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)

    logger.warning('Invalid method for getAllEvents')
    return JsonResponse({'error': 'Method not allowed'}, status=405)
