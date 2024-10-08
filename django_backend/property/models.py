from django.db import models

import uuid
from django.conf import settings
from useraccount.models import User

# Create your models here.
class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    guests = models.IntegerField()
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=20)
    category = models.CharField(max_length=100)
    # favourited
    image = models.ImageField(upload_to='uploads/properties')
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def image_url(self):
        return f'{settings.WEBSITE_URL}{self.image.url}'
    
class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reservations')
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField()
    number_of_nights = models.IntegerField()
    total_price = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')

    created_at = models.DateTimeField(auto_now_add=True)