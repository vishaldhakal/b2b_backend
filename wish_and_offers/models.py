from django.db import models
from accounts.models import CustomUser, Organization
from events.models import Event

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.FileField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    hs_code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    image = models.FileField(upload_to='product_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} ({self.hs_code})"

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.FileField(upload_to='service_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Wish(models.Model):
    WISH_STATUS = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    WISH_TYPE = [
        ('Product', 'Product'),
        ('Service', 'Service'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wishes')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='wishes', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishes', blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='wishes', blank=True, null=True)
    status = models.CharField(max_length=10, choices=WISH_STATUS, default='Pending')
    wish_type = models.CharField(max_length=10, choices=WISH_TYPE, default='Product')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wish by {self.user.username} for {self.event.title if self.event else 'No Event'}"

class Offer(models.Model):
    OFFER_STATUS = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    OFFER_TYPE = [
        ('Product', 'Product'),
        ('Service', 'Service'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='offers')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='offers', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers', blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='offers', blank=True, null=True)
    status = models.CharField(max_length=10, choices=OFFER_STATUS, default='Pending')
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPE, default='Product')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Offer by {self.user.username} for {self.event.title if self.event else 'No Event'}"

class Match(models.Model):
    wish = models.ForeignKey(Wish, on_delete=models.CASCADE, related_name='matches')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='matches')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Match: {self.wish.user.username} with {self.offer.user.username}"

    @staticmethod
    def find_matches():
        matches = []
        wishes = Wish.objects.filter(status='Pending')
        offers = Offer.objects.filter(status='Pending')

        for wish in wishes:
            for offer in offers:
                if wish.wish_type == offer.offer_type:
                    if (wish.product and offer.product and wish.product == offer.product) or \
                       (wish.service and offer.service and wish.service == offer.service):
                        match = Match(wish=wish, offer=offer)
                        matches.append(match)
        return matches
