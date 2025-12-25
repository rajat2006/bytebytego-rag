"""
ByteByteGo Blog Post Scraper Module

This module provides functions to scrape blog posts from blog.bytebytego.com
and extract clean text, metadata, images, and code snippets.
"""

import requests
from bs4 import BeautifulSoup
import json
import re


def fetch_html(url):
    """
    Fetch HTML content from a URL.

    Args:
        url (str): The URL to fetch

    Returns:
        BeautifulSoup: Parsed HTML content
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise error for bad status codes
    return BeautifulSoup(response.text, 'html.parser')


def extract_title(soup):
    """
    Extract the post title from HTML.

    Args:
        soup (BeautifulSoup): Parsed HTML content

    Returns:
        str: Post title, or None if not found
    """
    title_tag = soup.find('h1', class_='post-title')
    return title_tag.get_text(strip=True) if title_tag else None


def extract_content_text(soup):
    """
    Extract clean post content (text only, no HTML).

    Args:
        soup (BeautifulSoup): Parsed HTML content

    Returns:
        str: Clean post text, or None if not found
    """
    # Find the main content body div
    body_div = soup.find('div', class_='body markup')

    if body_div:
        # Extract text with newlines preserved
        return body_div.get_text(separator='\n', strip=True)

    return None


def extract_metadata(soup):
    """
    Extract metadata (author, date, description, engagement metrics).

    Args:
        soup (BeautifulSoup): Parsed HTML content

    Returns:
        dict: Metadata including author, dates, likes, comments
    """
    metadata = {}

    # Extract from JSON-LD structured data
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
        except json.JSONDecodeError:
            pass

    # Extract engagement metrics (likes)
    like_button = soup.find('button', {'aria-label': re.compile(r'Like \((\d+)\)')})
    if like_button:
        likes_match = re.search(r'Like \((\d+)\)', like_button.get('aria-label', ''))
        if likes_match:
            metadata['likes'] = int(likes_match.group(1))

    # Extract engagement metrics (comments)
    comment_button = soup.find('button', {'aria-label': re.compile(r'View comments \((\d+)\)')})
    if comment_button:
        comments_match = re.search(r'View comments \((\d+)\)', comment_button.get('aria-label', ''))
        if comments_match:
            metadata['comments'] = int(comments_match.group(1))

    return metadata


def extract_code_snippets(soup):
    """
    Extract code blocks from the post.

    Args:
        soup (BeautifulSoup): Parsed HTML content

    Returns:
        list: List of code snippets with language and code text
    """
    code_snippets = []
    article = soup.find('article', class_='newsletter-post')

    if article:
        code_blocks = article.find_all('code')

        for idx, code_block in enumerate(code_blocks):
            code_text = code_block.get_text()

            # Try to detect programming language from CSS class
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

    return code_snippets


def extract_images(soup):
    """
    Extract images (diagrams, screenshots) from the post.
    Filters out small images like icons and avatars.

    Args:
        soup (BeautifulSoup): Parsed HTML content

    Returns:
        list: List of images with URLs and metadata
    """
    images = []
    article = soup.find('article', class_='newsletter-post')

    if article:
        img_tags = article.find_all('img')

        for idx, img in enumerate(img_tags):
            width = img.get('width')
            height = img.get('height')

            # Filter out small images (icons, avatars, etc.)
            if width and height:
                try:
                    if int(width) < 100 or int(height) < 100:
                        continue  # Skip small images
                except ValueError:
                    pass

            images.append({
                'index': idx,
                'src': img.get('src'),
                'alt': img.get('alt'),
                'title': img.get('title'),
                'width': width,
                'height': height,
            })

    return images


def extract_post(url):
    """
    Main function to extract all data from a blog post.
    Combines all extraction functions to get complete post data.

    Args:
        url (str): URL of the blog post to scrape

    Returns:
        dict: Complete post data including title, content, metadata, code, images

    Example:
        post = extract_post('https://blog.bytebytego.com/p/some-post')
        print(post['title'])
        print(post['content_text'][:100])
    """
    # Fetch and parse HTML
    soup = fetch_html(url)

    # Extract all components
    post_data = {
        'url': url,
        'title': extract_title(soup),
        'content_text': extract_content_text(soup),
        'metadata': extract_metadata(soup),
        'code_snippets': extract_code_snippets(soup),
        'images': extract_images(soup)
    }

    return post_data


# Example usage
if __name__ == '__main__':
    # Test the scraper on a sample post
    test_url = 'https://blog.bytebytego.com/p/ep194-evolution-of-http'
    print(f"Testing scraper on: {test_url}\n")

    post = extract_post(test_url)

    print(f"Title: {post['title']}")
    print(f"Author: {post['metadata'].get('author')}")
    print(f"Published: {post['metadata'].get('date_published')}")
    print(f"Content length: {len(post['content_text'])} characters")
    print(f"Images: {len(post['images'])}")
    print(f"Code snippets: {len(post['code_snippets'])}")
    print(f"Likes: {post['metadata'].get('likes')}")
    print(f"Comments: {post['metadata'].get('comments')}")
