import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse

def is_valid_url(url):
    """Check if url is a valid URL."""
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url):
    """Returns all URLs that are found on `url` and belong to the same website"""
    urls = set()
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        if domain_name not in parsed_href.netloc:
            continue
        if not is_valid_url(href):
            continue
        urls.add(href)
    return urls

def scrape_page(url):
    """Scrape the content of a single page"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = soup.title.string if soup.title else "No title found"
        
        # Extract all text
        text = soup.get_text(separator='\n', strip=True)
        
        return f"URL: {url}\nTitle: {title}\n\nContent:\n{text}\n\n{'='*100}\n"
    except requests.RequestException as e:
        return f"Failed to retrieve {url}. Error: {e}\n\n{'='*100}\n"

def scrape_website(url, max_pages=100):
    """Scrape all pages of the website, up to max_pages"""
    links = get_all_website_links(url)
    all_content = []
    scraped_count = 0
    
    for link in links:
        if scraped_count >= max_pages:
            break
        print(f"Scraping: {link}")
        content = scrape_page(link)
        all_content.append(content)
        scraped_count += 1
    
    return ''.join(all_content)

# Get user input
url = input("Enter the URL of the website you want to scrape: ")
max_pages = int(input("Enter the maximum number of pages to scrape (default is 100): ") or 100)

# Scrape the website
print(f"Starting to scrape {url}...")
result = scrape_website(url, max_pages)

# Save the result to a file
file_name = "scraped_website_data.txt"
with open(file_name, "w", encoding="utf-8") as file:
    file.write(result)

print(f"\nScraped data has been saved to {os.path.abspath(file_name)}")
