from django.core.management.base import BaseCommand
from products.models import Product
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

class Command(BaseCommand):
    help = 'Парсинг Wildberries по ключевому слову'

    def add_arguments(self, parser):
        parser.add_argument('keyword', type=str, help='Ключевое слово для поиска')
        parser.add_argument('--pages', type=int, default=1, help='Количество страниц')

    def handle(self, *args, **kwargs):
        keyword = kwargs['keyword']
        pages = kwargs['pages']

        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)

        Product.objects.all().delete()
        self.stdout.write("🗑️ Старые товары удалены")

        for page in range(1, pages + 1):
            url = f"https://www.wildberries.ru/catalog/0/search.aspx?page={page}&search={keyword}"
            self.stdout.write(f"Парсим страницу: {url}")
            driver.get(url)
            time.sleep(5)

            cards = driver.find_elements(By.CSS_SELECTOR, ".product-card__wrapper")
            for card in cards:
                try:
                    name = card.find_element(By.CSS_SELECTOR, ".product-card__name").text.strip()
                except:
                    name = "Неизвестно"

                try:
                    price_el = card.find_element(By.CSS_SELECTOR, ".price__wrap del")
                    price = int(price_el.text.replace('₽', '').replace(' ', '').strip())
                except:
                    price = 0

                try:
                    discount_el = card.find_element(By.CSS_SELECTOR, ".price__lower-price")
                    discount_price = int(discount_el.text.replace('₽', '').replace(' ', '').strip())
                except:
                    discount_price = price

                try:
                    rating_el = card.find_element(By.CSS_SELECTOR, ".address-rate-mini")
                    rating_text = rating_el.text.strip().replace(',', '.')
                    rating = float(rating_text) if rating_text else 0.0
                except:
                    rating = 0.0

                try:
                    reviews_el = card.find_element(By.CSS_SELECTOR, ".product-card__count")
                    reviews_text = reviews_el.text.strip()
                    reviews_count = int(''.join(filter(str.isdigit, reviews_text)))
                except:
                    reviews_count = 0

                Product.objects.create(
                    name=name,
                    price=price,
                    discount_price=discount_price,
                    rating=rating,
                    reviews_count=reviews_count
                )
                self.stdout.write(f"{name} | {price} | {discount_price} | {rating} | {reviews_count}")

        driver.quit()
        self.stdout.write("Парсинг завершён")
