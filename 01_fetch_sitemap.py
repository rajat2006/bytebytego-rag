import requests

# Fetch 2025 sitemap
print("Fetching sitemap from https://blog.bytebytego.com/sitemap/2025...")
response = requests.get('https://blog.bytebytego.com/sitemap/2025')

print(f"Status code: {response.status_code}")
print(f"Content length: {len(response.text)} characters")

# Save to file
output_file = '_local-testing-data/01_sitemap_2025.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(response.text)

print(f"Saved to {output_file}")
print("\nFirst 500 characters of the response:")
print(response.text[:500])
