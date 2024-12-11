
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shop.api.serializers import AllShopPackagePromotionsSerializer
from shop.models import Shop, ShopPackage, ShopPackagePromotion


User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication])
def add_promotion(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        shop_id = request.data.get('shop_id', "")
        package_id = request.data.get('package_id', "")
        description = request.data.get('description', "")
        discount_percent = request.data.get('discount_percent', "")
        start_date = request.data.get('start_date', "")
        end_date = request.data.get('end_date', "")
        coupon_code = request.data.get('coupon_code', "")
  

        if not shop_id:
            errors['shop_id'] = ['Shop ID is required.']

        if not package_id:
            errors['package_id'] = ['Package ID is required.']

        if not discount_percent:
            errors['discount_percent'] = ['Discount percent is required.']

        if not description:
            errors['description'] = ['Description is required.']

        if not start_date:
            errors['start_date'] = ['Start date is required.']

        if not end_date:
            errors['end_date'] = ['End date is required.']

        if not coupon_code:
            errors['coupon_code'] = ['Coupon code is required.']


        try:
            shop = Shop.objects.get(shop_id=shop_id)
        except:
            errors['shop_id'] = ['Shop does not exist.']


        try:
            package = ShopPackage.objects.get(id=package_id)
        except:
            errors['package_id'] = ['Package does not exist.']
            

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)



        promotion = ShopPackagePromotion.objects.create(
            shop=shop,
            package=package,
            description=description,
            discount_percent=discount_percent,
            start_date=start_date,
            end_date=end_date,
            coupon_code=coupon_code,
        )

        data["pack_promotion_id"] = promotion.pack_promotion_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication])
def get_all_promotions_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    shop_id = request.query_params.get('shop_id', '')
    page_size = 10

    all_promotions = ShopPackagePromotion.objects.all().order_by('-created_at')


    if search_query:
        all_promotions = all_promotions.filter(
            Q(promotion_id__icontains=search_query) |
            Q(package__package_name__icontains=search_query) 
        )


    if shop_id:
        all_promotions = all_promotions.filter(
            shop__shop_id=shop_id
        )

    paginator = Paginator(all_promotions, page_size)

    try:
        paginated_promotions = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_promotions = paginator.page(1)
    except EmptyPage:
        paginated_promotions = paginator.page(paginator.num_pages)

    all_promotions_serializer = AllShopPackagePromotionsSerializer(paginated_promotions, many=True)


    data['promotions'] = all_promotions_serializer.data
    data['pagination'] = {
        'page_number': paginated_promotions.number,
        'total_pages': paginator.num_pages,
        'next': paginated_promotions.next_page_number() if paginated_promotions.has_next() else None,
        'previous': paginated_promotions.previous_page_number() if paginated_promotions.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication])
def get_promotion_details_view(request):
    payload = {}
    data = {}
    errors = {}

    promotion_id = request.query_params.get('promotion_id', None)
    

    if not promotion_id:
        errors['promotion_id'] = ["ShopPackagePromotion id required"]

    try:
        promotion = ShopPackagePromotion.objects.get(promotion_id=promotion_id)
    except ShopPackagePromotion.DoesNotExist:
        errors['promotion_id'] = ['ShopPackagePromotion does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    promotion_serializer = ShopPackagePromotionDetailsSerializer(promotion, many=False)
    if promotion_serializer:
        promotion = promotion_serializer.data

    promotion_serializer = ShopPackagePromotionDetailsSerializer(promotion, many=False)

    payload['message'] = "Successful"
    payload['data'] = promotion

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication])
def edit_promotion(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        promotion_id = request.data.get('promotion_id', "")
        shop_id = request.data.get('shop_id', "")
        package_id = request.data.get('package_id', "")
        description = request.data.get('description', "")
        discount_percent = request.data.get('discount_percent', "")
        start_date = request.data.get('start_date', "")
        end_date = request.data.get('end_date', "")
        coupon_code = request.data.get('coupon_code', "")
  

        if not shop_id:
            errors['shop_id'] = ['Shop ID is required.']

        if not package_id:
            errors['package_id'] = ['Package ID is required.']

        if not discount_percent:
            errors['discount_percent'] = ['Discount percent is required.']

        if not description:
            errors['description'] = ['Description is required.']

        if not start_date:
            errors['start_date'] = ['Start date is required.']

        if not end_date:
            errors['end_date'] = ['End date is required.']

        if not coupon_code:
            errors['coupon_code'] = ['Coupon code is required.']


        try:
            shop = Shop.objects.get(shop_id=shop_id)
        except:
            errors['shop_id'] = ['Shop does not exist.']


        try:
            package = ShopPackage.objects.get(package_id=package_id)
        except:
            errors['package_id'] = ['Package does not exist.']
        try:
            promotion = ShopPackagePromotion.objects.get(promotion_id=promotion_id)
        except:
            errors['promotion_id'] = ['ShopPackagePromotion does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        promotion.shop = shop
        promotion.package = package
        promotion.description = description
        promotion.discount_percent = discount_percent
        promotion.start_date = start_date
        promotion.end_date = end_date
        promotion.coupon_code = coupon_code
        promotion.save()

        data["promotion_id"] = promotion.promotion_id

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication])
def archive_promotion(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        promotion_id = request.data.get('promotion_id', "")

        if not promotion_id:
            errors['promotion_id'] = ['ShopPackagePromotion ID is required.']

        try:
            promotion = ShopPackagePromotion.objects.get(promotion_id=promotion_id)
        except:
            errors['promotion_id'] = ['ShopPackagePromotion does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        promotion.is_archived = True
        promotion.save()



        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication])
def delete_promotion(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        promotion_id = request.data.get('promotion_id', "")

        if not promotion_id:
            errors['promotion_id'] = ['ShopPackagePromotion ID is required.']

        try:
            promotion = ShopPackagePromotion.objects.get(promotion_id=promotion_id)
        except:
            errors['promotion_id'] = ['ShopPackagePromotion does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        promotion.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication])
def unarchive_promotion(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        promotion_id = request.data.get('promotion_id', "")

        if not promotion_id:
            errors['promotion_id'] = ['ShopPackagePromotion ID is required.']

        try:
            promotion = ShopPackagePromotion.objects.get(promotion_id=promotion_id)
        except:
            errors['promotion_id'] = ['ShopPackagePromotion does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        promotion.is_archived = False
        promotion.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



 

@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication])
def get_all_archived_promotions_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_promotions = ShopPackagePromotion.objects.all().filter(is_archived=True)


    if search_query:
        all_promotions = all_promotions.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) 
        )


    paginator = Paginator(all_promotions, page_size)

    try:
        paginated_promotions = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_promotions = paginator.page(1)
    except EmptyPage:
        paginated_promotions = paginator.page(paginator.num_pages)

    all_promotions_serializer = AllShopPackagePromotionsSerializer(paginated_promotions, many=True)


    data['promotions'] = all_promotions_serializer.data
    data['pagination'] = {
        'page_number': paginated_promotions.number,
        'total_pages': paginator.num_pages,
        'next': paginated_promotions.next_page_number() if paginated_promotions.has_next() else None,
        'previous': paginated_promotions.previous_page_number() if paginated_promotions.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)
