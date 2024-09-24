# events/api/serializers.py

from rest_framework import serializers
from events.models import Event, Attendee
from accounts.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']

class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    attendees_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'location', 'organizer', 'attendees_count', 'created_at', 'updated_at']

    def get_attendees_count(self, obj):
        return obj.attendees.count()

class AttendeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)

    class Meta:
        model = Attendee
        fields = ['id', 'user', 'event', 'registration_date']