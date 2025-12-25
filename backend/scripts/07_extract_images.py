import requests
from bs4 import BeautifulSoup
import json

url = 'https://blog.bytebytego.com/p/ep194-evolution-of-http'
print(f"Fetching and parsing: {url}\n")

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find article content
article = soup.find('article', class_='newsletter-post')
images = []

if article:
    # Find all images in the article
    img_tags = article.find_all('img')

    for idx, img in enumerate(img_tags):
        # Skip small images (likely icons, avatars, etc.)
        width = img.get('width')
        height = img.get('height')

        # Filter for content images (usually larger)
        if width and height:
            try:
                if int(width) < 100 or int(height) < 100:
                    continue  # Skip small images
            except:
                pass

        images.append({
            'index': idx,
            'src': img.get('src'),
            'alt': img.get('alt'),
            'title': img.get('title'),
            'width': width,
            'height': height,
        })

# Save to JSON
output_file = '_local-testing-data/07_images.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(images, f, indent=2, ensure_ascii=False)

print(f"Found {len(images)} content images (filtered out small icons)")
for image in images:
    print(f"\nImage {image['index']}:")
    print(f"  Alt: {image['alt']}")
    print(f"  Size: {image['width']}x{image['height']}")
    print(f"  URL: {image['src'][:80]}...")

print(f"\nSaved to {output_file}")
