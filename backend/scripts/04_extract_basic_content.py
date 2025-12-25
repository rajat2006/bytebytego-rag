import requests
from bs4 import BeautifulSoup
import json

url = 'https://blog.bytebytego.com/p/ep194-evolution-of-http'
print(f"Fetching and parsing: {url}\n")

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract title
title_tag = soup.find('h1', class_='post-title')
title = title_tag.get_text(strip=True) if title_tag else None

# Extract main content from article
article = soup.find('article', class_='newsletter-post')
if article:
    # Get all text content from article
    content_html = str(article)
    content_text = article.get_text(separator='\n', strip=True)
else:
    content_html = None
    content_text = None

# Create output data
output = {
    'url': url,
    'title': title,
    'content_length': len(content_text) if content_text else 0,
    'content_text_preview': content_text[:1000] if content_text else None,  # First 1000 chars
}

# Save to JSON
output_file = '_local-testing-data/04_basic_content.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Extracted content:")
print(f"Title: {title}")
print(f"Content length: {output['content_length']} characters")
print(f"\nFirst 500 characters of content:")
print(content_text[:500] if content_text else "No content found")
print(f"\nSaved to {output_file}")
