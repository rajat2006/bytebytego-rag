# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ByteByteGo RAG System - A Retrieval-Augmented Generation system for ByteByteGo blog content that enables intelligent search and question-answering over 500+ blog posts from blog.bytebytego.com.

**Mono-repo structure:**
- `backend/` - Web scraping and data processing (active development)
- `frontend/` - User interface (placeholder - coming soon)
- `rag-backend/` - RAG pipeline and vector database (placeholder - coming soon)

## Important Context

**User's Implementation Approach:**
The user is implementing the RAG pipeline themselves. You should act as a helpful assistant. Other parts of the project can be implemented by you, but **only after user approval for each step**.

This project follows an **incremental development approach** - build simple scripts first, inspect outputs in `_local-testing-data/`, make decisions based on actual data, then refactor.

## Running the Scraper

All scraper commands should be run from the `backend/` directory:

```bash
cd backend

# Run batch scraper to collect all blog posts (500+)
python batch_scrape.py

# Test scraper module on a single post
python scraper.py
```

## Configuration

Environment variables are in root `.env` (copy from `.env.example`):

- `DEBUG_FILE_LOGS=true` - Save scraped data to `_local-testing-data/` for inspection
- `DEBUG_FILE_LOGS=false` - Production mode (no debug files written)
- `RATE_LIMIT=1.0` - Seconds between requests (respect the server)

## Architecture

### Backend Scraping Architecture

**Core Modules:**
- `backend/scraper.py` - Reusable extraction functions (7 functions)
- `backend/batch_scrape.py` - Batch scraping orchestration

**Key Design Pattern:**
The scraper uses a modular extraction pattern where `scraper.py` provides low-level extraction functions, and `batch_scrape.py` orchestrates the batch collection process.

**Critical Path Resolution:**
- `batch_scrape.py` uses **script-relative paths** to find `_local-testing-data/` in project root
- Calculates `project_root = Path(__file__).resolve().parent.parent`
- This allows the script to work regardless of working directory
- Always run from `backend/` directory for imports to work: `from scraper import extract_post`

**scraper.py Functions:**
1. `fetch_html(url)` - Fetch and parse HTML with BeautifulSoup
2. `extract_title(soup)` - Extract post title from `<h1 class='post-title'>`
3. `extract_content_text(soup)` - Extract clean text from `<div class='body markup'>`
4. `extract_metadata(soup)` - Extract JSON-LD structured data (author, dates, likes, comments)
5. `extract_code_snippets(soup)` - Extract `<code>` blocks with language detection
6. `extract_images(soup)` - Extract images, filtering small ones (<100px)
7. `extract_post(url)` - Main function combining all extractions

**batch_scrape.py Functions:**
1. `collect_urls_from_sitemap(year)` - Fetch URLs from yearly sitemap
2. `collect_all_urls()` - Collect from all years (2021-2025), deduplicate
3. `save_post(post_data, output_dir, save_enabled)` - Save individual post JSON
4. `scrape_all_posts(urls, output_dir, rate_limit, save_enabled)` - Main scraping loop with resumability
5. `main()` - Orchestration with env var configuration

**Data Flow:**
```
Sitemaps (2021-2025) → collect_all_urls() → scrape_all_posts() → extract_post() → JSON files
                                                                           ↓
                                                    _local-testing-data/posts/[slug].json
```

### Incremental Development Scripts

`backend/scripts/` contains 9 test scripts (01-09) used during development:
- Each script explores one aspect of scraping (sitemap, URLs, content, metadata, etc.)
- Outputs saved to `_local-testing-data/` for inspection
- These are **development artifacts** - not used in production
- Script 09 tests extraction on 6 diverse posts for validation

## File Path Patterns

**Substack URL Pattern:**
- Blog: `https://blog.bytebytego.com`
- Posts: `/p/[slug]` (e.g., `/p/ep194-evolution-of-http`)
- Sitemaps: `/sitemap/[year]` (e.g., `/sitemap/2025`)

**HTML Selectors (Substack-specific):**
- Title: `<h1 class='post-title'>`
- Content: `<div class='body markup'>` (main content only, no UI)
- Article container: `<article class='newsletter-post'>`
- Metadata: `<script type='application/ld+json'>` (JSON-LD structured data)

## Tech Stack

**Current (Backend):**
- Python 3.x
- BeautifulSoup4 - HTML parsing
- requests - HTTP client
- python-dotenv - Environment variables

**Planned (RAG Pipeline):**
- Qdrant - Vector database (free tier)
- OpenAI text-embedding-3-small - Embeddings
- OpenAI GPT-4/GPT-3.5-turbo - Question answering

## Development Workflow

1. **Testing changes to scraper:**
   ```bash
   cd backend
   python scraper.py  # Tests on single post
   ```

2. **Testing batch scraper:**
   ```bash
   cd backend
   # Set DEBUG_FILE_LOGS=false for dry-run (no files saved)
   python batch_scrape.py
   ```

3. **Inspecting scraped data:**
   ```bash
   ls _local-testing-data/posts/  # Individual post JSONs
   cat _local-testing-data/all_urls.json  # All collected URLs
   cat _local-testing-data/scraping_summary.json  # Success/failure stats
   ```

## Important Notes

- **Rate limiting:** Default 1 req/sec. Scraping all 500+ posts takes ~10 minutes
- **Resumability:** batch_scrape.py skips already-scraped posts (checks for existing JSON files)
- **Clean text only:** Content is stored as clean text (`content_text`), not HTML
- **Image filtering:** Images smaller than 100x100px are filtered out (icons, avatars)
- **Output location:** `_local-testing-data/` is gitignored and always in project root

## Future Phases

See `backend/IMPLEMENTATION_PLAN.md` for full plan:
- Phase 2: Qdrant vector database setup
- Phase 3: Generate embeddings with OpenAI
- Phase 4: RAG query system
- Phase 5: API layer (TypeScript/Node.js)
