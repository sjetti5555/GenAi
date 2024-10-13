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

def load_existing_links(filename):
    """Load existing links from the file"""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return set(line.strip() for line in f)
    return set()

def save_links_to_file(links, filename):
    """Save the links to a text file"""
    with open(filename, 'w') as f:
        for link in sorted(links):
            f.write(f"{link}\n")

def scrape_links(base_url, max_depth=3):
    """Scrape links from the base URL and its subpages up to max_depth"""
    visited = set()
    to_visit = {base_url}
    all_links = set()

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
        to_visit = new_to_visit
        print(f"Depth {depth + 1} completed. Total links found: {len(all_links)}")

    return all_links

# Get user input
base_url = input("Enter the URL of the website you want to scrape: ")
max_depth = int(input("Enter the maximum depth to scrape (default is 3): ") or 3)

# Generate company-specific filename
company_name = get_company_name(base_url)
file_name = f"{company_name}_scraped_links.txt"

# Scrape the website
print(f"Starting to scrape {base_url}...")
all_links = scrape_links(base_url, max_depth)

# Save the result to a file
save_links_to_file(all_links, file_name)
print(f"\nScraped links have been saved to {os.path.abspath(file_name)}")
print(f"Total number of unique links: {len(all_links)}")

if interrupted:
    print("Scraping was interrupted. Progress has been saved.")
