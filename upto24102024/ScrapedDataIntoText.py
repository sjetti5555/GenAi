import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import signal
import sys
import re

# Global variable to track if the script is interrupted
interrupted = False

def signal_handler(sig, frame):
    global interrupted
    print("\nInterruption detected. Saving progress...")
    interrupted = True

signal.signal(signal.SIGINT, signal_handler)

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

def scrape_page_content(url):
    """Scrape content from a given URL"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "No title"
        content = soup.get_text(separator='\n', strip=True)
        return title, content
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return "Error", f"Failed to fetch content: {e}"

def save_content_to_files(company_name, links_and_content):
    """Save scraped content to text files"""
    folder_name = f"{company_name}_data"
    os.makedirs(folder_name, exist_ok=True)
    
    for i, (url, (title, content)) in enumerate(links_and_content.items(), 1):
        file_name = f"page_{i:03d}.txt"
        file_path = os.path.join(folder_name, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"Title: {title}\n\n")
            f.write(f"URL: {url}\n\n")
            f.write(content)
    
    return folder_name

def scrape_links_and_content(base_url, max_depth=3):
    """Scrape links and content from the base URL and its subpages up to max_depth"""
    visited = set()
    to_visit = {base_url}
    all_links = set()
    links_and_content = {}

    for depth in range(max_depth):
        if interrupted:
            break
        new_to_visit = set()
        for url in to_visit:
            if interrupted:
                break
            if url not in visited:
                print(f"Scraping: {url}")
                links = get_all_links(url)
                all_links.update(links)
                new_to_visit.update(links - visited)
                visited.add(url)
                title, content = scrape_page_content(url)
                links_and_content[url] = (title, content)
        to_visit = new_to_visit
        print(f"Depth {depth + 1} completed. Total links found: {len(all_links)}")

    return all_links, links_and_content

# Get user input
base_url = input("Enter the URL of the website you want to scrape: ")
max_depth = int(input("Enter the maximum depth to scrape (default is 3): ") or 3)

# Generate company-specific filename
company_name = get_company_name(base_url)
file_name = f"{company_name}_scraped_links.txt"

# Scrape the website
print(f"Starting to scrape {base_url}...")
all_links, links_and_content = scrape_links_and_content(base_url, max_depth)

# Save the links to a file
with open(file_name, "w", encoding='utf-8') as f:
    for link in sorted(all_links):
        f.write(f"{link}\n")

print(f"\nScraped links have been saved to {os.path.abspath(file_name)}")
print(f"Total number of unique links: {len(all_links)}")

# Save content to text files
folder_path = save_content_to_files(company_name, links_and_content)
print(f"Scraped content has been saved to text files in: {os.path.abspath(folder_path)}")

if interrupted:
    print("Scraping was interrupted. Progress has been saved.")
