# ByteByteGo RAG System

A Retrieval-Augmented Generation (RAG) system for ByteByteGo blog content, enabling intelligent search and question-answering over the entire ByteByteGo knowledge base.

## Project Structure

This is a mono-repo containing three main components:

```
bytebytego-rag/
├── backend/          # Web scraping and data processing
├── frontend/         # User interface (coming soon)
└── rag-backend/      # RAG pipeline and vector database (coming soon)
```

## Backend

The backend handles scraping blog posts from blog.bytebytego.com (500+ posts from 2021-2025) and processing them for the RAG system.

See [backend/README.md](backend/README.md) for details.

## Quick Start

### Prerequisites

- Python 3.x
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/rajat2006/bytebytego-rag.git
cd bytebytego-rag
```

2. Install dependencies:
```bash
pip install requests beautifulsoup4 python-dotenv
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env as needed
```

### Running the Scraper

```bash
cd backend
python batch_scrape.py
```

## Configuration

Configuration is managed through `.env` file in the root directory:

- `DEBUG_FILE_LOGS` - Set to `true` to save scraped data to files, `false` for production mode
- `RATE_LIMIT` - Seconds to wait between requests (default: 1.0)

## Development

This project uses an incremental development approach with test scripts in `backend/scripts/` for each stage of development.

## License

MIT
