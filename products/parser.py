import requests
from bs4 import BeautifulSoup
from products.models import Product
import time

def parse_wildberries_html(query, pages=1):
    base_url = "https://www.wildberries.ru/catalog/0/search.aspx"

    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    for page in range(1, pages + 1):
        params = {
            "search": query,
            "page": page
        }

        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Ошибка запроса: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "lxml")
        cards = soup.select("div.product-card")

        if not cards:
            print(f"⚠ Товары не найдены на странице {page}")
            continue

        for card in cards:
            name_tag = card.select_one("a.goods-name")
            price_tag = card.select_one("ins.lower-price")
            old_price_tag = card.select_one("del")

            name = name_tag.get_text(strip=True) if name_tag else "Неизвестно"
            discounted_price = parse_price(price_tag)
            original_price = parse_price(old_price_tag) or discounted_price
            rating = float(card.get("data-rating", "0"))
            reviews = int(card.get("data-feedbacks", "0"))

            Product.objects.update_or_create(
                name=name,
                defaults={
                    "price": original_price,
                    "discounted_price": discounted_price,
                    "rating": rating,
                    "review_count": reviews
                }
            )

        print(f"Загружено {len(cards)} товаров с страницы {page}")
        time.sleep(1)

    print("🎉 Парсинг HTML завершен.")

def parse_price(tag):
    if not tag:
        return 0.0
    price_text = tag.get_text(strip=True).replace("₽", "").replace(" ", "").replace(",", ".")
    try:
        return float(price_text)
    except ValueError:
        return 0.0
