import math
import random
import re
import string
from django.contrib.auth import get_user_model, authenticate




def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_random_otp_code():
    code = ''
    for i in range(4):
        code += str(random.randint(0, 9))
    return code


def unique_user_id_generator(instance):
    """
    This is for a django project with a user_id field
    :param instance:
    :return:
    """

    size = random.randint(30,45)
    user_id = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(user_id=user_id).exists()
    if qs_exists:
        return
    return user_id





def unique_shop_id_generator(instance):
    """
    This is for a django project with a shop_id field
    :param instance:
    :return:
    """

    size = random.randint(30,45)
    shop_id = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(shop_id=shop_id).exists()
    if qs_exists:
        return
    return shop_id

def generate_email_token():
    code = ''
    for i in range(4):
        code += str(random.randint(0, 9))
    return code




def unique_promotion_id_generator(instance):
    """
    This is for a promotion_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    promotion_id = "PROMO-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(P)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(promotion_id=promotion_id).exists()
    if qs_exists:
        return None
    return promotion_id

def unique_pack_promotion_id_generator(instance):
    """
    This is for a pack_promotion_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    pack_promotion_id = "PK-PROMO-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(P)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(pack_promotion_id=pack_promotion_id).exists()
    if qs_exists:
        return None
    return pack_promotion_id



def unique_service_id_generator(instance):
    """
    This is for a service_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    service_id = "BK-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(S)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(service_id=service_id).exists()
    if qs_exists:
        return None
    return service_id



def unique_booking_id_generator(instance):
    """
    This is for a booking_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    booking_id = "BK-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "_AP"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(booking_id=booking_id).exists()
    if qs_exists:
        return None
    return booking_id

def unique_room_id_generator(instance):
    """
    This is for a room_id field
    :param instance:
    :return:
    """
    size = random.randint(30, 45)
    room_id = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(room_id=room_id).exists()
    if qs_exists:
        return None
    return room_id


def unique_staff_id_generator(instance):
    """
    This is for a staff_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    staff_id = "STF-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(S)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(staff_id=staff_id).exists()
    if qs_exists:
        return None
    return staff_id




def unique_account_id_generator(instance):
    """
    This is for a account_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    account_id = "ACC-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(BNK)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(account_id=account_id).exists()
    if qs_exists:
        return None
    return account_id


def unique_transaction_id_generator(instance):
    """
    This is for a transaction_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    transaction_id = "TRN-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(P)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(transaction_id=transaction_id).exists()
    if qs_exists:
        return None
    return transaction_id



def haversine(lon1, lat1, lon2, lat2):
    # Check for None values
    if None in (lon1, lat1, lon2, lat2):
        raise ValueError("Coordinates cannot be None.")

    R = 6371  # Earth radius in kilometers

    dlon = math.radians(lon2 - lon1)
    dlat = math.radians(lat2 - lat1)

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))

    return R * c  # Distance in kilometers




    
def convert_phone_number(phone):
    # Match pattern for phone numbers starting with "+" followed by the country code
    # and replace with "0" + the local part of the number.
    match = re.match(r"^\+(\d{1,3})(\d{9,10})$", phone)
    if match:
        return "0" + match.group(2)  # Extracts the local number part and prepends "0"
    return phone
