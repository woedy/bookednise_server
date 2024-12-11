from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from bookings.api.serializers import ListBookingSerializer
from bookings.models import Booking
from user_profile.models import UserProfile

User = get_user_model()


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_user_profile_view(request):
    payload = {}
    data = {}
    user_data = {}
    all_bookings = []

    user_id = request.query_params.get('user_id', None)

    user = User.objects.get(user_id=user_id)
    personal_info = UserProfile.objects.get(user=user)

    bookings = Booking.objects.filter(client=user).order_by("-created_at")



    user_data['user_id'] = user.user_id
    user_data['email'] = user.email
    user_data['full_name'] = user.full_name

    user_data['photo'] = personal_info.photo.url
    user_data['phone'] = personal_info.phone
    user_data['country'] = personal_info.country
    user_data['bookings_count'] = bookings.count()
    data['user_data'] = user_data



    _bookings = Booking.objects.filter(client=user).order_by('-created_at')
    booking_serializer = ListBookingSerializer(_bookings, many=True)
    if booking_serializer:
        all_bookings = booking_serializer.data


    data['bookings'] = all_bookings

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def update_user_profile_view(request):
    payload = {}
    errors = {}

    user_id = request.data.get('user_id')
    email = request.data.get('email')
    full_name = request.data.get('full_name')
    phone = request.data.get('phone')
    address = request.data.get('address')
    gender = request.data.get('gender')
    dob = request.data.get('dob')
    photo = request.data.get('photo')
    
    # Check if user_id is provided
    if not user_id:
        errors['user_id'] = ['User ID is required.']
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    # Try to retrieve the user
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        errors['user_id'] = ['User does not exist.']
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_404_NOT_FOUND)

    # Update user fields if provided
    if email is not None:
        user.email = email.lower()
    if full_name is not None:
        user.full_name = full_name
    user.save()

    try:
        token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        token = Token.objects.create(user=user)

    # Update or create UserProfile if exists
    try:
        personal_info, created = UserProfile.objects.get_or_create(user=user)
        if phone is not None:
            personal_info.phone = phone
        if address is not None:
            personal_info.address = address
        if gender is not None:
            personal_info.gender = gender
        if dob is not None:
            personal_info.dob = dob
        if photo is not None:
            personal_info.photo = photo
        personal_info.save()
    except Exception as e:
        payload['message'] = "Failed to update profile information"
        payload['errors'] = {"profile": [str(e)]}
        return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Prepare response data
    data = {
        'user_id': user.user_id,
        'email': user.email,
        'full_name': user.full_name,
        'token': token.key,
        'phone': personal_info.phone,
        'address': personal_info.address,
        'gender': personal_info.gender,
        'dob': personal_info.dob,
        'country': personal_info.country,
        'photo': personal_info.photo.url if personal_info.photo else None
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)