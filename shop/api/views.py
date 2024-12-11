from decimal import Decimal
import math
import re
from datetime import datetime

from celery import chain
import googlemaps
import requests


from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from django.template.loader import get_template

from bank_account.models import BankAccount
from bookednise_pro.tasks import send_generic_email

from accounts.api.serializers import UserRegistrationSerializer, StaffRegistrationSerializer
from activities.models import AllActivity
from bookednise_pro import settings
from bookednise_pro.utils import convert_phone_number, generate_email_token, haversine
from bookings.api.serializers import BookingSeriveSerializer, ServiceCategorySerializer
from payments.models import PaymentSetup
from shop.api.serializers import ShopDetailSerializer, ListShopsSerializer, ShopStaffSerializer, ShopServiceSerializer, \
    ShopServiceDetailSerializer, ShopPackageSerializer, ShopAvailabilitySerializer
from shop.models import ServiceCategory, Shop, ShopInterior, ShopExterior, ShopVisit, ShopWork, ShopService, ShopStaff, ShopPackage, \
    ServiceSpecialist, ShopAvailability, get_default_package_image, get_default_staff_image
from rest_framework.authtoken.models import Token
from django.core.mail import EmailMessage, send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from datetime import timedelta
from django.db.models import Count

User = get_user_model()

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def check_shop_email_exists(request):
    payload = {}
    data = {}
    errors = {}

    email = request.data.get('email', '')


    if not email:
        errors['email'] = ['User Email is required.']
    elif not is_valid_email(email):
        errors['email'] = ['Valid email required.']
    elif check_email_exist(email):
        errors['email'] = ['Email already exists in our database.']


    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def check_registration_complete(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')


    if not shop_id:
        errors['shop_id'] = ['Shop ID is required.']

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except:
        errors['shop_id'] = ['Shop does not exist.']


    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)
    
    data['status'] = {
        'shop_registered': shop.shop_registered,
        'shop_setup': shop.shop_setup,
        'service_setup': shop.service_setup,
        'payment_setup': shop.payment_setup,
        'staff_setup': shop.staff_setup,
    }

    data['registration_complete'] = shop.registration_complete

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def admin_add_shop_view(request):
    payload = {}
    data = {}
    errors = {}

    full_name = request.data.get('full_name', '')
    contact = request.data.get('contact', '')
    email = request.data.get('email', '')
    country = request.data.get('country', '')
    street_address1 = request.data.get('street_address1', '')
    street_address2 = request.data.get('street_address2', '')
    city = request.data.get('city', '')
    state = request.data.get('state', '')
    zipcode = request.data.get('zipcode', '')
    location_name = request.data.get('location_name', '')
    location_lat = request.data.get('location_lat', '')
    location_lng = request.data.get('location_lng', '')
    business_type = request.data.get('business_type', '')
    business_logo = request.data.get('business_logo', '')

    password = request.data.get('password', 'Bookelu123!_')
    password2 = request.data.get('password2', 'Bookelu123!_')

    if not email:
        errors['email'] = ['User Email is required.']
    elif not is_valid_email(email):
        errors['email'] = ['Valid email required.']
    elif check_email_exist(email):
        errors['email'] = ['Email already exists in our database.']

    if not full_name:
        errors['full_name'] = ['Shop full name is required.']

    if not contact:
        errors['contact'] = ['Contact number is required.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserRegistrationSerializer(data=request.data)
    user = None
    if serializer.is_valid():
        user = serializer.save()
        data["user_id"] = user.user_id
        data["email"] = user.email
        data["shop_name"] = user.full_name

        user.user_type = "Shop"
        user.save()

    new_shop = Shop.objects.create(
        user=user,
        email=email,
        shop_name=full_name,
        phone=contact,
        country=country,
        street_address1=street_address1,
        street_address2=street_address2,
        city=city,
        state=state,
        zipcode=zipcode,
        location_name=location_name,
        lat=location_lat,
        lng=location_lng,
        business_type=business_type,
        photo=business_logo,

    )

    new_shop.shop_registered = True
    new_shop.save()

    token = Token.objects.get(user=user).key
    data['token'] = token

    data['shop_id'] = new_shop.shop_id

    email_token = generate_email_token()

    user = User.objects.get(email=email)
    user.email_token = email_token
    user.save()

    context = {
        'email_token': email_token,
        'email': user.email,
        'full_name': user.full_name
    }

    txt_ = get_template("registration/emails/verify.html").render(context)
    html_ = get_template("registration/emails/verify.txt").render(context)

    subject = 'EMAIL CONFIRMATION CODE'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    #  # Use Celery chain to execute tasks in sequence
    #  email_chain = chain(
    #      send_generic_email.si(subject, txt_, from_email, recipient_list, html_),
    #  )
    #  # Execute the Celery chain asynchronously
    #  email_chain.apply_async()

    send_mail(
        subject,
        txt_,
        from_email,
        recipient_list,
        html_message=html_,
        fail_silently=False,
    )


    #
    new_activity = AllActivity.objects.create(
        user=user,
        subject="Shop Registration",
        body= "Admin Just created an account."
    )
    new_activity.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def add_shop_view(request):
    payload = {}
    data = {}
    errors = {}

    full_name = request.data.get('full_name', '')
    contact = request.data.get('contact', '')
    email = request.data.get('email', '')
    country = request.data.get('country', '')
    street_address1 = request.data.get('street_address1', '')
    street_address2 = request.data.get('street_address2', '')
    city = request.data.get('city', '')
    state = request.data.get('state', '')
    zipcode = request.data.get('zipcode', '')

    password = request.data.get('password', '')
    password2 = request.data.get('password2', '')

    contact = convert_phone_number(contact)


    if not email:
        errors['email'] = ['User Email is required.']
    elif not is_valid_email(email):
        errors['email'] = ['Valid email required.']
    elif check_email_exist(email):
        errors['email'] = ['Email already exists in our database.']

    if not full_name:
        errors['full_name'] = ['Shop full name is required.']

    #if not contact:
    #    errors['contact'] = ['Contact number is required.']

    if not password:
        errors['password'] = ['Password is required.']

    if not password2:
        errors['password2'] = ['Password2 is required.']

    if password != password2:
        errors['password'] = ['Passwords dont match.']

    if not is_valid_password(password):
        errors['password'] = [
            'Password must be at least 8 characters long\n- Must include at least one uppercase letter,\n- One lowercase letter, one digit,\n- And one special character']

    if check_shop_name_exist(full_name):
        errors['full_name'] = ['Shop name already exists in our database.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        data["user_id"] = user.user_id
        data["email"] = user.email
        data["shop_name"] = user.full_name

        user.user_type = "Shop"
        user.save()

    new_shop = Shop.objects.create(
        user=user,
        email=email,
        shop_name=full_name,
        phone=contact,
        country=country,
        street_address1=street_address1,
        street_address2=street_address2,
        city=city,
        state=state,
        zipcode=zipcode

    )

    new_shop.shop_registered = True
    new_shop.save()


    if (new_shop.shop_registered == True and 
        new_shop.shop_setup == True and
        new_shop.service_setup == True and
        new_shop.payment_setup == True and
        new_shop.staff_setup == True
        ):
         new_shop.registration_complete = True
         new_shop.save()
    else:
        new_shop.registration_complete = False
        new_shop.save()

    new_bank_account = BankAccount.objects.create(
        user=user,

    )
    data['account_id'] = new_bank_account.account_id


    token = Token.objects.get(user=user).key
    data['token'] = token

    data['shop_id'] = new_shop.shop_id

    email_token = generate_email_token()

    user = User.objects.get(email=email)
    user.email_token = email_token
    user.save()

    #     ##### SEND SMS

    # _msg = f'Your BoodedNise OTP code is {email_token}'
    # url = f"https://apps.mnotify.net/smsapi"
    # api_key = settings.MNOTIFY_KEY  # Replace with your actual API key
    # print(api_key)
    # response = requests.post(url,
    # data={
    #     "key": api_key,
    #     "to": new_shop.phone,
    #     "msg": _msg,
    #     "sender_id": settings.MNOTIFY_SENDER_ID,
    #     })
    # if response.status_code == 200:
    #     print('##########################')
    #     print(response.content)
    #     payload['message'] = "Successful"
    # else:
    #     errors['user_id'] = ['Faitled to send SMS']
        ######################

    context = {
        'email_token': email_token,
        'email': user.email,
        'full_name': user.full_name
    }
#
    txt_ = get_template("registration/emails/verify.txt").render(context)
    html_ = get_template("registration/emails/verify.html").render(context)
#
    subject = 'EMAIL CONFIRMATION CODE'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    # Use Celery chain to execute tasks in sequence
    # email_chain = chain(
    #     send_generic_email.si(subject, txt_, from_email, recipient_list, html_),
    # )
    # # Execute the Celery chain asynchronously
    # email_chain.apply_async()
    send_mail(
        subject,
        txt_,
        from_email,
        recipient_list,
        html_message=html_,
        fail_silently=False,
    )



    #
    new_activity = AllActivity.objects.create(
        user=user,
        subject="Shop Registration",
        body=user.email + " Just created an account."
    )
    new_activity.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def edit_shop_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')

    full_name = request.data.get('full_name', '')
    contact = request.data.get('contact', '')
    email = request.data.get('email', '')
    country = request.data.get('country', '')
    street_address1 = request.data.get('street_address1', '')
    street_address2 = request.data.get('street_address2', '')
    city = request.data.get('city', '')
    state = request.data.get('state', '')
    zipcode = request.data.get('zipcode', '')
    location_name = request.data.get('location_name', '')
    location_lat = request.data.get('location_lat', '')
    location_lng = request.data.get('location_lng', '')
    business_type = request.data.get('business_type', '')
    business_logo = request.data.get('business_logo', '')
    cvr = request.data.get('cvr', '')
    special_features = request.data.get('special_features', '')
    description = request.data.get('description', '')
    
    business_days = request.data.get('business_days', '')
    business_hours_open = request.data.get('business_hours_open', '')
    business_hours_close = request.data.get('business_hours_close', '')

    #if not email:
    #    errors['email'] = ['User Email is required.']
    #elif not is_valid_email(email):
    #    errors['email'] = ['Valid email required.']

    if not shop_id:
        errors['shop_id'] = ['Shop ID is required.']

    #if not full_name:
    #    errors['full_name'] = ['Shop full name is required.']
#
    #if not contact:
    #    errors['contact'] = ['Contact number is required.']


    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except:
        errors['shop_id'] = ['Shop does not exist.']



    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)
    
    if shop_id:
        shop.user = shop.user
    if email:
        shop.email = email
    if full_name:
        shop.user.full_name = full_name
    shop.user.save()



    if email:
        shop.email = email
    if full_name:
        shop.shop_name = full_name
    if contact:
        shop.phone = contact
    if country:
        shop.country = country
    if street_address1:
        shop.street_address1 = street_address1
    if street_address2:
        shop.street_address2 = street_address2
    if city:
        shop.city = city
    if state:
        shop.state = state
    if zipcode:
        shop.zipcode = zipcode
    if location_name:
        shop.location_name = location_name
    if location_lat:
        shop.lat = location_lat
    if location_lng:
        shop.lng = location_lng
    if business_type:
        shop.business_type = business_type
    if business_logo:
        shop.photo = business_logo
    if cvr:
        shop.cvr = cvr
    if special_features:
        shop.special_features = special_features

    if description:
        shop.description = description
        
    if business_days:
        shop.business_days = business_days
    if business_hours_open:
        shop.business_hours_open = business_hours_open
    if business_hours_close:
        shop.business_hours_close = business_hours_close

    shop.save()


    data['shop_id'] = shop.shop_id

    #new_activity = AllActivity.objects.create(
    #    user=shop_user,
    #    subject="Shop Edited",
    #    body=shop.email + " Just edited an account."
    #)
    #new_activity.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def setup_shop_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    description = request.data.get('description', '')
    business_days = request.data.get('business_days', '')
    business_hours_open = request.data.get('business_hours_open', '')
    business_hours_close = request.data.get('business_hours_close', '')
    special_features = request.data.get('special_features', '')

    location_name = request.data.get('location_name', '')
    location_lat = Decimal(request.data.get('location_lat', '0.0'))  if request.data.get('location_lat') else None
    location_lng = Decimal(request.data.get('location_lng', '0.0'))  if request.data.get('location_lng') else None
    business_type = request.data.get('business_type', '')
    business_logo = request.data.get('business_logo', '')
    cvr = request.data.get('cvr', '')

    #if not description:
    #    errors['description'] = ["Description required"]

    if not shop_id:
        errors['shop_id'] = ['Shop ID is required.']

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        errors['shop_id'] = ['Shop does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    shop = Shop.objects.get(shop_id=shop_id)
    shop.description = description
    shop.business_days = business_days
    shop.business_hours_open = business_hours_open
    shop.business_hours_close = business_hours_close
    shop.special_features = special_features

    shop.location_name = location_name
    shop.lat = location_lat
    shop.lng = location_lng
    shop.business_type = business_type
    shop.cvr = cvr
    shop.photo = business_logo
    shop.save()



    shop.shop_setup = True
    shop.save()

    if (shop.shop_registered == True and 
        shop.shop_setup == True and
        shop.service_setup == True and
        shop.payment_setup == True and
        shop.staff_setup == True
        ):
         shop.registration_complete = True
         shop.save()
    else:
        shop.registration_complete = False
        shop.save()


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_shop_location_address_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    address = request.data.get('address', "")

    if not shop_id:
        errors['shop_id'] = ['Shop ID is required.']
    if not address:
        errors['address'] = ['Address is required.']

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        errors['shop_id'] = ['Shop does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)
    

    #######

    url = "https://ghanapostgps.sperixlabs.org/get-location"
    
    _address = 'address=' + address
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.request("POST", url, headers=headers, data = _address)

        print("##################################")
        print("##################################")
        print("##################################")
        #print(response.json())
        res = response.json()
        location_name = address
        lat = res['data']['Table'][0]['CenterLatitude']
        lng = res['data']['Table'][0]['CenterLongitude']


        print(location_name)
        print(lat)
        print(lng)

        shop.digital_address = address
        shop.lat = lat
        shop.lng = lng
        shop.save()

        location_name = get_location_name_google(lat, lng)
        shop.location_name = location_name
        shop.save()

        
        data['location_name'] = location_name
        data['digital_address'] = address
        data['lat'] = lat
        data['lng'] = lng

    except:
        print("##################################")
        print("##################################")
        print(res)
        errors['address'] = ['Address Not found']

 


    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)
    



    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_location_name(request):
    payload = {}
    data = {}
    errors = {}

    latitude = request.data.get('lat', '')
    longitude = request.data.get('lng', '')

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    if latitude and longitude:
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            location_name = get_location_name_google(latitude, longitude)

            print('############################')
            print('############################')
            print(location_name)
        except Exception as e:
            location_name = "Error fetching location"
            print('############################')
            print('############################')
            print(str(e))
    else:
        location_name = "No coordinates provided"
        print('############################')
        print('############################')
        print(location_name)

    data['location_name'] = location_name
    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

def get_location_name_google(latitude, longitude):
    """
    Get location name from Google Geocoding API using coordinates
    """
    try:
        response = requests.get(
            'https://maps.googleapis.com/maps/api/geocode/json',
            params={
                'latlng': f"{latitude},{longitude}",
                'key': settings.GOOGLE_API_KEY
            }
        )
        response.raise_for_status()
        data = response.json()
        
        if data['status'] != 'OK' or not data['results']:
            return "Location not found"
            
        return data['results'][0]['formatted_address']
        
    except Exception as e:
        print(f"Geocoding error: {str(e)}")
        return "Error fetching location"


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def setup_shop_exterior_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    shop_exterior = request.data.get('shop_exterior', "")

    if not shop_id:
        errors['shop_id'] = ['Shop ID is required.']

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        errors['shop_id'] = ['Shop does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    shop = Shop.objects.get(shop_id=shop_id)
    shop.save()


    ShopExterior.objects.create(
            shop=shop,
            photo=shop_exterior
        )

    shop.shop_setup = True
    shop.save()


    if (shop.shop_registered == True and 
        shop.shop_setup == True and
        shop.service_setup == True and
        shop.payment_setup == True and
        shop.staff_setup == True
        ):
         shop.registration_complete = True
         shop.save()
    else:
        shop.registration_complete = False
        shop.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def remove_shop_exterior_view(request):
    payload = {}
    data = {}
    errors = {}

    id = request.data.get('id', '')

    if not id:
        errors['id'] = ['Shop exterior ID is required.']

    try:
        item = ShopExterior.objects.get(id=id)
    except:
        errors['id'] = ['Shop Exterior does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    item.delete()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def setup_shop_interior_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    shop_interior = request.data.get('shop_interior', "")

    if not shop_id:
        errors['shop_id'] = ['Shop ID is required.']

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        errors['shop_id'] = ['Shop does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    shop = Shop.objects.get(shop_id=shop_id)
    shop.save()


    ShopInterior.objects.create(
            shop=shop,
            photo=shop_interior
        )

    shop.shop_setup = True
    shop.save()

    if (shop.shop_registered == True and 
        shop.shop_setup == True and
        shop.service_setup == True and
        shop.payment_setup == True and
        shop.staff_setup == True
        ):
         shop.registration_complete = True
         shop.save()
    else:
        shop.registration_complete = False
        shop.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def remove_shop_interior_view(request):
    payload = {}
    data = {}
    errors = {}

    id = request.data.get('id', '')

    if not id:
        errors['id'] = ['Shop interior ID is required.']

    try:
        item = ShopInterior.objects.get(id=id)
    except:
        errors['id'] = ['Shop interior does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    item.delete()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def setup_shop_work_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    shop_work = request.data.get('shop_work', "")

    if not shop_id:
        errors['shop_id'] = ['Shop ID is required.']

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        errors['shop_id'] = ['Shop does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    shop = Shop.objects.get(shop_id=shop_id)
    shop.save()


    ShopWork.objects.create(
            shop=shop,
            photo=shop_work
        )

    shop.shop_setup = True
    shop.save()

    if (shop.shop_registered == True and 
        shop.shop_setup == True and
        shop.service_setup == True and
        shop.payment_setup == True and
        shop.staff_setup == True
        ):
         shop.registration_complete = True
         shop.save()
    else:
        shop.registration_complete = False
        shop.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def remove_shop_work_view(request):
    payload = {}
    data = {}
    errors = {}

    id = request.data.get('id', '')

    if not id:
        errors['id'] = ['Shop work ID is required.']

    try:
        item = ShopWork.objects.get(id=id)
    except:
        errors['id'] = ['Shop work does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    item.delete()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def setup_shop_view222(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    description = request.data.get('description', '')
    shop_exteriors = request.data.get('shop_exteriors', [])
    shop_interiors = request.data.get('shop_interiors', [])
    shop_works = request.data.get('shop_works', [])
    business_days = request.data.get('business_days', '')
    business_hours_open = request.data.get('business_hours_open', '')
    business_hours_close = request.data.get('business_hours_close', '')
    special_features = request.data.get('special_features', '')

    if not description:
        errors['description'] = ["Description required"]

    if not shop_id:
        errors['shop_id'] = ['Shop ID is required.']

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        errors['shop_id'] = ['Shop does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    shop = Shop.objects.get(shop_id=shop_id)
    shop.description = description
    shop.business_days = business_days
    shop.business_hours_open = business_hours_open
    shop.business_hours_close = business_hours_close
    shop.special_features = special_features

    shop.save()

    for interior in shop_interiors:
        ShopInterior.objects.create(
            shop=shop,
            photo=interior
        )

    for exterior in shop_exteriors:
        ShopExterior.objects.create(
            shop=shop,
            photo=exterior
        )

    for work in shop_works:
        ShopWork.objects.create(
            shop=shop,
            photo=work
        )

    shop.shop_setup = True
    shop.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def setup_services_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    service_type = request.data.get('service_type', '')
    category_id = request.data.get('category_id', '')
    #price = request.data.get('price', '')
    #duration = request.data.get('duration', '')
    description = request.data.get('description', '')

    if not service_type:
        errors['service_type'] = ["Services type required"]

    if not category_id:
        errors['category_id'] = ["Services category required"]

    #if not price:
    #    errors['price'] = ["Price required"]

    #if not description:
    #    errors['description'] = ["Description required"]

    # if not duration:
    #     errors['duration'] = ["Duration required"]

    if not shop_id:
        errors['shop_id'] = ['Shop ID is required.']

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        errors['shop_id'] = ['Shop does not exist.']
    try:
        category = ServiceCategory.objects.get(id=category_id)
    except:
        errors['category_id'] = ['Category does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    shop = Shop.objects.get(shop_id=shop_id)

    ShopService.objects.create(
            shop=shop,
            service_type=service_type,
            category=category,
            #price=price,
            #duration=duration,
            description=description,
        )

    shop.service_setup = True
    shop.save()

    if (shop.shop_registered == True and 
        shop.shop_setup == True and
        shop.service_setup == True and
        shop.payment_setup == True and
        shop.staff_setup == True
        ):
         shop.registration_complete = True
         shop.save()
    else:
        shop.registration_complete = False
        shop.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)








@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def setup_services_view22(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    services = request.data.get('services', '')

    if not services:
        errors['services'] = ["Services required"]

    if not shop_id:
        errors['shop_id'] = ['Shop ID is required.']

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        errors['shop_id'] = ['Shop does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    shop = Shop.objects.get(shop_id=shop_id)

    for service in services:
        ShopService.objects.create(
            shop=shop,
            service_type=service['service_type'],
            price=service['price'],
            duration=service['duration'],
            description=service['description'],
        )

    shop.service_setup = True
    shop.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def setup_staff_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    full_name = request.data.get('full_name', '')
    email = request.data.get('email', '')
    role = request.data.get('role', '')
    photo = request.data.get('photo', '')

    if not role:
        errors['role'] = ["Role name required"]

    if not full_name:
        errors['full_name'] = ["Full name required"]

    if not email:
        errors['email'] = ["Staff email required"]
    elif not is_valid_email(email):
        errors['email'] = ['Valid email required.']
    elif check_email_exist(email):
        errors['email'] = ['Email already exists in our database.']


    if not shop_id:
        errors['shop_id'] = ['Shop ID is required.']

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        errors['shop_id'] = ['Shop does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    serializer = StaffRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        data["user_id"] = user.user_id
        data["email"] = user.email
        data["full_name"] = user.full_name

        user.user_type = "Saloon Staff"
        user.save()



    shop = Shop.objects.get(shop_id=shop_id)

    ShopStaff.objects.create(
        user=user,
            shop=shop,
            staff_name=full_name,
            role=role,
        photo=photo if photo else get_default_staff_image(),  # Assign default image if no photo is provided
        )

    shop.staff_setup = True
    shop.save()

    if (shop.shop_registered == True and 
        shop.shop_setup == True and
        shop.service_setup == True and
        shop.payment_setup == True and
        shop.staff_setup == True
        ):
         shop.registration_complete = True
         shop.save()
    else:
        shop.registration_complete = False
        shop.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def edit_staff_view(request):
    payload = {}
    data = {}
    errors = {}

    staff_id = request.data.get('staff_id', '')
    full_name = request.data.get('full_name', '')
    email = request.data.get('email', '')
    role = request.data.get('role', '')
    photo = request.data.get('photo', '')

    if not staff_id:
        errors['staff_id'] = ['Staff ID is required.']

    try:
        item = ShopStaff.objects.get(staff_id=staff_id)
    except:
        errors['staff_id'] = ['Staff does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)
    
    if photo:
        item.photo = photo
    if full_name:
        item.full_name = full_name
    if email:
        item.email = email
    if role:
        item.role = role
    item.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def remove_staff_photo_view(request):
    payload = {}
    data = {}
    errors = {}

    staff_id = request.data.get('staff_id', '')

    if not staff_id:
        errors['staff_id'] = ['Staff ID is required.']

    try:
        item = ShopStaff.objects.get(staff_id=staff_id)
    except:
        errors['staff_id'] = ['Staff does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    item.photo = None
    item.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)





@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def setup_staff_view222222(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    staffs = request.data.get('staffs', '')

    if not staffs:
        errors['staffs'] = ["Staffs required"]

    if not shop_id:
        errors['shop_id'] = ['Shop ID is required.']

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        errors['shop_id'] = ['Shop does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    shop = Shop.objects.get(shop_id=shop_id)

    for staff in staffs:
        ShopStaff.objects.create(
            shop=shop,
            staff_name=staff['staff_name'],
            role=staff['role'],
            photo=staff['photo'],
        )

    shop.staff_setup = True
    shop.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def setup_payment_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    platform = request.data.get('platform', '')
    public_api_key = request.data.get('public_api_key', '')
    reservation_policy_value = request.data.get('reservation_policy_value', 0)
    reservation_policy_description = request.data.get('reservation_policy_description', '')
    cancellation_policy_value = request.data.get('cancellation_policy_value', 0)
    cancellation_policy_description = request.data.get('cancellation_policy_description', '')

    # Validate required fields
    if not platform:
        errors['platform'] = ["Platform required"]

    if not shop_id:
        errors['shop_id'] = ['Shop ID is required.']

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        errors['shop_id'] = ['Shop does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    # Check if PaymentSetup exists for the shop, if yes, update it, else create a new one
    payment_setup, created = PaymentSetup.objects.update_or_create(
        shop=shop,
        defaults={
            'platform': platform,
            'public_api_key': public_api_key,
            'reservation_policy_value': reservation_policy_value,
            'reservation_policy_description': reservation_policy_description,
            'cancellation_policy_value': cancellation_policy_value,
            'cancellation_policy_description': cancellation_policy_description,
        }
    )

    # Set the payment_setup flag to True on the shop
    shop.payment_setup = True
    shop.save()

    # Check if the shop's registration is complete based on the setup flags
    if (shop.shop_registered and 
        shop.shop_setup and
        shop.service_setup and
        shop.payment_setup and
        shop.staff_setup):
        shop.registration_complete = True
        shop.save()
    else:
        shop.registration_complete = False
        shop.save()

    # Prepare the response data
    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def remove_staff_view(request):
    payload = {}
    data = {}
    errors = {}

    staff_id = request.data.get('staff_id', '')

    if not staff_id:
        errors['staff_id'] = ['Staff ID is required.']

    try:
        staff = ShopStaff.objects.get(staff_id=staff_id)
    except:
        errors['staff_id'] = ['Staff does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    staff.delete()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def remove_service_view(request):
    payload = {}
    data = {}
    errors = {}

    service_id = request.data.get('service_id', '')

    if not service_id:
        errors['service_id'] = ['Service ID is required.']

    try:
        service = ShopService.objects.get(service_id=service_id)
    except:
        errors['service_id'] = ['Service does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    service.delete()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def remove_package_view(request):
    payload = {}
    data = {}
    errors = {}

    package_id = request.data.get('package_id', '')

    if not package_id:
        errors['package_id'] = ['Package ID is required.']

    try:
        package = ShopPackage.objects.get(id=package_id)
    except:
        errors['package_id'] = ['Package does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    package.delete()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_package_view(request):
    payload = {}
    data = {}
    errors = {}

    service_id = request.data.get('service_id', '')
    package_name = request.data.get('package_name', '')
    price = request.data.get('price', '')
    duration = request.data.get('duration', '')
    photo = request.data.get('photo', None)  # Make sure to check for None, not just absence

    # Validation checks
    if not package_name:
        errors['package_name'] = ["Package Name required."]
    if not price:
        errors['price'] = ["Price required."]
    if not service_id:
        errors['service_id'] = ['Service ID is required.']

    # Check if the service exists
    try:
        service = ShopService.objects.get(service_id=service_id)
    except ShopService.DoesNotExist:
        errors['service_id'] = ['Service does not exist.']

    # Return errors if any
    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    # Create ShopPackage with default photo if none is provided
    package = ShopPackage.objects.create(
        service=service,
        package_name=package_name,
        duration=duration,
        price=price,
        photo=photo if photo else get_default_package_image(),  # Assign default image if no photo is provided
    )

    payload['message'] = "Successful"
    payload['data'] = {
        'package_name': package.package_name,
        'price': package.price,
        'duration': package.duration,
        'photo': package.photo.url,  # Assuming you're using a media URL for the photo
    }

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def edit_package_view(request):
    payload = {}
    data = {}
    errors = {}

    package_id = request.data.get('package_id', '')
    package_name = request.data.get('package_name', '')
    price = request.data.get('price', '')
    photo = request.data.get('photo', '')

    if not package_id:
        errors['package_id'] = ['Package ID is required.']

    try:
        package = ShopPackage.objects.get(id=package_id)
    except:
        errors['package_id'] = ['Package does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)
    
    if package_name:
        package.package_name = package_name
    if price:
        package.price = price
    if photo:
        package.photo = photo
    package.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_package_view22(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    packages = request.data.get('packages', '')

    if not packages:
        errors['packages'] = ["Add at least one package required"]

    if not shop_id:
        errors['shop_id'] = ['Shop ID is required.']

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        errors['shop_id'] = ['Shop does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    shop = Shop.objects.get(shop_id=shop_id)

    for package in packages:
        ShopPackage.objects.create(
            shop=shop,
            package_name=package['package_name'],
            price=package['price'],
            photo=package['photo'],

        )

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def list_all_shops_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    service_category = request.query_params.get('service_category', '')
    page_size = 10

    shops = Shop.objects.filter(registration_complete=True)

    if search_query:
        shops = shops.filter(
            Q(shop_name__icontains=search_query) |
            Q(shop_services__service_type__icontains=search_query) 

        ).distinct() 


        # Filter by service category if provided
    if service_category:
        shops = shops.filter(
            shop_services__category__name__icontains=service_category
        ).distinct()

    paginator = Paginator(shops, page_size)

    try:
        paginated_shops = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_shops = paginator.page(1)
    except EmptyPage:
        paginated_shops = paginator.page(paginator.num_pages)

    shops_serializer = ListShopsSerializer(paginated_shops, many=True)

    data['shops'] = shops_serializer.data
    data['pagination'] = {
        'page_number': paginated_shops.number,
        'total_pages': paginator.num_pages,
        'next': paginated_shops.next_page_number() if paginated_shops.has_next() else None,
        'previous': paginated_shops.previous_page_number() if paginated_shops.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def list_all_nearby_shops_view(request):
    payload = {}
    data = {}
    errors = {}

    user_id = request.query_params.get('user_id', '')
    radius = int(request.query_params.get('radius', 0.0))
    #radius = 15


    if not user_id:
        errors['user_id'] = ["User ID required"]

    try:
        user = User.objects.get(user_id=user_id)  # Use 'id' instead of 'user_id'
    except User.DoesNotExist:
        errors['user_id'] = ['User does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    nearby_shops = []
    all_shops = Shop.objects.filter(registration_complete=True)

    for shop in all_shops:
        #print('################')
        #print('################')
        #print('################')
        #print(user.lng)
        #print(user.lat)
        #print(shop.lng)
        #print(shop.lat)

        distance = haversine(user.lng, user.lat, shop.lng, shop.lat)

        
        if distance <= radius:
            # Create a dictionary for each shop
            nearby_shops.append({
                "shop_name": shop.shop_name,
                "shop_id": shop.shop_id,
                 "location": shop.location_name,
                "lat": shop.lat,
                "lng": shop.lng,
                "distance": distance,
                "photo": shop.photo.url

            })

    # Sort the shops by distance
    nearby_shops.sort(key=lambda x: x['distance'])

    data['nearest_shops'] = nearby_shops

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def shop_details_view(request):
    payload = {}
    errors = {}

    shop_id = request.query_params.get('shop_id')
    user_id = request.query_params.get('user_id')

    if not shop_id:
        errors['shop_id'] = ["Shop id required"]
        return Response({"message": "Errors", "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        errors['shop_id'] = ['Shop does not exist.']
        return Response({"message": "Errors", "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

    if user_id:
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            errors['user_id'] = ['User does not exist.']
            return Response({"message": "Errors", "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        user_visit = ShopVisit.objects.create(client=user, shop=shop)
        user_visit.save()

    shop_detail_serializer = ShopDetailSerializer(shop, many=False)
    
    payload['message'] = "Successful"
    payload['data'] = shop_detail_serializer.data

    return Response(payload, status=status.HTTP_200_OK)

@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_staffs_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.query_params.get('shop_id', None)
    
    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    if not shop_id:
        errors['shop_id'] = ['Shop ID is required.']

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        errors['shop_id'] = ['Shop does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    staffs = ShopStaff.objects.filter(shop=shop).order_by('-created_at')

    if search_query:
        staffs = staffs.filter(
            Q(staff_name__icontains=search_query) | 
            Q(staff_id__icontains=search_query))

    paginator = Paginator(staffs, page_size)

    try:
        paginated_staffs = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_staffs = paginator.page(1)
    except EmptyPage:
        paginated_staffs = paginator.page(paginator.num_pages)

    staffs_serializer = ShopStaffSerializer(paginated_staffs, many=True)

    data['staffs'] = staffs_serializer.data
    data['pagination'] = {
        'page_number': paginated_staffs.number,
        'total_pages': paginator.num_pages,
        'next': paginated_staffs.next_page_number() if paginated_staffs.has_next() else None,
        'previous': paginated_staffs.previous_page_number() if paginated_staffs.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def staff_details_view(request):
    payload = {}
    data = {}
    errors = {}

    staff_id = request.query_params.get('staff_id', None)

    if not staff_id:
        errors['staff_id'] = ["Staff id required"]

    try:
        staff = ShopStaff.objects.get(staff_id=staff_id)
    except ShopStaff.DoesNotExist:
        errors['staff_id'] = ['Staff does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    staff_detail = ShopStaff.objects.get(staff_id=staff_id)

    staff_detail_serializer = ShopStaffSerializer(staff_detail, many=False)
    if staff_detail_serializer:
        _staff = staff_detail_serializer.data

    payload['message'] = "Successful"
    payload['data'] = _staff

    return Response(payload, status=status.HTTP_200_OK)





from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_services_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.query_params.get('shop_id', None)
    
    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    if not shop_id:
        errors['shop_id'] = ['Shop ID is required.']

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        errors['shop_id'] = ['Shop does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    services = ShopService.objects.filter(shop=shop).order_by('-created_at')

    if search_query:
        services = services.filter(
            Q(service_id__icontains=search_query) |
            Q(service_type__icontains=search_query)
        )

    paginator = Paginator(services, page_size)

    try:
        paginated_services = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_services = paginator.page(1)
    except EmptyPage:
        paginated_services = paginator.page(paginator.num_pages)

    services_serializer = ShopServiceDetailSerializer(paginated_services, many=True)

    data['services'] = services_serializer.data
    data['pagination'] = {
        'page_number': paginated_services.number,
        'total_pages': paginator.num_pages,
        'next': paginated_services.next_page_number() if paginated_services.has_next() else None,
        'previous': paginated_services.previous_page_number() if paginated_services.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)





@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_service_categories_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 100

    categories = ServiceCategory.objects.all()

    if search_query:
        categories = categories.filter(Q(name__icontains=search_query))

    paginator = Paginator(categories, page_size)

    try:
        paginated_categories = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_categories = paginator.page(1)
    except EmptyPage:
        paginated_categories = paginator.page(paginator.num_pages)

    categories_serializer = ServiceCategorySerializer(paginated_categories, many=True)

    data['service_categories'] = categories_serializer.data
    data['pagination'] = {
        'page_number': paginated_categories.number,
        'total_pages': paginator.num_pages,
        'next': paginated_categories.next_page_number() if paginated_categories.has_next() else None,
        'previous': paginated_categories.previous_page_number() if paginated_categories.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_package_view(request):
    payload = {}
    data = {}
    errors = {}

    service_id = request.query_params.get('service_id', None)
    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    if not service_id:
        errors['service_id'] = ['Service ID is required.']

    try:
        service = ShopService.objects.get(service_id=service_id)
    except ShopService.DoesNotExist:
        errors['service_id'] = ['Service does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)



    packages = ShopPackage.objects.filter(service=service)

    if search_query:
        packages = packages.filter(

            Q(package_name__icontains=search_query)
        )

    paginator = Paginator(packages, page_size)

    try:
        paginated_packages = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_packages = paginator.page(1)
    except EmptyPage:
        paginated_packages = paginator.page(paginator.num_pages)

    packages_serializer = ShopPackageSerializer(paginated_packages, many=True)

    data['packages'] = packages_serializer.data
    data['pagination'] = {
        'page_number': paginated_packages.number,
        'total_pages': paginator.num_pages,
        'next': paginated_packages.next_page_number() if paginated_packages.has_next() else None,
        'previous': paginated_packages.previous_page_number() if paginated_packages.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def package_details_view(request):
    payload = {}
    data = {}
    errors = {}

    package_id = request.query_params.get('package_id', None)

    if not package_id:
        errors['package_id'] = ["Package id required"]

    try:
        package = ShopPackage.objects.get(id=package_id)
    except ShopPackage.DoesNotExist:
        errors['package_id'] = ['Package does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    package_detail = ShopPackage.objects.get(id=package_id)

    package_id_serializer = ShopPackageSerializer(package_detail, many=False)
    if package_id_serializer:
        _package = package_id_serializer.data

    payload['message'] = "Successful"
    payload['data'] = _package

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def remove_shop_view(request):

    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        shop_id = request.data.get('shop_id', "")


        if not shop_id:
            errors['shop_id'] = ['Shop ID is required.']

        try:
            shop = Shop.objects.get(shop_id=shop_id)
        except:
            errors['shop_id'] = ['Shop does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        shop.is_deleted = True
        shop.save()

        shop.user.is_deleted = True
        shop.user.save()
        shop.save()

        new_activity = AllActivity.objects.create(
            user=shop.user,
            subject="Shop Removed",
            body=shop.user.email + " Just deleted their shop. " + shop.shop_name
        )
        new_activity.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def setup_services_staff_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    staff_ids = request.data.get('staff_id', [])
    service_id = request.data.get('service_id', '')


    if not service_id:
        errors['service_id'] = ["Services ID required"]

    if not staff_ids:
        errors['staff_ids'] = ["Staff IDs required"]


    if not shop_id:
        errors['shop_id'] = ['Shop ID is required.']

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        errors['shop_id'] = ['Shop does not exist.']



    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    shop = Shop.objects.get(shop_id=shop_id)

    shop_service = ShopService.objects.get(
            service_id=service_id
        )


    for staff_id in staff_ids:
        staff = ShopStaff.objects.get(staff_id=staff_id)
        ServiceSpecialist.objects.create(
            service=shop_service,
            specialist=staff
        )




    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


def check_shop_name_exist(full_name):
    qs = User.objects.filter(full_name=full_name)
    if qs.exists():
        return True
    else:
        return False


def check_email_exist(email):
    qs = User.objects.filter(email=email)
    if qs.exists():
        return True
    else:
        return False


def is_valid_email(email):
    # Regular expression pattern for basic email validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # Using re.match to check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False


def is_valid_password(password):
    # Check for at least 8 characters
    if len(password) < 8:
        return False

    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False

    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False

    # Check for at least one digit
    if not re.search(r'[0-9]', password):
        return False

    # Check for at least one special character
    if not re.search(r'[-!@#\$%^&*_()-+=/.,<>?"~`£{}|:;]', password):
        return False

    return True

from django.utils.dateparse import parse_time

@api_view(['POST'])
@permission_classes([])  # Add permission classes as needed
@authentication_classes([])  # Add authentication classes as needed
def set_or_update_shop_availability(request):
    payload = {}
    errors = {}

    # Extract the payload data
    shop_id = request.data.get('shop_id', "")
    availability_data = request.data.get('availability', [])

    if not shop_id:
        errors['shop_id'] = ['Shop ID is required.']

    if not availability_data:
        errors['availability'] = ['Availability data is required.']

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        errors['shop_id'] = ['Shop does not exist.']



    # If there are any validation errors, return them
    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    # Loop through availability data and create or update ShopAvailability entries
    for availability in availability_data:
        day = availability.get('day')
        open_time = availability.get('open')
        closed_time = availability.get('closed')

        if day not in dict(ShopAvailability.DAYS_OF_THE_WEEK).keys():
            errors['availability'] = ['Invalid day provided.']

        # Time format validation
        try:
            if open_time != "Closed":
                open_time = datetime.strptime(open_time, "%H:%M").time()
            if closed_time != "Closed":
                closed_time = datetime.strptime(closed_time, "%H:%M").time()
        except ValueError:
            errors['availability'] = ['Invalid time format for open or closed time.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        # Create or update the availability record
        availability_instance, created = ShopAvailability.objects.update_or_create(
            shop=shop,
            day=day,
            defaults={'open_time': open_time if open_time != "Closed" else None, 
                      'closed_time': closed_time if closed_time != "Closed" else None,
                      'active': True}  # You can modify the 'active' field as needed
        )

    # Success response
    payload['message'] = "Availability added or updated successfully"
    payload['data'] = {
        'shop_id': shop_id,
        'availability': availability_data,
    }

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def set_shop_availability(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        shop_id = request.data.get('shop_id', "")
        availability = request.data.get('availability', [])

        if not shop_id:
            errors['shop_id'] = ['Shop ID is required.']

        if not availability:
            errors['availability'] = ['Availability is required.']

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

        for slot in availability:
            date_str = slot.get('date', "")
            open_time_str = slot.get('open', "")
            closed_time_str = slot.get('closed', "")

            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                open_time = datetime.strptime(open_time_str, "%H:%M").time()
                closed_time = datetime.strptime(closed_time_str, "%H:%M").time()
            except ValueError:
                errors['availability'] = ['Invalid date or time format.']
                payload['message'] = "Errors"
                payload['errors'] = errors
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

            # Check if a shop availability already exists for the date
            existing_availability = ShopAvailability.objects.filter(shop=shop, date=date)
            if existing_availability.exists():
                # Update the existing availability
                shop_availability = existing_availability.first()
                shop_availability.open = open_time
                shop_availability.closed = closed_time
                shop_availability.save()
            else:
                # Create a new shop availability
                shop_availability = ShopAvailability.objects.create(
                    shop=shop,
                    date=date,
                    open=open_time,
                    closed=closed_time
                )

            # Add the shop availability data to the response
            data[date_str] = {
                "open": shop_availability.open.strftime("%H:%M"),
                "closed": shop_availability.closed.strftime("%H:%M")
            }

        payload['message'] = "Slot added or updated successfully"
        payload['data'] = data

        return Response(payload)



@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def list_shop_availability(request):
    payload = {}
    data = {}

    errors = {}

    if request.method == 'POST':
        shop_id = request.data.get('shop_id', "")

        if not shop_id:
            errors['shop_id'] = ['Shop ID is required.']

        try:
            shop = Shop.objects.get(shop_id=shop_id)
        except Shop.DoesNotExist:
            errors['shop_id'] = ['Shop does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        availabilities = ShopAvailability.objects.filter(shop=shop)
        serializer = ShopAvailabilitySerializer(availabilities, many=True)
        data["shop_availability"] = serializer.data

        payload['message'] = "Successful"
        payload['data'] = data
        return Response(payload)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def shop_visit_count_view(request):
    shop_id = request.query_params.get('shop_id')
    period = request.query_params.get('period', 'all')

    if not shop_id:
        return Response({"message": "Error", "errors": {"shop_id": ["Shop id required"]}}, 
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        return Response({"message": "Error", "errors": {"shop_id": ["Shop does not exist"]}}, 
                        status=status.HTTP_404_NOT_FOUND)

    now = timezone.now()
    if period == 'daily':
        start_date = now - timedelta(days=1)
    elif period == 'weekly':
        start_date = now - timedelta(weeks=1)
    elif period == 'monthly':
        start_date = now - timedelta(days=30)
    elif period == 'yearly':
        start_date = now - timedelta(days=365)
    else:  # 'all'
        start_date = None

    # Query the ShopVisit table for visits related to the shop
    queryset = ShopVisit.objects.filter(shop=shop)
    if start_date:
        queryset = queryset.filter(updated_at__gte=start_date)

    # Aggregate visit counts (total visits and unique visitors)
    visit_counts = queryset.aggregate(
        total_visits=Count('id'),
        unique_visitors=Count('client', distinct=True)
    )

    # Get the unique visitors and their visit counts
    visitors_data = []
    unique_visitors_queryset = queryset.values('client').annotate(visit_count=Count('client')).distinct()  # Get unique clients with their visit count

    for visit in unique_visitors_queryset:
        client = User.objects.get(id=visit['client'])  # Fetch the user data efficiently
        visitors_data.append({
            'user_id': client.user_id,
            'email': client.email,
            'photo': client.personal_info.photo.url if client.personal_info else None,
            'full_name': client.full_name,
            'visit_count': visit['visit_count'],  # Add visit count for each client
        })

    response_data = {
        "shop_id": shop_id,
        "shop_name": shop.shop_name,
        "period": period,
        "total_visits": visit_counts['total_visits'],
        "unique_visitors": visit_counts['unique_visitors'],
        "visitors_data": visitors_data  # Include user details and visit count
    }

    return Response({"message": "Successful", "data": response_data}, status=status.HTTP_200_OK)







@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def shop_visit_count_view2222(request):
    shop_id = request.query_params.get('shop_id')
    period = request.query_params.get('period', 'all')

    if not shop_id:
        return Response({"message": "Error", "errors": {"shop_id": ["Shop id required"]}}, 
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        return Response({"message": "Error", "errors": {"shop_id": ["Shop does not exist"]}}, 
                        status=status.HTTP_404_NOT_FOUND)

    now = timezone.now()
    if period == 'daily':
        start_date = now - timedelta(days=1)
    elif period == 'weekly':
        start_date = now - timedelta(weeks=1)
    elif period == 'monthly':
        start_date = now - timedelta(days=30)
    elif period == 'yearly':
        start_date = now - timedelta(days=365)
    else:  # 'all'
        start_date = None

    queryset = ShopVisit.objects.filter(shop=shop)
    if start_date:
        queryset = queryset.filter(updated_at__gte=start_date)

    visit_counts = queryset.aggregate(
        total_visits=Count('id'),
        unique_visitors=Count('client', distinct=True)
    )

    response_data = {
        "shop_id": shop_id,
        "shop_name": shop.shop_name,
        "period": period,
        "total_visits": visit_counts['total_visits'],
        "unique_visitors": visit_counts['unique_visitors']
    }

    return Response({"message": "Successful", "data": response_data}, status=status.HTTP_200_OK)