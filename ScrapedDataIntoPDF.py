import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import signal
import sys
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.units import inch

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

def clean_content(text):
    """Clean the content to avoid ReportLab parsing errors"""
    # Remove any XML/HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Replace problematic characters
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return text

def split_long_paragraphs(paragraph, max_width, font_name, font_size):
    """Split long paragraphs to avoid overflow"""
    words = paragraph.split()
    lines = []
    current_line = []
    current_width = 0

    for word in words:
        word_width = stringWidth(word, font_name, font_size)
        if current_width + word_width <= max_width:
            current_line.append(word)
            current_width += word_width + stringWidth(' ', font_name, font_size)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_width = word_width

    if current_line:
        lines.append(' '.join(current_line))

    return '\n'.join(lines)

def save_content_to_pdf(url, title, content, folder_name, index):
    """Save scraped content to a PDF file"""
    file_name = f"page_{index:03d}.pdf"
    file_path = os.path.join(folder_name, file_name)
    
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Clean the title and content
    title = clean_content(title)
    content = clean_content(content)
    
    story.append(Paragraph(f"Title: {title}", styles['Heading1']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"URL: {url}", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Split content into paragraphs and add them to the story
    for paragraph in content.split('\n'):
        if paragraph.strip():
            try:
                # Split long paragraphs
                split_paragraph = split_long_paragraphs(paragraph, 6*inch, 'Helvetica', 10)
                story.append(Paragraph(split_paragraph, styles['Normal']))
                story.append(Spacer(1, 6))
            except Exception as e:
                print(f"Error processing paragraph: {e}")
                continue
    
    try:
        doc.build(story)
    except Exception as e:
        print(f"Error creating PDF for {url}: {e}")

def scrape_links_and_content(base_url, max_depth):
    """Scrape links and content from the base URL and its subpages up to max_depth"""
    visited = set()
    to_visit = {base_url}
    all_links = set()
    company_name = get_company_name(base_url)
    folder_name = f"{company_name}_data"
    os.makedirs(folder_name, exist_ok=True)
    pdf_count = 0

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
                pdf_count += 1
                save_content_to_pdf(url, title, content, folder_name, pdf_count)
        to_visit = new_to_visit
        print(f"Depth {depth + 1} completed. Total links found: {len(all_links)}")

    # Process remaining links that weren't visited due to depth limit
    for url in all_links - visited:
        if interrupted:
            break
        print(f"Scraping remaining link: {url}")
        title, content = scrape_page_content(url)
        pdf_count += 1
        save_content_to_pdf(url, title, content, folder_name, pdf_count)

    return all_links, folder_name, pdf_count

# Get user input
base_url = input("Enter the URL of the website you want to scrape: ")
max_depth = int(input("Enter the maximum depth to scrape: "))

# Generate company-specific filename
company_name = get_company_name(base_url)
file_name = f"{company_name}_scraped_links.txt"

# Scrape the website
print(f"Starting to scrape {base_url}...")
all_links, folder_path, pdf_count = scrape_links_and_content(base_url, max_depth)

# Save the links to a file
with open(file_name, "w", encoding='utf-8') as f:
    for link in sorted(all_links):
        f.write(f"{link}\n")

print(f"\nScraped links have been saved to {os.path.abspath(file_name)}")
print(f"Total number of unique links: {len(all_links)}")
print(f"Number of PDFs generated: {pdf_count}")
print(f"Scraped content has been saved to PDF files in: {os.path.abspath(folder_path)}")

if interrupted:
    print("Scraping was interrupted. Progress has been saved.")
