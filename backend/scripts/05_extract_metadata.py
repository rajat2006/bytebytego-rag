import requests
from bs4 import BeautifulSoup
import json
import re

url = 'https://blog.bytebytego.com/p/ep194-evolution-of-http'
print(f"Fetching and parsing: {url}\n")

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract metadata from JSON-LD
metadata = {}
json_ld_script = soup.find('script', type='application/ld+json')
if json_ld_script:
    json_data = json.loads(json_ld_script.string)
    metadata['headline'] = json_data.get('headline')
    metadata['description'] = json_data.get('description')
    metadata['date_published'] = json_data.get('datePublished')
    metadata['date_modified'] = json_data.get('dateModified')

    # Extract author info
    authors = json_data.get('author', [])
    if authors:
        metadata['author'] = authors[0].get('name')
        metadata['author_url'] = authors[0].get('url')

# Extract engagement metrics (likes, comments, etc.)
like_button = soup.find('button', {'aria-label': re.compile(r'Like \((\d+)\)')})
if like_button:
    likes_match = re.search(r'Like \((\d+)\)', like_button.get('aria-label', ''))
    if likes_match:
        metadata['likes'] = int(likes_match.group(1))

comment_button = soup.find('button', {'aria-label': re.compile(r'View comments \((\d+)\)')})
if comment_button:
    comments_match = re.search(r'View comments \((\d+)\)', comment_button.get('aria-label', ''))
    if comments_match:
        metadata['comments'] = int(comments_match.group(1))

# Save to JSON
output_file = '_local-testing-data/05_metadata.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print("Extracted metadata:")
for key, value in metadata.items():
    print(f"  {key}: {value}")
print(f"\nSaved to {output_file}")
