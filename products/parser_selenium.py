from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from .models import Product
import time

def parse_wildberries_selenium(query, pages=1):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)

    for page in range(1, pages + 1):
        url = f"https://www.wildberries.ru/catalog/0/search.aspx?search={query}&page={page}"
        driver.get(url)
        time.sleep(2)

        cards = driver.find_elements(By.CSS_SELECTOR, "div.product-card")
        if not cards:
            print(f"⚠ Товары не найдены на странице {page}")
            continue

        for card in cards:
            try:
                name = card.find_element(By.CSS_SELECTOR, ".product-card__brand").text + " " + card.find_element(By.CSS_SELECTOR, ".product-card__name").text
                price = int(card.find_element(By.CSS_SELECTOR, ".price__lower-price").text.replace('₽', '').replace(' ', '').strip())
                try:
                    old_price = int(card.find_element(By.CSS_SELECTOR, ".price__crossed").text.replace('₽', '').replace(' ', '').strip())
                except:
                    old_price = price

                try:
                    rating = float(card.find_element(By.CSS_SELECTOR, ".product-card__rating").get_attribute("textContent").strip())
                except:
                    rating = None

                try:
                    reviews = int(card.find_element(By.CSS_SELECTOR, ".product-card__count").text.strip("()"))
                except:
                    reviews = None

                Product.objects.create(
                    name=name,
                    price=old_price,
                    discount_price=price,
                    rating=rating,
                    reviews_count=reviews
                )
                print(f"{name}")
            except Exception as e:
                print(f"Ошибка при обработке товара: {e}")

    driver.quit()
    print("Парсинг Selenium завершен.")
