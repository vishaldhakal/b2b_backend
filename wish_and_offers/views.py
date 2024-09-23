from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Product, Service, Wish, Offer, Match
from .serializers import CategorySerializer, ProductSerializer, ServiceSerializer, WishSerializer, OfferSerializer, MatchSerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class WishListCreateView(generics.ListCreateAPIView):
    serializer_class = WishSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wish.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WishRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wish.objects.all()
    serializer_class = WishSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class OfferListCreateView(generics.ListCreateAPIView):
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Offer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OfferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class MatchListView(generics.ListAPIView):
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Match.objects.filter(wish__user=self.request.user) | Match.objects.filter(offer__user=self.request.user)

class FindMatchesView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        matches = Match.find_matches()
        Match.objects.bulk_create(matches)
        return Response({"message": f"{len(matches)} matches found and created"}, status=status.HTTP_201_CREATED)

class EventWishesOffersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, event_id):
        wishes = Wish.objects.filter(event_id=event_id)
        offers = Offer.objects.filter(event_id=event_id)
        wish_serializer = WishSerializer(wishes, many=True)
        offer_serializer = OfferSerializer(offers, many=True)
        return Response({
            "wishes": wish_serializer.data,
            "offers": offer_serializer.data
        })