import requests
from bs4 import BeautifulSoup
import json

url = 'https://blog.bytebytego.com/p/ep194-evolution-of-http'
print(f"Fetching and parsing: {url}\n")

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find article content
article = soup.find('article', class_='newsletter-post')
code_snippets = []

if article:
    # Look for code blocks (pre, code tags)
    code_blocks = article.find_all('code')

    for idx, code_block in enumerate(code_blocks):
        # Get the code text
        code_text = code_block.get_text()

        # Try to detect language from class attribute
        language = None
        if code_block.get('class'):
            for cls in code_block.get('class'):
                if cls.startswith('language-'):
                    language = cls.replace('language-', '')
                    break

        code_snippets.append({
            'index': idx,
            'language': language,
            'code': code_text,
            'length': len(code_text)
        })

# Save to JSON
output_file = '_local-testing-data/06_code_snippets.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(code_snippets, f, indent=2, ensure_ascii=False)

print(f"Found {len(code_snippets)} code snippets")
for snippet in code_snippets[:5]:  # Show first 5
    print(f"\nSnippet {snippet['index']}:")
    print(f"  Language: {snippet['language']}")
    print(f"  Length: {snippet['length']} characters")
    print(f"  Preview: {snippet['code'][:100]}...")

print(f"\nSaved to {output_file}")
