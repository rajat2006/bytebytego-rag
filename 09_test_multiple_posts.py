import json
import time
import sys
sys.path.insert(0, '.')

# Import the extractor (we'll use the function from 08_complete_post_extractor.py)
import importlib.util
spec = importlib.util.spec_from_file_location("extractor", "08_complete_post_extractor.py")
extractor_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extractor_module)
extract_post = extractor_module.extract_post

# Load URLs
with open('_local-testing-data/02_urls.json', 'r') as f:
    all_urls = json.load(f)

# Select diverse test posts (spread across the list)
test_indices = [0, 30, 60, 100, 150, 197]  # Last index is 197 since we have 198 posts
test_urls = [all_urls[i]['url'] for i in test_indices if i < len(all_urls)]

print(f"Testing extractor on {len(test_urls)} diverse posts...\n")

results = []
errors = []

for i, url in enumerate(test_urls, 1):
    try:
        print(f"[{i}/{len(test_urls)}] Processing: {url}")
        post = extract_post(url)

        # Save individual post
        slug = url.split('/p/')[-1]
        output_file = f'_local-testing-data/09_post_{i}_{slug[:30]}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(post, f, indent=2, ensure_ascii=False)

        # Collect summary
        results.append({
            'url': url,
            'title': post['title'],
            'content_length': len(post['content_text']) if post['content_text'] else 0,
            'images': len(post['images']),
            'code_snippets': len(post['code_snippets']),
            'has_metadata': bool(post['metadata']),
            'success': True
        })

        print(f"  ✓ Success: {post['title'][:60]}")
        print(f"    Content: {len(post['content_text'])} chars, Images: {len(post['images'])}, Code: {len(post['code_snippets'])}\n")

        # Rate limiting
        time.sleep(1)

    except Exception as e:
        print(f"  ✗ Error: {str(e)}\n")
        errors.append({'url': url, 'error': str(e)})
        results.append({
            'url': url,
            'success': False,
            'error': str(e)
        })

# Save summary
summary = {
    'total_tested': len(test_urls),
    'successful': len([r for r in results if r.get('success')]),
    'failed': len(errors),
    'results': results,
    'errors': errors
}

output_file = '_local-testing-data/09_test_summary.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

# Print final summary
print("\n" + "="*60)
print("TEST SUMMARY")
print("="*60)
print(f"Total posts tested: {summary['total_tested']}")
print(f"Successful: {summary['successful']}")
print(f"Failed: {summary['failed']}")
print(f"Success rate: {(summary['successful']/summary['total_tested']*100):.1f}%")
print(f"\nDetailed summary saved to {output_file}")
