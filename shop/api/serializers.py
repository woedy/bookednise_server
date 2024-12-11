from django.contrib.auth import get_user_model
from rest_framework import serializers

from payments.models import PaymentSetup
from shop.models import Shop, ShopPackagePromotion, ShopPromotion, ShopService, ShopInterior, ShopExterior, ShopWork, ShopStaff, ShopPackage, \
    ShopAvailability, ServiceSpecialist
from slots.api.serializers import StaffSlotSerializer
from datetime import date


User = get_user_model()


class ShopPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopPackage
        fields = [
            'id',
            'package_name',
            'price',
            'rating',
            'photo',
            'duration'
        ]

class ShopServiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopService
        fields = [
            'service_id',
            'service_type',
            #'price',
            #'duration',
            'description',
        ]


class StaffUserSerializer(serializers.ModelSerializer):
    staff_slot = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'staff_slot'
        ]

    def get_staff_slot(self, obj):
        staff_slots = obj.staff_slot.filter(slot_date__gte=date.today())
        return StaffSlotSerializer(staff_slots, many=True).data


class SpecialistSerializer(serializers.ModelSerializer):
    user = StaffUserSerializer(many=False)
    class Meta:
        model = ShopStaff
        fields = [
            'staff_id',
            'user',
            'staff_name',
            'photo',
            'role',
            'rating'
        ]


class ServiceSpecialistSerializer(serializers.ModelSerializer):
    specialist = SpecialistSerializer(many=False)
    class Meta:
        model = ServiceSpecialist
        fields = [
            #'service',
            'specialist'
        ]



class ShopServiceSerializer(serializers.ModelSerializer):
    package_service = ShopPackageSerializer(many=True)
    service_specialist = ServiceSpecialistSerializer(many=True)
    class Meta:
        model = ShopService
        fields = [
            'service_id',
            'service_type',
            'package_service',
            'service_specialist'

        ]

class ShopInteriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopInterior
        fields = [
            'id',
            'photo',
        ]

class ShopExteriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopExterior
        fields = [
            'id',
            'photo',
        ]

class ShopWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopWork
        fields = [
            'id',
            'photo',
        ]



class ShopPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentSetup
        fields = [
            'id',
            'reservation_policy_value',
            'reservation_policy_description',
            'cancellation_policy_value',
            'cancellation_policy_description',
        ]


class ShopStaffSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = ShopStaff
        fields = [
            'staff_id',
            'user_id',
            'staff_name',
            'photo',
            'role',
            'rating',
        ]

    def get_user_id(self, obj):
        return obj.user.user_id if obj.user else None

class ShopDetailSerializer(serializers.ModelSerializer):
    shop_services = ShopServiceSerializer(many=True)
    shop_interior = ShopInteriorSerializer(many=True)
    shop_exterior = ShopExteriorSerializer(many=True)
    shop_work = ShopWorkSerializer(many=True)
    shop_staffs = ShopStaffSerializer(many=True)
    shop_payment_setup = ShopPaymentSerializer(many=False)
    #shop_packages = ShopPackageSerializer(many=True)

    class Meta:
        model = Shop
        fields = [
            'shop_id',
            'shop_name',
            'email',
            'business_type',
            'country',
            'phone',
            'description',
            'business_days',
            'business_hours_open',
            'business_hours_close',
            'special_features',
            'photo',
            'street_address1',
            'street_address2',
            'city',
            'state',
            'zipcode',
            'location_name',
            'lat',
            'lng',
            'rating',
            'open',

            'shop_services',
            'shop_interior',
            'shop_exterior',
            'shop_work',
            'shop_staffs',
            'shop_payment_setup',
            'cvr',

        ]



class ListShopsSerializer(serializers.ModelSerializer):
    shop_services = ShopServiceSerializer(many=True)
    shop_interior = serializers.SerializerMethodField()
    shop_exterior = serializers.SerializerMethodField()


    class Meta:
        model = Shop
        fields = [
            'shop_id',
            'shop_name',
            'photo',
            'location_name',
            'shop_services',
            'shop_interior',
            'shop_exterior',
            'business_type'
        ]
  
            
    def get_shop_interior(self, obj):
        interior = obj.shop_interior.first()  # Use first() instead of [0]
        if interior and interior.photo:
            return interior.photo.url
        return None  # 


                
    def get_shop_exterior(self, obj):
        exterior = obj.shop_exterior.first()  # Use first() instead of [0]
        if exterior and exterior.photo:
            return exterior.photo.url
        return None  # 
    



class ShopAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopAvailability
        fields = '__all__'




class AllShopPromotionsSerializer(serializers.ModelSerializer):
    shop = ListShopsSerializer(many=False)

    class Meta:
        model = ShopPromotion
        fields = '__all__'





class AllShopPackagePromotionsSerializer(serializers.ModelSerializer):
    package_photo = serializers.SerializerMethodField()
    package_name = serializers.SerializerMethodField()
    package_price = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()
    shop = ListShopsSerializer(many=False)

    class Meta:
        model = ShopPackagePromotion
        fields = '__all__'

    
            
    def get_package_photo(self, obj):
        photo = obj.package.photo.url
        return photo


            
    def get_package_name(self, obj):
        name = obj.package.package_name
        return name



            
    def get_package_price(self, obj):
        price = obj.package.price
        return price

            
    def get_discount_price(self, obj):
        original_price = obj.package.price
        discount_percent = obj.discount_percent
        discount_amount = float(original_price) * float(discount_percent / 100)
        
        final_price = float(original_price) - float(discount_amount)

        return round(final_price, 2)    



class ShopPromotionDetailsSerializer(serializers.ModelSerializer):
    package_photo = serializers.SerializerMethodField()
    
    class Meta:
        model = ShopPromotion
        fields = '__all__'

            
    def get_package_photo(self, obj):
        package = obj.package.photo
        return package



