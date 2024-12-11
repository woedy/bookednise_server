from django.contrib.auth import get_user_model
from rest_framework import serializers

from bookednise_pro import settings
from bookings.api.serializers import ListBookingSerializer
from shop.models import Shop
from user_profile.models import UserProfile

User = get_user_model()



class ListAdminShopsSerializer(serializers.ModelSerializer):
    services_count = serializers.SerializerMethodField()
    staffs_count = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = [
            'shop_id',
            'shop_name',
            'photo',
            'services_count',
            'staffs_count'
        ]

    def get_services_count(self, obj):
        return obj.shop_services.count()

    def get_staffs_count(self, obj):
        return obj.shop_staffs.count()

class UserProfileSerializer(serializers.ModelSerializer):


    class Meta:
        model = UserProfile
        fields = [
            'phone',
            'photo',

        ]


class UserProfileDetailSerializer(serializers.ModelSerializer):


    class Meta:
        model = UserProfile
        fields = [
            'phone',
            'photo',
            'about_me',

        ]

class ListAdminAllUsersSerializer(serializers.ModelSerializer):
    personal_info = UserProfileSerializer(many=False)
    bookings_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            'user_id',
            'email',
            'full_name',
            'personal_info',
            'bookings_count'
        ]





class AdminUserDetailSerializer(serializers.ModelSerializer):
    personal_info = UserProfileDetailSerializer(many=False)
    bookings = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'user_id',
            'email',
            'full_name',
            'user_type',
            'is_deleted',
            'personal_info',
            'bookings'
        ]

    def get_bookings(self, obj):
        bookings = obj.shop_service_bookings.all()
        return ListBookingSerializer(bookings, many=True).data