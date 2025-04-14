from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Event, EventImage  # Import both Event and EventImage
from user_app.models import CustomUser
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


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

            start_time_obj = parse_time(event_hours.get('start'))
            end_time_obj = parse_time(event_hours.get('end'))

            # Create Event object
            event = Event(
                user=user,
                name=event_info.get('name', ''),
                address=event_info.get('address', ''),
                city=event_info.get('city', ''),
                state=event_info.get('state', ''),
                zip_code=event_info.get('zip', ''),
                hours=event_hours,  # Store the event_hours dictionary
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

            start_time_obj = parse_time(event_hours.get('start'))
            end_time_obj = parse_time(event_hours.get('end'))

            # Create Event object
            event = Event(
                user=user,
                name=event_info.get('name', ''),
                address=event_info.get('address', ''),
                city=event_info.get('city', ''),
                state=event_info.get('state', ''),
                zip_code=event_info.get('zip', ''),
                hours=event_hours,  # Store the event_hours dictionary
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


@csrf_exempt  # Added csrf_exempt decorator
def getAllEvents(request):
    """
    Retrieves all events from the database and returns them as a JSON response.
    Includes associated images and user information.
    """
    logger.debug('Entering getAllEvents view')
    if request.method == 'GET':
        try:
            events = Event.objects.all()  # Get all Event objects

            # Prepare the data structure
            events_data = []
            for event in events:
                # Get the images for the current event
                images = EventImage.objects.filter(event=event)
                image_uris = []
                for image in images:
                    #  Check if image.image is a dictionary and contains 'uri'
                    print('KENYA MARTING Da,insideWN',type(image.image))
                    if isinstance(image.image, dict) and 'uri' in image.image:
                        image_uris.append(
                            {'uri': image.image.get('uri')}
                        )  # Extract the URI from the dictionary
                    else:
                        logger.warning(
                            f"Image data for EventImage {image.id} is not a dictionary with 'uri' key. Skipping."
                        )
                        image_uris.append(
                            {'uri': None}
                        )  # Append None URI to maintain consistency

                # Get the user for the current event
                user = event.user
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    # Add other user fields as needed
                }
                print('ALL FOOTBALL TEAM',image_uris)
                event_data = {
                    'id': event.id,
                    'name': event.name,
                    'address': event.address,
                    'city': event.city,
                    'state': event.state,
                    'zip_code': event.zip_code,
                    'hours': event.hours,
                    'start_time': str(
                        event.start_time),  # Convert TimeField to string
                    'end_time': str(
                        event.end_time),  # Convert TimeField to string
                    'type': event.type,
                    'description': event.description,
                    'images': image_uris,  # Include the list of image URIs
                    'user': user_data,  # Include user data
                }
                events_data.append(event_data)

            return JsonResponse({'events': events_data}, safe=False, status=200)

        except Exception as e:
            logger.error(f'Error in getAllEvents: {e}', exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)
    else:
        logger.warning('Invalid method for getAllEvents')
        return JsonResponse({'error': 'Method not allowed'}, status=405)
