# events/api/views.py

from rest_framework import generics, permissions
from events.models import Event, Attendee
from .serializers import EventSerializer, AttendeeSerializer

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(organizer=self.request.user)

class AttendeeListCreateView(generics.ListCreateAPIView):
    serializer_class = AttendeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Attendee.objects.filter(event_id=self.kwargs['event_id'])

    def perform_create(self, serializer):
        event = Event.objects.get(pk=self.kwargs['event_id'])
        serializer.save(user=self.request.user, event=event)

class AttendeeRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer
    permission_classes = [permissions.IsAuthenticated]