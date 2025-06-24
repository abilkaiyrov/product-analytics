from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Load fake products into database'

    def handle(self, *args, **kwargs):
        products = [
            {"name": "Смартфон A1", "price": 15000, "discounted_price": 13000, "rating": 4.5, "review_count": 1200},
            {"name": "Смартфон B2", "price": 20000, "discounted_price": 18000, "rating": 4.2, "review_count": 800},
            {"name": "Наушники C3", "price": 5000, "discounted_price": 4000, "rating": 4.8, "review_count": 1500},
            {"name": "Ноутбук D4", "price": 60000, "discounted_price": 55000, "rating": 4.1, "review_count": 400},
            {"name": "Планшет E5", "price": 30000, "discounted_price": 25000, "rating": 4.6, "review_count": 700},
            {"name": "Фитнес-браслет F6", "price": 4000, "discounted_price": 3500, "rating": 4.9, "review_count": 2000},
        ]
        for p in products:
            Product.objects.update_or_create(
                name=p["name"],
                defaults=p
            )
        self.stdout.write(self.style.SUCCESS("Фиктивные данные загружены!"))