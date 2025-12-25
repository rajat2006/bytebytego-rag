# Backend

Backend services for ByteByteGo RAG system, including web scraping and data processing.

## Structure

- `scraper.py` - Core module for scraping ByteByteGo blog posts
- `batch_scrape.py` - Batch scraper for collecting all blog posts
- `scripts/` - Incremental development and test scripts

## Usage

### Running the Batch Scraper

```bash
cd backend
python batch_scrape.py
```

### Running the Scraper Module

```bash
cd backend
python scraper.py
```

## Configuration

Configuration is managed through environment variables in the root `.env` file:

- `DEBUG_FILE_LOGS` - Set to `true` to save scraped data to files
- `RATE_LIMIT` - Seconds to wait between requests (default: 1.0)
