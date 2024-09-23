from rest_framework import serializers
from .models import Category, Product, Service, Wish, Offer, Match
from accounts.models import CustomUser, Organization
from events.models import Event

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Service
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'start_date', 'end_date']

class WishSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Wish
        fields = '__all__'

class OfferSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Offer
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    wish = WishSerializer(read_only=True)
    offer = OfferSerializer(read_only=True)

    class Meta:
        model = Match
        fields = '__all__'