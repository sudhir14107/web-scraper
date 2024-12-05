import requests
from bs4 import BeautifulSoup
import json
import time
from app.services.notification import Notification
import os

class ScraperService:
    def __init__(self, redis_cache, page_limit: int = 5, proxy: str = None, recipients: list = None):
        self.proxy = proxy
        self.page_limit = page_limit
        self.base_url = "https://dentalstall.com/shop/"
        self.scraped_data = []
        self.notification_service = Notification(recipients or [])
        self.redis_cache = redis_cache
        self.total_updated_count = 0
        self.total_new_count = 0

    def save_data(self) -> None:
        """Save scraped data to a JSON file."""
        formatted_data = self.scraped_data
        try:
            with open('scrape_dump.json', 'w', encoding='utf-8') as json_file:
                json.dump(formatted_data, json_file, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving data: {e}")

    def fetch_page(self, page_number: int) -> str:
        """Fetch a page from the website."""
        url = f"{self.base_url}page/{page_number}/"
        try:
            response = requests.get(url, proxies={"http": self.proxy, "https": self.proxy} if self.proxy else None)
            response.raise_for_status()  # Raise an error for bad responses
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching page {page_number}: {e}")
            return None

    def data_update(self, title: str, price: float) -> None:
        """Update the cached price and counts."""
        cached_price = self.redis_cache.get(title)
        if not cached_price:
            self.total_new_count += 1
            self.redis_cache.set(title, price)
        elif float(cached_price.decode('utf-8')) != price:
            self.total_updated_count += 1
            self.redis_cache.set(title, price)

    def parse_product_data(self, page_content: str) -> None:
        """Parse product data from the page content."""
        soup = BeautifulSoup(page_content, 'html.parser')
        product_elements = soup.find_all('div', class_='product-inner clearfix')

        for product in product_elements:
            title = product.find('h2', class_='woo-loop-product__title').text.strip()
            price_element = product.find('div', class_='mf-product-price-box')
            price = float(price_element.find('bdi').text.strip().replace('₹', '').replace(',', '')) if price_element and price_element.find('bdi') else 0
            image_path = product.find('div', class_='mf-product-thumbnail').find('img')['data-lazy-src']

            self.data_update(title, price)
            self.scraped_data.append({ 
                "product_title": str(title),
                "product_price": float(price),
                "path_to_image": str(image_path)
            })

    def start_scraping(self, page_limit: int):
        retries = int(os.getenv('SCRAPER_RETRIES', 3))
        retries_time = int(os.getenv('SCRAPER_RETRIES_TIME', 10))
        for page_number in range(1, page_limit + 1):
            for attempt in range(retries):
                page_content = self.fetch_page(page_number)
                if page_content:
                    self.parse_product_data(page_content)
                    break
                else:
                    print(f"Attempt {attempt + 1} failed for page {page_number}. Retrying...")
                    time.sleep(retries_time)
            else:
                print(f"Failed to fetch page {page_number} after {retries} attempts.")
        
        self.save_data()
        self.notification_service.send_notification(
            success=True, 
            message="Scraping completed successfully.", 
            data={
                "data_length": len(self.scraped_data), 
                "total_updated": self.total_updated_count, 
                "total_new": self.total_new_count
            })
        return {
            "status": "success", 
            "message": "Scraping completed successfully.", 
            "data": {
                "data_length": len(self.scraped_data), 
                "total_updated": self.total_updated_count, 
                "total_new": self.total_new_count
            }
        }

