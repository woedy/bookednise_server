from django.contrib.auth import get_user_model
from rest_framework import serializers

from bookings.models import Booking, BookingPayment, BookingRating
from shop.api.serializers import ServiceSpecialistSerializer
from shop.models import ServiceCategory, ShopService, Shop, ShopStaff, ShopPackage
from slots.api.serializers import StaffSlotSerializer
from user_profile.models import UserProfile

User = get_user_model()

class BookingRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRating
        fields = [
            'id',
            'rating',
            'report',

        ]

class ShopSerializer(serializers.ModelSerializer):
    shop_interior = serializers.SerializerMethodField()
    shop_exterior = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = [
            'shop_name',
            'photo',
            'location_name',
            'open',
            'shop_interior',
            'shop_exterior',

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
    




class BookingPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingPayment
        fields = [
            'id',
            'payment_method',
            'amount',
        ]
class BookingPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopPackage
        fields = [
            'id',
            'package_name',
            'photo',
            'price',
            'rating',
        ]



class BookingSeriveSerializer(serializers.ModelSerializer):
    #service_specialist = ServiceSpecialistSerializer(many=True)

    class Meta:
        model = ShopService
        fields = [
            'service_id',
            'service_type',
            'service_specialist',
        ]

class BookendStaffUserSerializer(serializers.ModelSerializer):
    staff_slot = StaffSlotSerializer(many=True)
    class Meta:
        model = User
        fields = [
            'staff_slot'
        ]

class BookingStaffSerializer(serializers.ModelSerializer):
    user = BookendStaffUserSerializer(many=False)
    class Meta:
        model = ShopStaff
        fields = [
            'staff_id',
            'staff_name',
            'role',
            'photo',
            'rating',
            'user'
        ]


class BookingUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'photo',
            'phone',
        ]

class BookingUserSerializer(serializers.ModelSerializer):
    personal_info = BookingUserProfileSerializer(many=False)
    class Meta:
        model = User
        fields = [
            'user_id',
            'email',
            'full_name',
            'personal_info',
        ]


class BookingSerializer(serializers.ModelSerializer):
    client = BookingUserSerializer(many=False)
    service = BookingSeriveSerializer(many=False)
    booked_staff = BookingStaffSerializer(many=False)
    package = BookingPackageSerializer(many=False)
    booking_payments = BookingPaymentsSerializer(many=False)
    shop = ShopSerializer(many=False)

    class Meta:
        model = Booking
        fields = [
            'booking_id',
            'shop',
            'service',
            'client',
            'service_type',
            'package',
            'booked_staff',

            'booking_date',
            'booking_time',

            're_scheduled',
            'booking_rescheduled_at',

            'confirm_payment',

            'split',
            'booking_split_from',
            'booking_split_to',

            'amount_to_pay',
            'actual_price',

            'actual_duration',
            'notes',
            'review',

            'status',
            'booking_start',
            'booking_end',
            'booking_approved_at',
            'booking_declined_at',
            'booking_cancelled_at',
            'booking_payments',
            "is_gift",

        ]

class ListBookingSerializer(serializers.ModelSerializer):
    client = BookingUserSerializer(many=False)
    service = BookingSeriveSerializer(many=False)
    package = BookingPackageSerializer(many=False)
    booked_staff = BookingStaffSerializer(many=False)
    booking_payments = BookingPaymentsSerializer(many=False)
    shop = ShopSerializer(many=False)

    class Meta:
        model = Booking
        fields = [
            'booking_id',
            'client',
            'service_type',
            'service',
            'shop',
            'package',

            'booking_date',
            'booking_time',
            'status',
            'slot',
            'booking_payments',
            "booked_staff",
            "booked_staff",
            "is_gift",
        ]



class ListBookingAdminSerializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField()
    shop_name = serializers.SerializerMethodField()
    price = serializers.CharField(source='amount_to_pay')

    class Meta:
        model = Booking
        fields = [
            'booking_id',
            'client_name',
            'shop_name',
            'price',
            'status'
        ]

    def get_client_name(self, obj):
        return obj.client.full_name if obj.client else None

    def get_shop_name(self, obj):
        return obj.shop.shop_name if obj.shop else None
    




class ServiceCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceCategory
        fields = [
            'id',
            'name',
            'photo',
        ]
