from django.urls import path
from .views import EventListCreateView, EventRetrieveUpdateDestroyView, AttendeeListCreateView, AttendeeRetrieveDestroyView

urlpatterns = [
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventRetrieveUpdateDestroyView.as_view(), name='event-retrieve-update-destroy'),
    path('events/<int:event_id>/attendees/', AttendeeListCreateView.as_view(), name='attendee-list-create'),
    path('attendees/<int:pk>/', AttendeeRetrieveDestroyView.as_view(), name='attendee-retrieve-destroy'),
]