import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import csv
import re
import matplotlib.pyplot as plt
from collections import defaultdict

def get_company_name(url):
    """Extract company name from the URL"""
    domain = urlparse(url).netloc
    company_name = re.sub(r'^www\.', '', domain)
    company_name = re.sub(r'\.com$|\.org$|\.net$', '', company_name)
    return company_name.lower()

def get_all_links(url):
    """Get all links from a given URL"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                full_url = urljoin(url, href)
                if urlparse(full_url).netloc == urlparse(url).netloc:
                    links.add(full_url)
        return links
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return set()

def scrape_product_details(url):
    """Scrape product details from a given URL"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Example selectors; these will need to be customized based on the website's structure
        title = soup.find('h1', class_='product-title').get_text(strip=True) if soup.find('h1', class_='product-title') else "No title"
        price = soup.find('span', class_='product-price').get_text(strip=True) if soup.find('span', class_='product-price') else "No price"
        payment_methods = soup.find('div', class_='payment-methods').get_text(strip=True) if soup.find('div', class_='payment-methods') else "No payment methods"
        
        # Categorize based on the title or other content
        category = categorize_content(title)  # Categorize based on title
        
        return title, price, payment_methods, category
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return "Error", "Error", "Error", "Error"

def categorize_content(title):
    """Categorize content based on keywords in title"""
    categories = {
        'Beverages': ['coffee', 'latte', 'espresso', 'drink'],
        'Food': ['donut', 'sandwich', 'bagel', 'muffin'],
        'Others': []
    }
    for category, keywords in categories.items():
        if any(keyword in title.lower() for keyword in keywords):
            return category
    return 'Others'

def scrape_and_save_to_csv(base_url, max_depth):
    """Scrape website and save data to CSV"""
    visited = set()
    to_visit = {base_url}
    all_links = set()
    company_name = get_company_name(base_url)
    folder_name = f"{company_name}_data"
    os.makedirs(folder_name, exist_ok=True)
    csv_file = os.path.join(folder_name, f"{company_name}_scraped_data.csv")

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['URL', 'Product Title', 'Price', 'Payment Methods', 'Category'])  # CSV headers

        for depth in range(max_depth):
            new_to_visit = set()
            for url in to_visit:
                if url not in visited:
                    print(f"Scraping: {url}")
                    links = get_all_links(url)
                    all_links.update(links)
                    new_to_visit.update(links - visited)
                    visited.add(url)
                    
                    # Scrape product details
                    title, price, payment_methods, category = scrape_product_details(url)
                    writer.writerow([url, title, price, payment_methods, category])  # Save product details
            to_visit = new_to_visit
            print(f"Depth {depth + 1} completed. Total links found: {len(all_links)}")

    print(f"\nScraped data has been saved to {os.path.abspath(csv_file)}")
    print(f"Total number of unique links: {len(all_links)}")

    return csv_file

def draw_graph(csv_file):
    """Draw a graph based on the scraped data"""
    category_counts = defaultdict(int)

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            category_counts[row[4]] += 1  # Count occurrences of each category

    categories = list(category_counts.keys())
    counts = list(category_counts.values())

    plt.figure(figsize=(10, 5))
    plt.bar(categories, counts, color='skyblue')
    plt.xlabel('Categories')
    plt.ylabel('Number of Products')
    plt.title('Number of Products by Category')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    base_url = input("Enter the URL of the website you want to scrape: ")
    max_depth = int(input("Enter the maximum depth to scrape: "))
    csv_file = scrape_and_save_to_csv(base_url, max_depth)
    draw_graph(csv_file)
