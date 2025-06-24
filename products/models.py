from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0.0)
    reviews_count = models.PositiveIntegerField(default=0)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'discounted_price': self.discount_price,
            'rating': self.rating,
            'review_count': self.reviews_count
        }