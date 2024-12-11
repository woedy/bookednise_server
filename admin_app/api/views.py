from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate

from activities.models import AllActivity
from admin_app.api.serializers import ListAdminShopsSerializer, ListAdminAllUsersSerializer, AdminUserDetailSerializer
from bookings.api.serializers import ListBookingAdminSerializer, BookingRatingSerializer
from bookings.models import Booking, BookingRating
from shop.api.serializers import ShopDetailSerializer
from shop.models import Shop
from django.db.models import Count

User = get_user_model()

@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def overview_view(request):
    payload = {}
    data = {}
    errors = {}

    vendors_count = 0
    all_users_count = 0
    all_appointments_count = 0
    stats_data = {}

    all_shops = Shop.objects.all().filter(registration_complete=True).filter(is_deleted=False)
    vendors_count = all_shops.count()

    all_users = User.objects.all().filter(user_type="Client").filter(is_deleted=False)
    all_users_count = all_users.count()

    all_bookings = Booking.objects.all()
    all_appointments_count = all_bookings.count()


    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    data['vendors_count'] = vendors_count
    data['all_users_count'] = all_users_count
    data['all_appointments_count'] = all_appointments_count
    data['stats_data'] = stats_data





    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def list_all_shops_admin_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    # Assuming the Shop model has fields 'registration_complete' and 'is_deleted'
    shops = Shop.objects.filter(registration_complete=True, is_deleted=False)

    if search_query:
        shops = shops.filter(
            Q(shop_name__icontains=search_query) |
                        Q(shop_services__service_type__icontains=search_query) 

            ).distinct()

    paginator = Paginator(shops, page_size)

    try:
        paginated_shops = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_shops = paginator.page(1)
    except EmptyPage:
        paginated_shops = paginator.page(paginator.num_pages)

    shops_serializer = ListAdminShopsSerializer(paginated_shops, many=True)

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


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def admin_shop_details_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.query_params.get('shop_id', None)

    if not shop_id:
        errors['shop_id'] = ["Shop id required"]

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        errors['shop_id'] = ['Shop does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    shop_detail = Shop.objects.get(shop_id=shop_id)

    shop_detail_serializer = ShopDetailSerializer(shop_detail, many=False)
    if shop_detail_serializer:
        _shop = shop_detail_serializer.data

    payload['message'] = "Successful"
    payload['data'] = _shop

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def remove_vendor_view(request):

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
            body="Admin Just deleted shop. " + shop.shop_name
        )
        new_activity.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def list_all_users_admin_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    all_users = User.objects.all().filter(is_deleted=False).annotate(bookings_count=Count('shop_service_bookings'))

    if search_query:
        all_users = all_users.filter(Q(full_name__icontains=search_query) | Q(email__icontains=search_query))

    paginator = Paginator(all_users, page_size)

    try:
        paginated_users = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_users = paginator.page(1)
    except EmptyPage:
        paginated_users = paginator.page(paginator.num_pages)

    users_serializer = ListAdminAllUsersSerializer(paginated_users, many=True)

    data['all_users'] = users_serializer.data
    data['pagination'] = {
        'page_number': paginated_users.number,
        'total_pages': paginator.num_pages,
        'next': paginated_users.next_page_number() if paginated_users.has_next() else None,
        'previous': paginated_users.previous_page_number() if paginated_users.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def admin_user_details_view(request):
    payload = {}
    data = {}
    errors = {}

    user_id = request.query_params.get('user_id', None)

    if not user_id:
        errors['user_id'] = ["User id required"]

    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        errors['user_id'] = ['User does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    user_detail = User.objects.prefetch_related('shop_service_bookings').get(user_id=user_id)

    user_detail_serializer = AdminUserDetailSerializer(user_detail, many=False)
    if user_detail_serializer:
        _user = user_detail_serializer.data

    payload['message'] = "Successful"
    payload['data'] = _user

    return Response(payload, status=status.HTTP_200_OK)





@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def remove_user_view(request):

    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")


        if not user_id:
            errors['user_id'] = ['User ID is required.']

        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        user.is_deleted = True
        user.save()

        new_activity = AllActivity.objects.create(
            user=user,
            subject="User Removed",
            body="Admin Just deleted user. " + user.full_name
        )
        new_activity.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def list_all_bookings_admin_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    shop_id = request.query_params.get('shop_id', '')
    _status = request.query_params.get('status', '')
    date = request.query_params.get('date', '')
    page_size = 10

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    all_bookings = Booking.objects.all()

    if search_query:
        all_bookings = all_bookings.filter(Q(booking_id__icontains=search_query) |
        Q(service_type__icontains=search_query) |
        Q(client__full_name__icontains=search_query) |
        Q(client__email__icontains=search_query))
    if shop_id:
        all_bookings = all_bookings.filter(shop__shop_id=shop_id)


    if _status:
        all_bookings = all_bookings.filter(status=_status)

    if date:
        all_bookings = all_bookings.filter(booking_date=date)

    paginator = Paginator(all_bookings, page_size)

    try:
        paginated_bookings = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_bookings = paginator.page(1)
    except EmptyPage:
        paginated_bookings = paginator.page(paginator.num_pages)

    bookings_serializer = ListBookingAdminSerializer(paginated_bookings, many=True)

    data['bookings'] = bookings_serializer.data
    data['pagination'] = {
        'page_number': paginated_bookings.number,
        'total_pages': paginator.num_pages,
        'next': paginated_bookings.next_page_number() if paginated_bookings.has_next() else None,
        'previous': paginated_bookings.previous_page_number() if paginated_bookings.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def remove_booking_view(request):

    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        booking_id = request.data.get('booking_id', "")


        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking_id'] = ['Booking does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        booking.delete()

        new_activity = AllActivity.objects.create(
            user=User.objects.get(id=1),
            subject="Booking Removed",
            body="Admin Just deleted booking. "
        )
        new_activity.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def list_all_bookings_review_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    all_bookings_ratings = BookingRating.objects.all()

    if search_query:
        all_bookings_ratings = all_bookings_ratings.filter(Q(booking__booking_id__icontains=search_query) |
                                                             Q(booking__client__email__icontains=search_query))

    paginator = Paginator(all_bookings_ratings, page_size)

    try:
        paginated_ratings = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_ratings = paginator.page(1)
    except EmptyPage:
        paginated_ratings = paginator.page(paginator.num_pages)


    ratings_data = []
    for rating in paginated_ratings:
        bookings = Booking.objects.filter(client=rating.booking.client)

        rating_data = {
            'service_id': rating.booking.service.service_id,
            'service_type': rating.booking.service.service_type,
            'client_name': rating.booking.client.full_name,
            'photo': rating.booking.client.personal_info.photo.url,
            'client_email': rating.booking.client.email,
            'contact': rating.booking.client.personal_info.phone,
            'shop_name': rating.booking.shop.shop_name,
            'rating': rating.rating,
            'report': rating.report,
            'bookings_count': bookings.count(),

        }
        ratings_data.append(rating_data)

    data['ratings'] = ratings_data
    data['pagination'] = {
        'page_number': paginated_ratings.number,
        'total_pages': paginator.num_pages,
        'next': paginated_ratings.next_page_number() if paginated_ratings.has_next() else None,
        'previous': paginated_ratings.previous_page_number() if paginated_ratings.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)
