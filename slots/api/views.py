from datetime import datetime, date, timedelta

import pytz
from click.core import F
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.db.models import Q, ExpressionWrapper
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status, fields
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from activities.models import AllActivity
from shop.api.default_availability import create_or_update_staff_availability
from shop.models import Shop
from slots.api.serializers import StaffSlotSerializer
from slots.models import StaffSlot, TimeSlot

User = get_user_model()

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def set_staff_slot_shop_default(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        staff_user_id = request.data.get('staff_user_id', "")
        shop_id = request.data.get('shop_id', "")

        if not staff_user_id:
            errors['staff_user_id'] = ['Staff User ID is required.']

        if not shop_id:
            errors['shop_id'] = ['Shop ID is required.']

        try:
            shop = Shop.objects.get(shop_id=shop_id)
        except Shop.DoesNotExist:
            errors['shop_id'] = ['Shop does not exist.']

        try:
            staff = User.objects.get(user_id=staff_user_id)
        except:
            errors['staff_user_id'] = ['Staff does not exist.']
     

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        

        create_or_update_staff_availability(shop, staff)

        
        payload['message'] = "Slot added or updated successfully"
        payload['data'] = data

        return Response(payload)



@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def set_staff_slot(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        staff_user_id = request.data.get('staff_user_id', "")
        shop_id = request.data.get('shop_id', "")
        timezone = request.data.get('timezone', "")
        availability = request.data.get('availability', [])

        if not staff_user_id:
            errors['staff_user_id'] = ['Staff User ID is required.']

        if not shop_id:
            errors['shop_id'] = ['Shop ID is required.']

        if not timezone:
            errors['timezone'] = ['Timezone is required.']

        if not availability:
            errors['availability'] = ['Availability is required.']

        try:
            shop = Shop.objects.get(shop_id=shop_id)
        except Shop.DoesNotExist:
            errors['shop_id'] = ['Shop does not exist.']

        try:
            staff = User.objects.get(user_id=staff_user_id)
            interval = staff.availability_interval

            if interval is None:
                errors['availability'] = [f'Please set your availability interval first.']
                payload['message'] = "Errors"
                payload['errors'] = errors
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the existing slots for the practitioner
            existing_slots = StaffSlot.objects.filter(user=staff)
            existing_slot_dates = existing_slots.values_list('slot_date', flat=True)

            staff_list = ['Saloon Staff']
            if staff.user_type in staff_list:
                for slot_data in availability:
                    slot_date = slot_data.get('date')
                    new_time_slots = slot_data.get('time_slots')

                    # Convert the times to datetime objects
                    # # Check if the times are at least  hours apart
                    # if not are_times_spaced(interval, time_objects):
                    #     errors['availability'] = [f'Times provided should be at least {interval} apart.']
                    #     payload['message'] = "Errors"
                    #     payload['errors'] = errors
                    #     return Response(payload, status=status.HTTP_400_BAD_REQUEST)

                    # Check if a slot with the same date already exists
                    existing_slot = existing_slots.filter(slot_date=slot_date).first()

                    if existing_slot:
                        # Slot already exists, update it
                        existing_time_slots = TimeSlot.objects.filter(staff_slot=existing_slot)

                        # Iterate through the new time slots
                        for time in new_time_slots:
                            existing_time_slot = existing_time_slots.filter(time=time).first()
                            if existing_time_slot:
                                if existing_time_slot.occupied:
                                    # Time slot is occupied, continue to the next slot
                                    continue
                            else:
                                # Create a new time slot if it doesn't exist
                                TimeSlot.objects.create(
                                    staff_slot=existing_slot,
                                    time=time,
                                    occupied=False
                                )
                        # Delete time slots that are not in the new list
                        existing_time_slots.filter(~Q(time__in=new_time_slots)).delete()
                    else:
                        # Slot doesn't exist, create a new slot
                        new_slot = StaffSlot.objects.create(user=staff, slot_date=slot_date)
                        for time in new_time_slots:
                            TimeSlot.objects.create(
                                staff_slot=new_slot,
                                time=time,
                                occupied=False
                            )

                # Delete slots that are not in the new list
                existing_slots.filter(~Q(slot_date__in=[s['date'] for s in availability])).delete()

        except User.DoesNotExist:
            errors['staff_id'] = ['Staff does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Slot added or updated successfully"
        payload['data'] = data

        return Response(payload)







@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def set_staff_slot22222(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        staff_user_id = request.data.get('staff_user_id', "")
        shop_id = request.data.get('shop_id', "")
        timezone = request.data.get('timezone', "")
        availability = request.data.get('availability', [])

        if not staff_user_id:
            errors['staff_user_id'] = ['Staff User ID is required.']

        if not shop_id:
            errors['shop_id'] = ['Shop ID is required.']

        if not timezone:
            errors['timezone'] = ['Timezone is required.']

        if not availability:
            errors['availability'] = ['Availability is required.']

        try:
            shop = Shop.objects.get(shop_id=shop_id)
        except Shop.DoesNotExist:
            errors['shop_id'] = ['Shop does not exist.']

        try:
            staff = User.objects.get(user_id=staff_user_id)
            interval = staff.availability_interval

            if interval is None:
                errors['availability'] = [f'Please set your availability interval first.']
                payload['message'] = "Errors"
                payload['errors'] = errors
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the existing slots for the practitioner
            existing_slots = StaffSlot.objects.filter(user=staff)
            existing_slot_dates = existing_slots.values_list('slot_date', flat=True)

            staff_list = ['Saloon Staff']
            if staff.user_type in staff_list:
                for slot_data in availability:
                    slot_date = slot_data.get('date')
                    new_time_slots = slot_data.get('time_slots')

                    # Convert the times to datetime objects
                    # # Check if the times are at least  hours apart
                    # if not are_times_spaced(interval, time_objects):
                    #     errors['availability'] = [f'Times provided should be at least {interval} apart.']
                    #     payload['message'] = "Errors"
                    #     payload['errors'] = errors
                    #     return Response(payload, status=status.HTTP_400_BAD_REQUEST)

                    # Check if a slot with the same date already exists
                    existing_slot = existing_slots.filter(slot_date=slot_date).first()

                    if existing_slot:
                        # Slot already exists, update it
                        existing_time_slots = TimeSlot.objects.filter(staff_slot=existing_slot)

                        # Iterate through the new time slots
                        for time in new_time_slots:
                            existing_time_slot = existing_time_slots.filter(time=time).first()
                            if existing_time_slot:
                                if existing_time_slot.occupied:
                                    # Time slot is occupied, continue to the next slot
                                    continue
                            else:
                                # Create a new time slot if it doesn't exist
                                TimeSlot.objects.create(
                                    staff_slot=existing_slot,
                                    time=time,
                                    occupied=False
                                )
                        # Delete time slots that are not in the new list
                        existing_time_slots.filter(~Q(time__in=new_time_slots)).delete()
                    else:
                        # Slot doesn't exist, create a new slot
                        new_slot = StaffSlot.objects.create(user=staff, slot_date=slot_date)
                        for time in new_time_slots:
                            TimeSlot.objects.create(
                                staff_slot=new_slot,
                                time=time,
                                occupied=False
                            )

                # Delete slots that are not in the new list
                existing_slots.filter(~Q(slot_date__in=[s['date'] for s in availability])).delete()

        except User.DoesNotExist:
            errors['staff_id'] = ['Staff does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Slot added or updated successfully"
        payload['data'] = data

        return Response(payload)







def are_times_spaced(interval, times):
    # Calculate the minimum required time difference in minutes
    required_minutes = get_interval_in_minutes(interval)

    for i in range(1, len(times)):
        time_difference = calculate_time_difference(times[i], times[i - 1])
        if time_difference < required_minutes:
            return False

    return True





def get_interval_in_minutes(interval):
    intervals = {
        '1 hour': 1 * 60,
        '6 hours': 6 * 60,
        '8 hours': 8 * 60,
        '12 hours': 12 * 60,
        '24 hours': 24 * 60,
        '48 hours': 48 * 60,
    }
    return intervals.get(interval, 0)

def calculate_time_difference(time1, time2):
    dt1 = datetime.combine(date.today(), time1)
    dt2 = datetime.combine(date.today(), time2)
    return (dt1 - dt2).total_seconds() / 60



@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def list_staff_availability(request):
    payload = {}
    data = {}

    errors = {}

    if request.method == 'POST':
        staff_user_id = request.data.get('staff_user_id', "")
        shop_id = request.data.get('shop_id', "")

        if not staff_user_id:
            errors['staff_user_id'] = ['Staff User ID is required.']

        if not shop_id:
            errors['shop_id'] = ['Shop ID is required.']

        try:
            shop = Shop.objects.get(shop_id=shop_id)
        except Shop.DoesNotExist:
            errors['shop_id'] = ['Shop does not exist.']

        try:
            staff = User.objects.get(user_id=staff_user_id)
            availability_interval = staff.availability_interval

            # Calculate the datetime threshold based on the specified interval
            current_datetime = datetime.now()
            interval_mapping = {
                "1 hour": timedelta(hours=1),
                "6 hours": timedelta(hours=6),
                "12 hours": timedelta(hours=12),
                "8 hours": timedelta(hours=8),
                "24 hours": timedelta(hours=24),
                "48 hours": timedelta(hours=48)
            }
            threshold_datetime = current_datetime + interval_mapping.get(availability_interval, timedelta(hours=1))

            data['availability_interval'] = availability_interval

            # Filter availability slots based on the threshold_datetime
            all_staff_slots = StaffSlot.objects.filter(
                user=staff,
                slot_date__gte=threshold_datetime.date(),
            )

            #print(current_datetime.date())
            #print("###############")

            for _slot in all_staff_slots:
                if str(current_datetime.date()) == str(_slot.slot_date):
                    # check slots with times before the threshold time
                    print(_slot.slot_date)
                    print(_slot.slot_times)

            all_staff_slots_serializer = StaffSlotSerializer(all_staff_slots, many=True)
            _all_staff_slots = all_staff_slots_serializer.data
            data['all_staff_slots'] = _all_staff_slots

        except User.DoesNotExist:
            errors['staff_id'] = ['Staff does not exist']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Successful"
        payload['data'] = data
        return Response(payload)




@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def list_staff_availability_current_date(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        staff_user_id = request.data.get('staff_user_id', "")
        shop_id = request.data.get('shop_id', "")

        if not staff_user_id:
            errors['staff_user_id'] = ['Staff User ID is required.']

        if not shop_id:
            errors['shop_id'] = ['Shop ID is required.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        try:
            shop = Shop.objects.get(shop_id=shop_id)
        except Shop.DoesNotExist:
            errors['shop_id'] = ['Shop does not exist.']
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        try:
            staff = User.objects.get(user_id=staff_user_id)
            availability_interval = staff.availability_interval

            # Calculate the datetime threshold based on the specified interval
            current_datetime = datetime.now()
            interval_mapping = {
                "1 hour": timedelta(hours=1),
                "6 hours": timedelta(hours=6),
                "12 hours": timedelta(hours=12),
                "8 hours": timedelta(hours=8),
                "24 hours": timedelta(hours=24),
                "48 hours": timedelta(hours=48)
            }
            threshold_datetime = current_datetime + interval_mapping.get(availability_interval, timedelta(hours=1))

            data['availability_interval'] = availability_interval

            # Filter availability slots based on the threshold_datetime
            all_staff_slots = StaffSlot.objects.filter(
                user=staff,
                slot_date__gte=current_datetime.date()  # Include current date
            )

            # Serialize the filtered slots
            all_staff_slots_serializer = StaffSlotSerializer(all_staff_slots, many=True)
            _all_staff_slots = all_staff_slots_serializer.data
            data['all_staff_slots'] = _all_staff_slots

        except User.DoesNotExist:
            errors['staff_id'] = ['Staff does not exist']
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Successful"
        payload['data'] = data
        return Response(payload)



@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def set_availability_interval(request):
    payload = {}
    data = {}

    errors = {}

    if request.method == 'POST':

        staff_user_id = request.data.get('staff_user_id', "")
        shop_id = request.data.get('shop_id', "")
        interval = request.data.get('interval', "")


        if not staff_user_id:
            errors['staff_user_id'] = ['Staff User ID is required.']

        if not shop_id:
            errors['shop_id'] = ['Shop ID is required.']



        if not interval:
            errors['interval'] = ['Interval is required.']

        try:
            shop = Shop.objects.get(shop_id=shop_id)
        except Shop.DoesNotExist:
            errors['shop_id'] = ['Shop does not exist.']


        staff = User.objects.get(user_id=staff_user_id)

        if staff.user_type == "Saloon Staff":
            staff.availability_interval = interval
            staff.save()
        else:
            errors['pract_id'] = ['User is not a practitioner.']





        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
##
##
        #data['appintment_slot_id'] = new_slot.id

        payload['message'] = "Successful, Availability interval set."
        payload['data'] = data

        return Response(payload)



@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def update_staff_slot(request):
    payload = {}
    data = {}

    errors = {}

    if request.method == 'POST':


        availability = request.data.get('availability', "")
        staff_user_id = request.data.get('staff_user_id', "")
        shop_id = request.data.get('shop_id', "")


        if not staff_user_id:
            errors['staff_user_id'] = ['Staff User ID is required.']

        if not shop_id:
            errors['shop_id'] = ['Shop ID is required.']

        if not availability:
            errors['availability'] = ['Availability is required.']



        try:
            shop = Shop.objects.get(shop_id=shop_id)
        except Shop.DoesNotExist:
            errors['shop_id'] = ['Shop does not exist.']



        staff = User.objects.get(user_id=staff_user_id)
        interval = staff.availability_interval

        if interval is None:
            errors['availability'] = [f'Please set your availability interval first.']
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        try:

            for old_slot in availability:
                slot = StaffSlot.objects.get(id=old_slot['slot_id'])
                slot.slot_date = old_slot['date']
                slot.save()

                time_slots_data = TimeSlot.objects.all().filter(staff_slot=slot)
                for time in time_slots_data:
                    time.delete()

                # Convert the times to datetime objects
                time_objects = [datetime.strptime(t, "%H:%M:%S" if len(t) > 5 else "%H:%M").time() for t in old_slot['time_slots']]

                # Check if the times are at least  hours apart
                if not are_times_spaced(interval, time_objects):
                    errors['availability'] = [f'Times provided should be at least {interval} apart.']
                    payload['message'] = "Errors"
                    payload['errors'] = errors
                    return Response(payload, status=status.HTTP_400_BAD_REQUEST)


            for time in old_slot['time_slots']:
                    new_time_slot = TimeSlot.objects.create(
                        staff_slot=slot,
                        time=time
                    )

                    # Add new ACTIVITY
                    new_activity = AllActivity.objects.create(
                        user=User.objects.get(id=1),
                        subject="Availability Updated",
                        body=f"An appointee just updated their availability."
                    )
                    new_activity.save()

        except StaffSlot.DoesNotExist:
            errors['slot_id'] = ['Object is removed.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
##
##
        #data['appintment_slot_id'] = slot.id

        payload['message'] = "Slot updated successfully"
        payload['data'] = data

        return Response(payload)



@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def remove_staff_slot(request):
    payload = {}
    data = {}

    errors = {}

    if request.method == 'POST':

        staff_user_id = request.data.get('staff_user_id', "")
        shop_id = request.data.get('shop_id', "")
        slot_id = request.data.get('slot_id', "")

        if not staff_user_id:
            errors['staff_user_id'] = ['Staff User ID is required.']

        if not shop_id:
            errors['shop_id'] = ['Shop ID is required.']

        if not slot_id:
            errors['slot_id'] = ['Slot ID is required.']

        try:
            shop = Shop.objects.get(shop_id=shop_id)
        except:
            errors['shop_id'] = ['Shop does not exist.']

        try:
            slot = StaffSlot.objects.get(id=slot_id)
            slot.delete()
        except:
            errors['slot_id'] = ['Slot does not exist.']



        # Add new ACTIVITY
        new_activity = AllActivity.objects.create(
            user=User.objects.get(id=1),
            subject="Slot Removed",
            body=f"Slot Removed."
        )
        new_activity.save()

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
##
##
        #data['appintment_slot_id'] = slot.id

        payload['message'] = "Slot removed successfully"
        payload['data'] = data

        return Response(payload)
