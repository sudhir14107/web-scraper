import requests
from bs4 import BeautifulSoup
import json
import time
from typing import List
from app.services.notification import Notification
import os

class ScraperService:
    def __init__(self, proxy: str = None, page_limit: int = 5, recipients: list = None):
        self.proxy = proxy
        self.page_limit = page_limit
        self.base_url = "https://dentalstall.com/shop/"
        self.scraped_data = []
        self.notification_service = Notification(recipients or [])

    def save_data(self):
        formatted_data = self.scraped_data
        with open('scrape_dump.json', 'w', encoding='utf-8') as json_file:
            json.dump(formatted_data, json_file, indent=4, ensure_ascii=False)

    def fetch_page(self, page_number: int):
        url = f"{self.base_url}page/{page_number}/"
        if self.proxy:
            response = requests.get(url, proxies={"http": self.proxy, "https": self.proxy})
        else:
            response = requests.get(url)
        
        if response.status_code == 200:
            return response.text
        return None

    def parse_product_data(self, page_content: str):
        soup = BeautifulSoup(page_content, 'html.parser')
        product_elements = soup.find_all('div', class_='product-inner clearfix')  # Find all product containers

        for product in product_elements:
            title = product.find('h2', class_='woo-loop-product__title').text.strip()
            price_element = product.find('div', class_='mf-product-price-box')
            price = float(price_element.find('bdi').text.strip().replace('₹', '').replace(',', '')) if price_element and price_element.find('bdi') else 0
            image_path = product.find('div', class_='mf-product-thumbnail').find('img')['data-lazy-src']
            
            # Append product data to the list with type check
            self.scraped_data.append({ 
                "product_title": str(title),
                "product_price": int(price),
                "path_to_image": str(image_path)
            })

    def start_scraping(self, page_limit: int):
        retries = int(os.getenv('SCRAPER_RETRIES', 3))
        for page_number in range(1, page_limit + 1):
            for attempt in range(retries):
                page_content = self.fetch_page(page_number)
                if page_content:
                    self.parse_product_data(page_content)
                    break
                else:
                    print(f"Attempt {attempt + 1} failed for page {page_number}. Retrying...")
                    time.sleep(10)
            else:
                print(f"Failed to fetch page {page_number} after {retries} attempts.")
        
        self.save_data()
        self.notification_service.send_notification(success=True, message="Scraping completed successfully.", data_length=len(self.scraped_data))
        return {"status": "success", "message": "Scraping completed successfully.", "data_length": len(self.scraped_data)}

