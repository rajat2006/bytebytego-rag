import requests
from bs4 import BeautifulSoup
import json
import re

def extract_post(url):
    """
    Extract complete post data including:
    - Title
    - Content
    - Metadata (author, date, description, engagement)
    - Code snippets
    - Images
    """
    print(f"Extracting: {url}")

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize result
    post_data = {'url': url}

    # Extract title
    title_tag = soup.find('h1', class_='post-title')
    post_data['title'] = title_tag.get_text(strip=True) if title_tag else None

    # Extract main content from the actual post body
    article = soup.find('article', class_='newsletter-post')

    # Find the actual content body (not the full article with UI elements)
    body_div = soup.find('div', class_='body markup') if article else None

    if body_div:
        # Extract only clean text, no HTML
        post_data['content_text'] = body_div.get_text(separator='\n', strip=True)
    else:
        post_data['content_text'] = None

    # Keep reference to full article for extracting images/code
    article = article if article else soup

    # Extract metadata from JSON-LD
    metadata = {}
    json_ld_script = soup.find('script', type='application/ld+json')
    if json_ld_script:
        try:
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
        except:
            pass

    # Extract engagement metrics
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

    post_data['metadata'] = metadata

    # Extract code snippets
    code_snippets = []
    if article:
        code_blocks = article.find_all('code')
        for idx, code_block in enumerate(code_blocks):
            code_text = code_block.get_text()
            language = None
            if code_block.get('class'):
                for cls in code_block.get('class'):
                    if cls.startswith('language-'):
                        language = cls.replace('language-', '')
                        break
            code_snippets.append({
                'index': idx,
                'language': language,
                'code': code_text
            })
    post_data['code_snippets'] = code_snippets

    # Extract images
    images = []
    if article:
        img_tags = article.find_all('img')
        for idx, img in enumerate(img_tags):
            # Skip small images
            width = img.get('width')
            height = img.get('height')
            if width and height:
                try:
                    if int(width) < 100 or int(height) < 100:
                        continue
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
    post_data['images'] = images

    return post_data


# Test the extractor
if __name__ == '__main__':
    url = 'https://blog.bytebytego.com/p/ep194-evolution-of-http'
    post = extract_post(url)

    # Save to JSON
    output_file = '_local-testing-data/08_complete_post.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(post, f, indent=2, ensure_ascii=False)

    # Print summary
    print(f"\nExtraction Summary:")
    print(f"  Title: {post['title']}")
    print(f"  Author: {post['metadata'].get('author')}")
    print(f"  Date: {post['metadata'].get('date_published')}")
    print(f"  Content length: {len(post['content_text']) if post['content_text'] else 0} chars")
    print(f"  Code snippets: {len(post['code_snippets'])}")
    print(f"  Images: {len(post['images'])}")
    print(f"  Likes: {post['metadata'].get('likes')}")
    print(f"  Comments: {post['metadata'].get('comments')}")
    print(f"\nSaved to {output_file}")
