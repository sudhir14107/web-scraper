import requests
from bs4 import BeautifulSoup
import json
import time

class ScraperService:
    def __init__(self, proxy: str = None, page_limit: int = 5):
        self.proxy = proxy
        self.page_limit = page_limit
        self.base_url = "https://dentalstall.com/shop/"
        self.scraped_data = []

    def fetch_page(self, page_number: int):
        """Fetch page content."""
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
            # Extract product title
            product_name = product.find('h2', class_='woo-loop-product__title').text.strip()
            
            # Extract price
            price_element = product.find('div', class_='mf-product-price-box')
            price = price_element.find('ins').text.strip() if price_element and price_element.find('ins') else 'N/A'
            
            # Extract image URL
            img_url = product.find('div', class_='mf-product-thumbnail').find('img')['data-lazy-src']
            
            # Append product data to the list
            self.scraped_data.append({
                'name': product_name,
                'price': price,
                'image_url': img_url
            })

    def start_scraping(self):
        """Scrape products from the given number of pages."""
        for page_number in range(1, self.page_limit + 1):
            print(f"Scraping page {page_number}")
            page_content = self.fetch_page(page_number)
            if page_content:
                self.parse_product_data(page_content)  # Parse product data from the page
            else:
                print(f"Failed to fetch page {page_number}. Retrying...")
                time.sleep(3)  # Simple retry mechanism

        # Return the scraped product data as a JSON string
        return json.dumps(self.scraped_data, indent=4)

