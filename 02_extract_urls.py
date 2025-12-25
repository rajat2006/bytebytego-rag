import requests
from bs4 import BeautifulSoup
import json

# Fetch and parse sitemap
print("Fetching sitemap from https://blog.bytebytego.com/sitemap/2025...")
response = requests.get('https://blog.bytebytego.com/sitemap/2025')
soup = BeautifulSoup(response.text, 'html.parser')

# Find all links with /p/ pattern (blog posts)
post_links = []
for link in soup.find_all('a', href=True):
    href = link['href']
    # Check if it's a blog post URL
    if '/p/' in href and 'blog.bytebytego.com' in href:
        # Extract title from link text
        title = link.get_text(strip=True)
        post_links.append({
            'url': href,
            'title': title,
            'year': 2025
        })

# Remove duplicates (same URL might appear multiple times)
seen_urls = set()
unique_posts = []
for post in post_links:
    if post['url'] not in seen_urls:
        seen_urls.add(post['url'])
        unique_posts.append(post)

print(f"\nFound {len(unique_posts)} unique blog posts from 2025")

# Save to JSON
output_file = '_local-testing-data/02_urls.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(unique_posts, f, indent=2, ensure_ascii=False)

print(f"Saved to {output_file}")

# Display first 10 posts
print("\nFirst 10 posts:")
for i, post in enumerate(unique_posts[:10], 1):
    print(f"{i}. {post['title']}")
    print(f"   {post['url']}")
