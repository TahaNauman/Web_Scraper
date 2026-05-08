import argparse
import logging
from fetcher import fetch_page
from parser import get_all_tags, extract_tags, find_next_page
from saver import save_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Dynamic Web Scraper (Playwright)")
    parser.add_argument("--urls", nargs="+", help="Starting URLs (space-separated)")
    parser.add_argument("--tags", nargs="+", help="HTML tags to extract (e.g., h1 p img a)")
    parser.add_argument("--max-pages", type=int, default=1, help="Max pages to scrape per URL (default: 1)")
    parser.add_argument("--output", default="output.json", help="Output filename (default: output.json)")
    parser.add_argument("--no-csv", action="store_true", help="Disable CSV export")
    parser.add_argument("--deduplicate", action="store_true", help="Remove duplicate entries from results")
    parser.add_argument("--headless", action="store_true", default=True, help="Run browser in headless mode (default: True)")
    parser.add_argument("--no-headless", action="store_true", help="Show browser window for debugging")
    parser.add_argument("--wait-for", help="CSS selector to wait for before scraping")
    parser.add_argument("--timeout", type=int, default=30000, help="Page load timeout in ms (default: 30000)")
    parser.add_argument("--scroll", action="store_true", help="Enable infinite scroll mode")
    parser.add_argument("--max-scrolls", type=int, default=10, help="Max scrolls for infinite scroll (default: 10)")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    headless = not args.no_headless and args.headless

    if args.urls:
        urls = [url.strip() for url in args.urls]
    else:
        urls_input = input("Enter URLs separated by commas: ").split(",")
        urls = [url.strip() for url in urls_input]

    combined_results = {}

    for start_url in urls:
        current_url = start_url
        pages_count = 0
        selected_tags = []
        visited_urls = set()

        while current_url and pages_count < args.max_pages:
            if current_url in visited_urls:
                logger.warning(f"Already visited {current_url}, stopping to avoid loop.")
                break
            visited_urls.add(current_url)

            logger.info(f"Processing Page {pages_count + 1}: {current_url}")

            html = fetch_page(current_url, headless=headless, wait_for=args.wait_for, timeout=args.timeout, scroll=args.scroll, max_scrolls=args.max_scrolls)

            if not html:
                logger.warning(f"Failed to fetch: {current_url}")
                break

            if pages_count == 0:
                available_tags = get_all_tags(html)
                logger.info(f"Available Tags: {', '.join(available_tags)}")
                if args.tags:
                    selected_tags = [t.strip() for t in args.tags]
                else:
                    tag_input = input("Enter comma-separated tags to extract: ").split(",")
                    selected_tags = [t.strip() for t in tag_input]

            extracted = extract_tags(html, selected_tags, base_url=current_url)

            for tag, items in extracted.items():
                if tag not in combined_results:
                    combined_results[tag] = []
                combined_results[tag].extend(items)

            pages_count += 1

            if args.scroll:
                current_url = None
            else:
                next_url = find_next_page(html, current_url)
                if next_url and pages_count < args.max_pages:
                    if next_url == current_url or next_url in visited_urls:
                        current_url = None
                    else:
                        current_url = next_url
                        logger.info(f"Next page found. Moving to Page {pages_count + 1}...")
                else:
                    current_url = None

    if combined_results:
        save_data(combined_results, filename=args.output, save_csv=not args.no_csv, deduplicate=args.deduplicate)
        logger.info("Scraping Task Complete!")
    else:
        logger.warning("No data was extracted.")

if __name__ == "__main__":
    main()
