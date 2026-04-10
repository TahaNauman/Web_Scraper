# ⚡ Static Web Scraper 

This is a modular, high-speed scraper designed to extract text, links, and image sources from static HTML pages.

## ✨ Features
- **Pagination:** Automatically follows "Next" links to scrape multiple pages.
- **Attribute Extraction:** Captures `href` for links and `src` for images.
- **Path Resolution:** Automatically converts relative URLs into absolute, clickable links.
- **Human-Like Behavior:** Uses randomized delays and `Referer` headers to avoid detection.

## ⚙️ Architecture
- `fetcher.py`: Handles HTTP requests, headers, and `robots.txt`.
- `parser.py`: Logic for tag extraction and pagination navigation.
- `saver.py`: Manages data export to JSON and CSV.
- `main.py`: The orchestrator that manages the scraping loop.

## 🕹️ Usage
1. Navigate to this directory: `cd static_scraper`
2. Install requirements: `pip install -r requirements.txt`
3. Run the script: `python main.py`
