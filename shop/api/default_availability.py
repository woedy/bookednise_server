from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from django.contrib.auth.models import User

from shop.models import ShopAvailability
from slots.models import StaffSlot, TimeSlot
from django.db import transaction


def create_default_staff_availability(shop_id, staff_user):
    """
    Create the default staff availability for the next 7 days based on the shop's availability.
    """
    shop_availability = ShopAvailability.objects.filter(shop_id=shop_id, active=True)
    
    for availability in shop_availability:
        shop_date = availability.date
        open_time = availability.open
        close_time = availability.closed
        
        # Calculate time difference (i.e., the number of time slots between open and close)
        start_time = make_aware(datetime.combine(shop_date, open_time))
        end_time = make_aware(datetime.combine(shop_date, close_time))
        
        # Loop through the week (7 days)
        for i in range(7):  # For 7 days from shop availability
            staff_slot_date = shop_date + timedelta(days=i)
            staff_slot = StaffSlot.objects.create(
                user=staff_user,  # Assign the newly created user as the staff member
                slot_date=staff_slot_date,
                state="Vacant",
                is_recurring=False,
                active=True
            )
            
            # Generate time slots for this date based on shop's open and close time
            current_time = start_time
            while current_time < end_time:
                time_slot = TimeSlot.objects.create(
                    staff_slot=staff_slot,
                    time=current_time.time(),
                    occupied=False,
                    active=True
                )
                current_time += timedelta(hours=1)  # Increment by 1 hour for each time slot







from django.db import transaction

def create_or_update_staff_availability2222(shop, staff_user):
    with transaction.atomic():
        shop_availability = ShopAvailability.objects.filter(shop=shop, active=True)

        for availability in shop_availability:
            shop_date = availability.date
            open_time = availability.open
            close_time = availability.closed

            start_time = make_aware(datetime.combine(shop_date, open_time))
            end_time = make_aware(datetime.combine(shop_date, close_time))

            for i in range(7):
                staff_slot_date = shop_date + timedelta(days=i)

                # Get or create the staff slot
                staff_slot, created = StaffSlot.objects.get_or_create(
                    user=staff_user,
                    slot_date=staff_slot_date,
                    defaults={'state': 'Vacant', 'is_recurring': False, 'active': True}
                )

                if not created:
                    staff_slot.state = 'Vacant'
                    staff_slot.save()

                # Create or update the time slots
                current_time = start_time
                while current_time < end_time:
                    time_slot, created = TimeSlot.objects.get_or_create(
                        staff_slot=staff_slot,
                        time=current_time.time(),
                        defaults={'occupied': False, 'active': True}
                    )

                    if not created:
                        time_slot.occupied = False
                        time_slot.save()

                    current_time += timedelta(hours=1)









# Dictionary to map days of the week to their index (0 = Monday, 6 = Sunday)
DAYS_OF_WEEK = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6
}


def create_or_update_staff_availability(shop, staff_user):
    """
    Create or update the default staff availability for the next 7 days based on the shop's availability.
    """
    # Fetch the shop's weekly availability
    shop_availability = ShopAvailability.objects.filter(shop=shop, active=True)

    # Get today's date
    today = datetime.today()

    for availability in shop_availability:
        shop_day = availability.day
        open_time = availability.open_time
        close_time = availability.closed_time
        
        # Skip days that are closed or have None values
        if open_time == "Closed" or close_time == "Closed" or open_time is None or close_time is None:
            continue
        
        # Get the date for the specific day in the upcoming week, starting from today
        target_date = get_date_for_day(shop_day, today)

        # Ensure open_time and close_time are datetime objects and properly formatted
        if isinstance(open_time, str):
            open_time = datetime.strptime(open_time, "%H:%M").time()
        if isinstance(close_time, str):
            close_time = datetime.strptime(close_time, "%H:%M").time()

        # If the target date is in the future, create/update the staff availability
        if target_date >= today:
            # Get or create the staff slot for this specific date
            staff_slot, created = StaffSlot.objects.get_or_create(
                user=staff_user,
                slot_date=target_date,
                defaults={'state': 'Vacant', 'is_recurring': True, 'active': True}
            )
            # If the StaffSlot already exists, you can optionally update its properties
            if not created:
                staff_slot.state = 'Vacant'  # Resetting the state (if necessary)
                staff_slot.save()

            # Generate or update time slots for this date based on shop's open and close time
            if open_time and close_time:  # Ensure both times are valid
                start_time = make_aware(datetime.combine(target_date, open_time))
                end_time = make_aware(datetime.combine(target_date, close_time))
                current_time = start_time
                while current_time < end_time:
                    time_slot, created = TimeSlot.objects.get_or_create(
                        staff_slot=staff_slot,
                        time=current_time.time(),
                        defaults={'occupied': False, 'active': True}
                    )
                    if not created:
                        # Optionally update time slot properties (e.g., reset occupancy)
                        time_slot.occupied = False
                        time_slot.save()
                    current_time += timedelta(hours=1)  # Increment by 1 hour for each time slot




def get_date_for_day(day_name, start_date):
    """
    Given a day name (e.g., 'Monday'), return the date for that day in the current or next week
    starting from `start_date`.
    """
    # Get the current day of the week (0 = Monday, 6 = Sunday)
    current_day_of_week = start_date.weekday()

    # Get the target day index from DAYS_OF_WEEK dictionary
    target_day_index = DAYS_OF_WEEK.get(day_name)

    # Calculate the difference in days to the target day
    delta_days = target_day_index - current_day_of_week

    if delta_days < 0:  # If the target day has already passed in the current week, add 7 days
        delta_days += 7

    target_date = start_date + timedelta(days=delta_days)
    return target_date