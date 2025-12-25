# ByteByteGo RAG System - Implementation Plan

## Project Overview
Build a Retrieval-Augmented Generation (RAG) system for the ByteByteGo blog that:
1. Scrapes blog posts from blog.bytebytego.com
2. Ingests data into Qdrant vector database
3. Enables semantic search and question answering

## Tech Stack
- **Scraping (Python)**: BeautifulSoup + requests
- **Vector Database**: Qdrant (free tier)
- **Embeddings**: OpenAI (text-embedding-3-small)
- **LLM**: OpenAI GPT-4/GPT-3.5-turbo
- **API (TypeScript/Node.js)**: REST API (later phase)

## Strategy
**Incremental development approach:**
1. Build as simple Python scripts first
2. Inspect HTML structure at each step
3. Save outputs to `_local-testing-data/` for analysis
4. Make decisions based on actual data
5. Refactor into proper structure later

---

## Discovered Information

### Website Structure
- **Blog URL**: https://blog.bytebytego.com (Substack platform)
- **Post URL Pattern**: `/p/[slug]`
- **Sitemap Structure**:
  - Index: `/sitemap`
  - Yearly: `/sitemap/2025`, `/sitemap/2024`, etc.
  - Total: ~500+ posts across 2021-2025 (194 in 2025 alone)

### Content to Extract
- Title and main content (essential)
- Metadata (date, author, tags, engagement metrics)
- Code snippets (preserve separately)
- Images/diagrams (URLs and descriptions)

### Technical Approach
- Substack pages are HTML-based (easier to scrape)
- Can use BeautifulSoup + requests (no headless browser needed)
- Sitemap provides all URLs upfront (no complex crawling logic needed)

---

## Phase 1: Incremental Script Development

### Step 1.1: Fetch Single Sitemap HTML
**Script: `01_fetch_sitemap.py`**

**Goal:** Fetch one sitemap and save raw HTML to inspect structure

```python
import requests

# Fetch 2025 sitemap
response = requests.get('https://blog.bytebytego.com/sitemap/2025')
with open('_local-testing-data/01_sitemap_2025.html', 'w') as f:
    f.write(response.text)
```

**Output:** `_local-testing-data/01_sitemap_2025.html`
**Analysis:** Inspect HTML to find URL patterns and structure

---

### Step 1.2: Extract URLs from Sitemap
**Script: `02_extract_urls.py`**

**Goal:** Parse sitemap HTML and extract all post URLs

```python
import requests
from bs4 import BeautifulSoup
import json

# Fetch and parse sitemap
response = requests.get('https://blog.bytebytego.com/sitemap/2025')
soup = BeautifulSoup(response.text, 'html.parser')

# Extract URLs (inspect HTML to determine correct selectors)
# Save extracted URLs
```

**Output:** `_local-testing-data/02_urls.json`
**Analysis:** Verify all URLs are correct and complete

---

### Step 1.3: Fetch Single Blog Post HTML
**Script: `03_fetch_single_post.py`**

**Goal:** Fetch one blog post and save raw HTML to inspect structure

```python
import requests

# Use first URL from previous step
url = 'https://blog.bytebytego.com/p/ep194-evolution-of-http'
response = requests.get(url)

with open('_local-testing-data/03_single_post.html', 'w') as f:
    f.write(response.text)
```

**Output:** `_local-testing-data/03_single_post.html`
**Analysis:** Study HTML structure to identify:
- Title location (h1, meta tags?)
- Main content container (article, div?)
- Code blocks (pre, code tags?)
- Images (img tags, where?)
- Metadata (date, author location?)

---

### Step 1.4: Extract Title and Content
**Script: `04_extract_basic_content.py`**

**Goal:** Extract basic content (title, main text) from single post

```python
import requests
from bs4 import BeautifulSoup
import json

url = 'https://blog.bytebytego.com/p/ep194-evolution-of-http'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Based on HTML analysis, extract:
# - Title
# - Main content
# Save as JSON
```

**Output:** `_local-testing-data/04_basic_content.json`
**Analysis:** Verify title and content are correctly extracted

---

### Step 1.5: Extract Metadata
**Script: `05_extract_metadata.py`**

**Goal:** Extract metadata (date, author, tags) from single post

```python
# Based on previous HTML analysis
# Extract: published_date, author, tags, etc.
```

**Output:** `_local-testing-data/05_metadata.json`
**Analysis:** Verify metadata extraction

---

### Step 1.6: Extract Code Snippets
**Script: `06_extract_code_snippets.py`**

**Goal:** Find and extract code blocks with language detection

```python
# Find all code blocks
# Detect language from class names
# Save structured code snippets
```

**Output:** `_local-testing-data/06_code_snippets.json`
**Analysis:** Verify code preservation and language detection

---

### Step 1.7: Extract Images
**Script: `07_extract_images.py`**

**Goal:** Extract image URLs and metadata (alt text, captions)

```python
# Find all images in main content
# Extract URLs, alt text, captions
# Filter out UI elements
```

**Output:** `_local-testing-data/07_images.json`
**Analysis:** Verify image extraction focuses on content diagrams

---

### Step 1.8: Build Complete Post Extractor
**Script: `08_complete_post_extractor.py`**

**Goal:** Combine all extraction logic into single function

```python
def extract_post(url):
    # Combine all previous extraction logic
    return {
        'url': url,
        'title': ...,
        'content': ...,
        'metadata': ...,
        'code_snippets': ...,
        'images': ...
    }
```

**Output:** `_local-testing-data/08_complete_post.json`
**Analysis:** Verify complete extraction works correctly

---

### Step 1.9: Test on Multiple Posts
**Script: `09_test_multiple_posts.py`**

**Goal:** Test extractor on 5-10 different posts to ensure robustness

```python
# Test URLs from different time periods, topics
# Save each to _local-testing-data/09_post_{i}.json
```

**Output:** `_local-testing-data/09_post_*.json`
**Analysis:** Check for edge cases, missing data, errors

---

### Step 1.10: Build Batch Scraper
**Script: `10_batch_scraper.py`**

**Goal:** Scrape all posts from all years with rate limiting

```python
# Fetch all sitemap URLs (2021-2025)
# For each URL:
#   - Extract post data
#   - Save to file
#   - Rate limit (sleep 1s)
#   - Handle errors
```

**Output:** `_local-testing-data/posts/*.json`
**Analysis:** Monitor progress, check error rate

---

## Phase 2: Refactoring & Production

Once scripts are working and tested:

### Step 2.1: Create Requirements File
```txt
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
```

### Step 2.2: Refactor into Reusable Code
- Combine working scripts into clean modules
- Add error handling and retry logic
- Add progress tracking and logging
- Create final production scraper

---

## Phase 3: Data Processing & Embedding (Future)

### Step 3.1: Text Chunking Strategy
- Implement chunking logic (by section, paragraph, or token limit)
- Ensure chunks maintain context (overlapping windows)
- Preserve metadata for each chunk

### Step 3.2: Generate Embeddings
- Set up OpenAI embedding client
- Create batch processing for chunks
- Implement caching to avoid re-embedding

### Step 3.3: Set Up Qdrant Vector Database
- Install and configure Qdrant (local or cloud)
- Create collection with appropriate schema
- Define vector dimensions (1536 for text-embedding-3-small)

### Step 3.4: Ingest Data into Qdrant
- Create ingestion pipeline
- Batch upload chunks with embeddings and metadata
- Verify data integrity and search functionality

---

## Phase 4: RAG Query System (Future)

### Step 4.1: Implement Semantic Search
- Create search function with Qdrant client
- Implement query embedding generation
- Configure search parameters (top_k, score_threshold)

### Step 4.2: Build RAG Pipeline
- Implement retrieval logic (fetch relevant chunks)
- Create prompt templates for different query types
- Integrate OpenAI GPT for answer generation

### Step 4.3: Add Response Enhancement
- Implement source citation in responses
- Add confidence scoring
- Handle edge cases (no relevant results, ambiguous queries)

---

## Phase 5: API Development (Future)

### Step 5.1: Create REST API Endpoints
- POST /api/query - Main query endpoint
- GET /api/health - Health check
- GET /api/stats - Database statistics

### Step 5.2: Implement API Logic (TypeScript)
- Connect to Python RAG backend or call Qdrant directly
- Add request validation and error handling
- Implement rate limiting

---

## Current Phase: Success Criteria

**Phase 1 Complete When:**
- [ ] Step 1.1-1.3: Successfully extract URLs from sitemaps
- [ ] Step 1.4-1.7: Successfully extract all content types from single post
- [ ] Step 1.8: Build complete extractor for single post
- [ ] Step 1.9: Test on multiple posts, handle edge cases
- [ ] Step 1.10: Successfully scrape all 500+ posts
- [ ] All outputs saved to `_local-testing-data/` for verification
- [ ] Ready for next phase (embedding generation)

---

## Critical Files to Create (Phase 1)

**Incremental scripts (in order):**
1. `01_fetch_sitemap.py`
2. `02_extract_urls.py`
3. `03_fetch_single_post.py`
4. `04_extract_basic_content.py`
5. `05_extract_metadata.py`
6. `06_extract_code_snippets.py`
7. `07_extract_images.py`
8. `08_complete_post_extractor.py`
9. `09_test_multiple_posts.py`
10. `10_batch_scraper.py`

**Output directory:**
- `_local-testing-data/` - All test outputs and scraped data

---

## Notes

- **Rate Limiting**: Respect Substack's servers (1 req/sec max)
- **Error Handling**: Log failures but continue scraping
- **Checkpointing**: Save progress incrementally
- **Resumability**: Can resume from last saved post
- **Extensibility**: Easy to add main website scraping later
