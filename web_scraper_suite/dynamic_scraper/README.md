# Dynamic Web Scraper

A modular, high-speed scraper designed to extract text, links, and image sources from dynamic HTML pages.

##  Features
- **CLI & Interactive Modes:** Use command-line arguments or interactive prompts.
- **Pagination:** Automatically follows "Next" links (supports `rel="next"` and common patterns) across multiple pages.
- **Attribute Extraction:** Captures `href` for links and `src` for images with absolute URL resolution.
- **Human-Like Behavior:** Uses randomized delays, `Referer` headers, and rotating User-Agents.
- **Robots.txt Compliance:** Respects `robots.txt` rules using proper domain-root URL generation and a timeout.
- **Resilient Fetching:** Automatic retries with exponential backoff for transient errors.
- **Deduplication:** Optional removal of duplicate entries in results.
- **Structured Logging:** Replace print statements with configurable logging (use `--verbose` for debug).
- **Infinite Scrolling:** Scrolls up to N times (default: 10, configurable via `--max-scrolls`)

##  Architecture
- `fetcher.py`: HTTP requests, headers, retries, and `robots.txt` handling.
- `parser.py`: Tag extraction, pagination navigation, and URL resolution.
- `saver.py`: Data export to JSON and CSV with optional deduplication.
- `main.py`: Orchestrator managing the scraping loop and CLI arguments.

  ## Usage
1. Navigate to this directory: `cd dynamic_scraper`
2. Install requirements: `pip install -r requirements.txt`
3. Run with CLI arguments:
   ```bash
   python main.py --urls https://example.com --tags h1 p a --no-headless
   ```
   Or run interactively with
  ```bash
  python main.py
  ```

## CLI Options

- `--urls` — Starting URLs (space-separated)
- `--tags` — HTML tags to extract (e.g., `h1 p img a`)
- `--max-pages` — Max pages to scrape per URL (default: 1)
- `--output` — Output filename (default: `output.json`)
- `--no-csv` — Disable CSV export
- `--deduplicate` — Remove duplicate entries from results
- `--headless` — Run browser in headless mode (default: True)
- `--no-headless` — Show browser window for debugging
- `--wait-for` — CSS selector to wait for before scraping
- `--timeout` — Page load timeout in milliseconds (default: 30000)
- `--scroll` — Enable infinite scroll mode
- `--max-scrolls` — Max scrolls for infinite scroll (default: 10)
- `--verbose` — Enable debug logging
