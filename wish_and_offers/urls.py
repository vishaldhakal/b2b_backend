from django.urls import path
from .views import (
    CategoryListCreateView,
    ProductListCreateView,
    ServiceListCreateView,
    WishListCreateView,
    WishRetrieveUpdateDestroyView,
    OfferListCreateView,
    OfferRetrieveUpdateDestroyView,
    MatchListView,
    FindMatchesView,
    EventWishesOffersView
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('services/', ServiceListCreateView.as_view(), name='service-list-create'),
    path('wishes/', WishListCreateView.as_view(), name='wish-list-create'),
    path('wishes/<int:pk>/', WishRetrieveUpdateDestroyView.as_view(), name='wish-retrieve-update-destroy'),
    path('offers/', OfferListCreateView.as_view(), name='offer-list-create'),
    path('offers/<int:pk>/', OfferRetrieveUpdateDestroyView.as_view(), name='offer-retrieve-update-destroy'),
    path('matches/', MatchListView.as_view(), name='match-list'),
    path('find-matches/', FindMatchesView.as_view(), name='find-matches'),
    path('events/<int:event_id>/wishes-offers/', EventWishesOffersView.as_view(), name='event-wishes-offers'),
]