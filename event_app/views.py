from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Event, EventImage  # Import both Event and EventImage
from user_app.models import CustomUser
import logging
from datetime import datetime
from dateutil import parser as dateutil_parser

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
            print('event info now requestData image_data_list', image_data_list)
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

            date_obj = event_hours.get('date')
            start_time_obj = event_hours.get('start')
            end_time_obj = event_hours.get('end')
            print('test hour n start adding' , )
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
                photos=image_data_list,
                ticket=event_info.get('ticket', ''),
                date=date_obj,  # Store as TimeField
                start_time=start_time_obj,  # Store as TimeField
                end_time=end_time_obj,  # Store as TimeField
                type=event_info.get('type', ''),
                description=event_info.get('description', ''),
            )
            event.save()

            # Create EventImage objects and associate them with the Event
            # for image_data in image_data_list:  # Iterate through the list of image data
            #     image_uri = image_data.get('uri')  # Extract the URI
            #     if image_uri:  # Only create EventImage if URI is present
            #         event_image = EventImage(
            #             event=event,
            #             image={'uri': image_uri},  # Store the URI in the JSONField
            #         )
            #         event_image.save()
            #     else:
            #         logger.warning(
            #             f"Image URI is missing for an image in event {event.id}")  # Log warning

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
def editEvent(request, event_id=None):
    """
    Updates an Event and its associated EventImages.
    Only updates fields provided in the request.
    """
    logger.debug('Received event request body: %s', request.body)

    if request.method != 'PUT':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        request_data = json.loads(request.body)
        event_info = request_data.get('eventInfo', {})
        image_data_list = request_data.get('allImages', [])
        event_hours = request_data.get('eventHours', {})


        def parse_time(time_str):
            if not time_str:
                return None
            try:
                # Handles "HH:MM AM/PM" and "HH:MM:SS"
                return datetime.strptime(time_str, "%I:%M %p").time()
            except ValueError:
                try:
                    return datetime.strptime(time_str, "%H:%M:%S").time()
                except ValueError:
                    try:
                        # Handles ISO 8601 (e.g., "2025-04-30T05:42:00.000Z")
                        return dateutil_parser.parse(time_str).time()
                    except Exception:
                        logger.error(f"Invalid time format: {time_str}")
                        raise ValueError(
                            f"Invalid time format: {time_str}. Use HH:MM AM/PM, HH:MM:SS, or ISO format"
                        )

        if not event_id:
            return JsonResponse({'error': 'Missing event ID'}, status=400)

        event = get_object_or_404(Event, id=event_id)
        logger.info(f"Updating existing event with ID {event_id}")

        # Update only provided fields in eventInfo
        if 'name' in event_info:
            event.name = event_info['name']
        if 'addressLine1' in event_info:
            event.address_line1 = event_info['addressLine1']
        if 'addressLine2' in event_info:
            event.address_line2 = event_info['addressLine2']
        if 'city' in event_info:
            event.city = event_info['city']
        if 'region' in event_info:
            event.region = event_info['region']
        if 'postal' in event_info:
            event.postal_code = event_info['postal']
        if 'country' in event_info:
            event.country = event_info['country']
        if 'price' in event_info:
            event.price = event_info['price']
        if 'ticket' in event_info:
            event.ticket = event_info['ticket']
        if 'type' in event_info:
            event.type = event_info['type']
        if 'description' in event_info:
            event.description = event_info['description']

        # Update only provided time/date fields
        if 'date' in event_hours:
            event.date = event_hours['date']
        if 'start' in event_hours:
            event.start_time = parse_time(event_hours['start'])
        if 'end' in event_hours:
            event.end_time = parse_time(event_hours['end'])

        event.save()

        # Replace images only if new ones are provided
        if image_data_list:
            EventImage.objects.filter(event=event).delete()
            for image_data in image_data_list:
                image_uri = image_data.get('uri')
                if image_uri:
                    EventImage.objects.create(
                        event=event,
                        image={'uri': image_uri},
                    )

        return JsonResponse({
            'message': 'Event updated successfully',
            'eventId': event.id
        }, status=200)

    except json.JSONDecodeError as e:
        logger.error('JSONDecodeError: %s', e)
        return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        logger.error('Exception: %s', e, exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)
from django.utils import timezone
from datetime import timedelta

@csrf_exempt
def getAllEvents(request, country):
    """
    Retrieves all events and returns them as JSON.
    Also deletes events older than 1 day before the current date.
    """
    logger.debug('Entering getAllEvents view')

    if request.method == 'GET':
        try:
            # Delete events more than 1 day old
            cutoff_date = timezone.now().date() - timedelta(days=1)
            old_events = Event.objects.filter(date__lt=cutoff_date)
            deleted_count, _ = old_events.delete()
            logger.info(f'Deleted {deleted_count} old events')

            # Fetch current events by country
            events = Event.objects.filter(country=country).order_by('name')
            events_data = []
            for event in events:
                images = EventImage.objects.filter(event=event)
                image_uris = [
                    {'uri': image.image['uri']} if isinstance(image.image, dict) and 'uri' in image.image
                    else {'uri': None}
                    for image in images
                ]

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
                    'photos': event.photos,
                    'price': event.price,
                    'claps': event.claps,
                    'ticket': event.ticket,
                    'date': str(event.date),
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
