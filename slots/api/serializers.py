from django.contrib.auth import get_user_model
from rest_framework import serializers

from slots.models import TimeSlot, StaffSlot

User = get_user_model()


class OccupantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'email', 'full_name', ]

class StaffTimeSerializer(serializers.ModelSerializer):
    occupant = OccupantSerializer(many=False)
    time = serializers.SerializerMethodField()

    class Meta:
        model = TimeSlot
        fields = ['time', 'occupied', 'occupant', ]

    def get_time(self, obj):
        # Format the time as "HH:MM"
        return obj.time.strftime("%H:%M")

class StaffSlotSerializer(serializers.ModelSerializer):

    slot_times = StaffTimeSerializer(many=True)

    class Meta:
        model = StaffSlot
        fields = ['id', 'slot_date', 'time_slot_count', 'state', 'slot_times']



