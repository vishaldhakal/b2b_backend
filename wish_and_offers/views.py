from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Product, Service, Wish, Offer, Match
from .serializers import CategorySerializer, ProductSerializer, ServiceSerializer, WishSerializer, OfferSerializer, MatchSerializer, CreateWishSerializer, CreateOfferSerializer, MatchWishSerializer, MatchOfferSerializer
from django.core.exceptions import ObjectDoesNotExist

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
    serializer_class = CreateWishSerializer
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
    serializer_class = CreateOfferSerializer
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
    def get(self, request):
        wish_id = request.query_params.get('wish_id')
        offer_id = request.query_params.get('offer_id')

        if wish_id and offer_id:
            return Response({"error": "Please provide either wish_id or offer_id, not both."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            if wish_id:
                # Verify that the wish exists
                Wish.objects.get(id=wish_id)
                matches = Match.find_matches_for_wish(wish_id)
                serializer = MatchWishSerializer
            elif offer_id:
                # Verify that the offer exists
                Offer.objects.get(id=offer_id)
                matches = Match.find_matches_for_offer(offer_id)
                serializer = MatchOfferSerializer
            else:
                matches = Match.find_matches()
                serializer = MatchSerializer

            serialized_matches = []
            for match, score in matches:
                match.match_score = score  # Attach the score to the match object
                serialized_matches.append(serializer(match).data)

            return Response({
                "message": f"{len(matches)} matches found",
                "matches": serialized_matches
            }, status=status.HTTP_200_OK)

        except ObjectDoesNotExist as e:
            return Response({
                "error": f"Invalid {'wish' if wish_id else 'offer'} ID: {str(e)}"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "error": f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SaveMatchView(APIView):
    def post(self, request):
        wish_id = request.data.get('wish_id')
        offer_id = request.data.get('offer_id')
        if wish_id and offer_id:
            Match.objects.create(wish_id=wish_id, offer_id=offer_id)
            return Response({"message": "Match saved successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST)

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