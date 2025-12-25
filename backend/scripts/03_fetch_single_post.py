import requests

# Use the first URL from our extracted list
url = 'https://blog.bytebytego.com/p/ep194-evolution-of-http'

print(f"Fetching blog post from {url}...")
response = requests.get(url)

print(f"Status code: {response.status_code}")
print(f"Content length: {len(response.text)} characters")

# Save to file
output_file = '_local-testing-data/03_single_post.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(response.text)

print(f"Saved to {output_file}")
print("\nNow you can inspect the HTML to identify:")
print("- Title location (h1, meta tags?)")
print("- Main content container (article, div?)")
print("- Code blocks (pre, code tags?)")
print("- Images (img tags, where?)")
print("- Metadata (date, author location?)")
