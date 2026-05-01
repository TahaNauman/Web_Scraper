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
    parser = argparse.ArgumentParser(description="Static Web Scraper")
    parser.add_argument("--urls", nargs="+", help="Starting URLs separated by spaces")
    parser.add_argument("--tags", nargs="+", help="HTML tags to extract (e.g., h1 p img a)")
    parser.add_argument("--max-pages", type=int, default=1, help="Max pages to scrape per URL (default 1)")
    parser.add_argument("--output", default="output.json", help="Output filename (default: output.json)")
    parser.add_argument("--no-csv", action="store_true", help="Disable CSV export")
    parser.add_argument("--deduplicate", action="store_true", help="Remove duplicate entries from results")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Fallback to interactive mode if no URLs provided
    if args.urls:
        urls = [url.strip() for url in args.urls]
    else:
        urls_input = input("Enter starting URLs separated by commas: ").split(",")
        urls = [url.strip() for url in urls_input]

    max_pages = args.max_pages

    combined_results = {}

    for start_url in urls:
        current_url = start_url
        pages_count = 0
        selected_tags = []
        visited_urls = set()

        while current_url and pages_count < max_pages:
            if current_url in visited_urls:
                logger.warning(f"Already visited {current_url}, stopping to avoid loop.")
                break
            visited_urls.add(current_url)

            logger.info(f"Scraping Page {pages_count + 1}: {current_url}")

            referer_url = None if pages_count == 0 else current_url
            html = fetch_page(current_url, referer=referer_url)

            if not html:
                break

            if pages_count == 0:
                available_tags = get_all_tags(html)
                logger.info(f"Available Tags: {', '.join(available_tags)}")
                if args.tags:
                    selected_tags = [t.strip() for t in args.tags]
                else:
                    tag_input = input("Select tags to extract (e.g., h1, p, img, a): ").split(",")
                    selected_tags = [t.strip() for t in tag_input]

            extracted = extract_tags(html, selected_tags, current_url)

            for tag, items in extracted.items():
                if tag not in combined_results:
                    combined_results[tag] = []
                combined_results[tag].extend(items)

            next_url = find_next_page(html, current_url)
            pages_count += 1

            if next_url and pages_count < max_pages:
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
        logger.warning("No data was extracted. Check your URLs or robots.txt permissions.")

if __name__ == "__main__":
    main()
