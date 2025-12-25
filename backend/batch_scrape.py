"""
Batch Scraper for ByteByteGo Blog Posts

This script scrapes all blog posts from blog.bytebytego.com (2021-2025)
and saves them as individual JSON files.
"""

import json
import time
import os
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import our scraper module
from scraper import extract_post


def collect_urls_from_sitemap(year):
    """
    Collect all post URLs from a specific year's sitemap.

    Args:
        year (int): The year to fetch (e.g., 2021, 2022, etc.)

    Returns:
        list: List of dicts with 'url', 'title', and 'year'
    """
    url = f'https://blog.bytebytego.com/sitemap/{year}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    posts = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        # Only collect blog post URLs (contain /p/)
        if '/p/' in href and 'blog.bytebytego.com' in href:
            title = link.get_text(strip=True)
            posts.append({
                'url': href,
                'title': title,
                'year': year
            })

    return posts


def collect_all_urls():
    """
    Collect all post URLs from all years (2021-2025).
    Removes duplicates and returns unique posts.

    Returns:
        list: List of unique post URLs with metadata
    """
    all_posts = []
    years = [2021, 2022, 2023, 2024, 2025]

    for year in years:
        print(f"Fetching sitemap for {year}...")
        posts = collect_urls_from_sitemap(year)
        all_posts.extend(posts)
        print(f"  Found {len(posts)} posts")

    # Remove duplicates based on URL
    seen_urls = set()
    unique_posts = []
    for post in all_posts:
        if post['url'] not in seen_urls:
            seen_urls.add(post['url'])
            unique_posts.append(post)

    return unique_posts


def save_post(post_data, output_dir, save_enabled=True):
    """
    Save a single post as a JSON file (only if save_enabled is True).

    Args:
        post_data (dict): Post data from extract_post()
        output_dir (Path): Directory to save the file
        save_enabled (bool): Whether to actually save files (from env SAVE_TO_FILE)

    Returns:
        str: Path to the saved file (or would-be path if not saving)
    """
    # Extract slug from URL for filename
    slug = post_data['url'].split('/p/')[-1]
    output_file = output_dir / f"{slug}.json"

    # Only save if flag is enabled
    if save_enabled:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(post_data, f, indent=2, ensure_ascii=False)

    return output_file


def scrape_all_posts(urls, output_dir, rate_limit=1.0, save_enabled=True):
    """
    Scrape all posts and save them to individual JSON files.

    Args:
        urls (list): List of URL dicts to scrape
        output_dir (Path): Directory to save scraped posts
        rate_limit (float): Seconds to wait between requests (default: 1.0)
        save_enabled (bool): Whether to save files (from env SAVE_TO_FILE)

    Returns:
        dict: Summary with success/failure counts and errors
    """
    success_count = 0
    error_count = 0
    errors = []

    for i, url_data in enumerate(urls, 1):
        url = url_data['url']
        slug = url.split('/p/')[-1]

        # Check if already scraped (for resumability) - only if saving is enabled
        output_file = output_dir / f"{slug}.json"
        if save_enabled and output_file.exists():
            print(f"[{i}/{len(urls)}] ⏭️  Skipped (already exists): {slug}")
            success_count += 1
            continue

        try:
            mode = "DRY-RUN" if not save_enabled else "SCRAPING"
            print(f"[{i}/{len(urls)}] 📥 {mode}: {slug}")

            # Extract post data using our scraper module
            post_data = extract_post(url)

            # Save to file (only if enabled)
            save_post(post_data, output_dir, save_enabled=save_enabled)

            success_count += 1
            content_len = len(post_data['content_text']) if post_data['content_text'] else 0
            save_status = "Saved" if save_enabled else "Extracted"
            print(f"    ✓ {save_status} ({content_len} chars, {len(post_data['images'])} images)")

            # Rate limiting - be respectful to the server
            time.sleep(rate_limit)

        except Exception as e:
            error_count += 1
            error_msg = str(e)
            errors.append({
                'url': url,
                'slug': slug,
                'error': error_msg
            })
            print(f"    ✗ Error: {error_msg}")

    return {
        'total': len(urls),
        'successful': success_count,
        'failed': error_count,
        'errors': errors
    }


def main():
    """
    Main execution function for batch scraping.
    """
    # Read environment variables
    debug_file_logs = os.getenv('DEBUG_FILE_LOGS', 'true').lower() == 'true'
    rate_limit = float(os.getenv('RATE_LIMIT', '1.0'))

    # Calculate project root (parent of backend directory)
    script_dir = Path(__file__).resolve().parent  # /path/to/backend
    project_root = script_dir.parent  # /path/to/project

    print("="*60)
    print("ByteByteGo Batch Scraper")
    print("="*60)
    print(f"Debug file logs: {debug_file_logs}")
    print(f"Rate limit: {rate_limit}s")
    print("="*60)

    # Setup output directory
    output_dir = project_root / '_local-testing-data' / 'posts'
    if debug_file_logs:
        output_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Collect all URLs
    print("\n[Step 1/3] Collecting URLs from sitemaps (2021-2025)...")
    all_urls = collect_all_urls()
    print(f"\n✓ Total unique posts found: {len(all_urls)}")

    # Save URL list for reference (only if debug logging is enabled)
    urls_file = project_root / '_local-testing-data' / 'all_urls.json'
    if debug_file_logs:
        with open(urls_file, 'w', encoding='utf-8') as f:
            json.dump(all_urls, f, indent=2, ensure_ascii=False)
        print(f"✓ URL list saved to: {urls_file}")
    else:
        print(f"✓ URL list collected (not saved - debug logs disabled)")

    # Step 2: Scrape all posts
    print(f"\n[Step 2/3] Scraping {len(all_urls)} posts...")
    if debug_file_logs:
        print("(This will take ~10 minutes with 1 req/sec rate limit)\n")
    else:
        print("(DEBUG_FILE_LOGS=false - no files will be saved)\n")

    summary = scrape_all_posts(all_urls, output_dir, rate_limit=rate_limit, save_enabled=debug_file_logs)

    # Step 3: Save summary report (only if debug logging is enabled)
    print(f"\n[Step 3/3] Generating summary report...")
    summary_file = project_root / '_local-testing-data' / 'scraping_summary.json'
    if debug_file_logs:
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
    else:
        print("(Summary not saved - debug logs disabled)")

    # Print final results
    print("\n" + "="*60)
    print("SCRAPING COMPLETE")
    print("="*60)
    print(f"Total posts: {summary['total']}")
    print(f"Successful: {summary['successful']}")
    print(f"Failed: {summary['failed']}")
    success_rate = (summary['successful'] / summary['total'] * 100) if summary['total'] > 0 else 0
    print(f"Success rate: {success_rate:.1f}%")

    if debug_file_logs:
        print(f"\nOutput directory: {output_dir}")
        print(f"Summary report: {summary_file}")
    else:
        print(f"\n(Debug logs disabled - no files were saved)")


if __name__ == '__main__':
    main()
