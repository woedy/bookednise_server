
from decimal import Decimal
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from bookings.api.serializers import BookingSerializer, ListBookingSerializer
from bookings.models import Booking
from shop.api.serializers import AllShopPackagePromotionsSerializer, AllShopPromotionsSerializer, ListShopsSerializer, ShopServiceSerializer, ShopStaffSerializer
from shop.models import ServiceCategory, Shop, ShopPackagePromotion, ShopPromotion, ShopService, ShopStaff
from django.db.models import Count


User = get_user_model()

@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def shop_homepage_view(request):
    payload = {}
    data = {}
    user_data = {}
    errors = {}

    shop_info = {}
    bookings_today = []
    shop_categories = []
    shop_staffs = []


    shop_id = request.query_params.get('shop_id', None)

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


    shop_info['shop_name'] = shop.shop_name
    shop_info['location_name'] = shop.location_name

    service = ShopService.objects.filter(shop=shop)
    service_serializer = ShopServiceSerializer(service, many=True)
    if service_serializer:
        shop_categories = service_serializer.data

    staff = ShopStaff.objects.filter(shop=shop)
    staff_serializer = ShopStaffSerializer(staff, many=True)
    if staff_serializer:
        shop_staffs = staff_serializer.data

    _bookings = Booking.objects.filter(shop=shop).order_by('-created_at')
    booking_serializer = ListBookingSerializer(_bookings, many=True)
    if booking_serializer:
        bookings_today = booking_serializer.data

    data['shop_info'] = shop_info
    data['bookings_today'] = bookings_today
    data['shop_categories'] = shop_categories
    data['shop_staffs'] = shop_staffs




    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)






@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def client_homepage_view(request):
    payload = {}
    data = {}
    user_data = {}
    errors = {}

    shop_info = {}
    bookings_today = []
    service_categories = []
    shop_staffs = []
    promotions = []



    user_id = request.query_params.get('user_id', None)
    lat = request.query_params.get('lat', 5.6222924)
    lng = request.query_params.get('lng', -0.173371561)

    print('###############################')
    print(lat)
    print(lng)


    if not user_id:
        errors['user_id'] = ['User ID is required.']

    if not lat:
        errors['lat'] = ['User latitude is required.']

    if not lng:
        errors['lng'] = ['User longitude is required.']

    try:
        user = User.objects.get(user_id=user_id)
    except:
        errors['user_id'] = ['User does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)
    
    if lat == 0.0 and lng == 0.0:
        user.lat = Decimal(lat)
        user.lng = Decimal(lng)
        user.save()
    else:
        user.lat = 5.6222924
        user.lng = -0.173371561
        user.save() 

    _bookings = Booking.objects.filter(client=user).filter(status="Pending").order_by('-created_at')
    booking_serializer = ListBookingSerializer(_bookings, many=True)
    if booking_serializer:
        bookings_today = booking_serializer.data

    data['bookings'] = bookings_today


    cats = ShopService.objects.all()
    for cat in cats:
        obj = {
            'service_type': cat.service_type,
            'service_image': 'image'
        }
        service_categories.append(obj)
    data['service_categories'] = service_categories


    promos = ShopPromotion.objects.all().order_by('-created_at')
    all_promotions_serializer = AllShopPromotionsSerializer(promos, many=True)
    _promotions = all_promotions_serializer.data
    data['promotions'] = _promotions



    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def client_homepage_new_view(request):
    payload = {}
    data = {}
    user_data = {}
    errors = {}

    shop_info = {}
    bookings_today = []
    bookings_history = []
    service_categories = []
    shop_staffs = []

    user_id = request.query_params.get('user_id', None)
    lat = Decimal(request.query_params.get('lat', 0.0))
    lng = Decimal(request.query_params.get('lng', 0.0))

    if not user_id:
        errors['user_id'] = ['User ID is required.']

    if not lat:
        errors['lat'] = ['User latitude is required.']

    if not lng:
        errors['lng'] = ['User longitude is required.']

    try:
        user = User.objects.get(user_id=user_id)
    except:
        errors['user_id'] = ['User does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    user.lat = Decimal(lat)
    user.lng = Decimal(lng)
    user.save()

    # Get bookings for today
    _bookings = Booking.objects.filter(client=user).filter(status="Pending").order_by('-created_at')[:10]
    booking_serializer = ListBookingSerializer(_bookings, many=True)
    if booking_serializer:
        bookings_today = booking_serializer.data
        upcoming = bookings_today

    # Get booking history
    __bookings = Booking.objects.filter(client=user, status__in=["Complete", "Cancelled"]).order_by('-created_at')[:10]
    booking_serializer = ListBookingSerializer(__bookings, many=True)
    if booking_serializer:
        history_data = booking_serializer.data
        history = history_data

    bookings = {
        'upcoming': upcoming,
        'history': history,
    }

    data['bookings'] = bookings

    # Get service categories
    cats = ServiceCategory.objects.all()
    for cat in cats:
        obj = {
            'id': cat.id,
            'name': cat.name,
            'photo': cat.photo.url
        }
        service_categories.append(obj)
    data['service_categories'] = service_categories

    # Fetch promoted services
    pack_promos = ShopPackagePromotion.objects.all().order_by('-created_at')[:10]
    all_promotions_serializer = AllShopPackagePromotionsSerializer(pack_promos, many=True)
    promoted_services = all_promotions_serializer.data

    # Fetch Gold, Silver, Bronze promotions
    gold_promos = ShopPromotion.objects.all().filter(level='Gold').order_by('-created_at')[:10]
    gold_promos_promotions_serializer = AllShopPromotionsSerializer(gold_promos, many=True)
    gold_promos = gold_promos_promotions_serializer.data

    silver_promos = ShopPromotion.objects.all().filter(level='Silver').order_by('-created_at')[:10]
    silver_promos_promotions_serializer = AllShopPromotionsSerializer(silver_promos, many=True)
    silver_promos = silver_promos_promotions_serializer.data

    bronze_promos = ShopPromotion.objects.all().filter(level='Bronze').order_by('-created_at')[:10]
    bronze_promos_promotions_serializer = AllShopPromotionsSerializer(bronze_promos, many=True)
    bronze_promos = bronze_promos_promotions_serializer.data

    # Combine promotions
    promotions = {
        'promoted_services': promoted_services,
        'gold_promoted_shops': gold_promos,
        'silver_promoted_shops': silver_promos,
        'bronze_promoted_shops': bronze_promos,
    }
    data['promotions'] = promotions

    # Fetch shops without promotions
    shops_without_promotions = Shop.objects.annotate(num_promotions=Count('shop_promos')).filter(num_promotions=0)[:10]
    shops_without_promotions_data = ListShopsSerializer(shops_without_promotions, many=True).data
    data['shops_without_promotions'] = shops_without_promotions_data

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def explore_shops_view(request):
    payload = {}
    data = {}
    errors = {}

  
    bookings_today = []
    service_categories = []


    user_id = request.query_params.get('user_id', None)
    lat = Decimal(request.query_params.get('lat', 0.0))
    lng = Decimal(request.query_params.get('lng', 0.0))

    if not user_id:
        errors['user_id'] = ['User ID is required.']

    if not lat:
        errors['lat'] = ['User latitude is required.']

    if not lng:
        errors['lng'] = ['User longitude is required.']

    try:
        user = User.objects.get(user_id=user_id)
    except:
        errors['user_id'] = ['User does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    user.lat = Decimal(lat)
    user.lng = Decimal(lng)
    user.save()




    # Fetch Gold, Silver, Bronze promotions
    gold_promos = ShopPromotion.objects.all().filter(level='Gold').order_by('-created_at')[:10]
    gold_promos_promotions_serializer = AllShopPromotionsSerializer(gold_promos, many=True)
    gold_promos = gold_promos_promotions_serializer.data

    silver_promos = ShopPromotion.objects.all().filter(level='Silver').order_by('-created_at')[:10]
    silver_promos_promotions_serializer = AllShopPromotionsSerializer(silver_promos, many=True)
    silver_promos = silver_promos_promotions_serializer.data

    bronze_promos = ShopPromotion.objects.all().filter(level='Bronze').order_by('-created_at')[:10]
    bronze_promos_promotions_serializer = AllShopPromotionsSerializer(bronze_promos, many=True)
    bronze_promos = bronze_promos_promotions_serializer.data

    # Combine promotions
    promotions = {
        'gold_promoted_shops': gold_promos,
        'silver_promoted_shops': silver_promos,
        'bronze_promoted_shops': bronze_promos,
    }
    data['promotions'] = promotions


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)
