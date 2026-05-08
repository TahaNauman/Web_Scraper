import logging
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

def _get_robots_parser(url):
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    robots_url = f"{base_url}/robots.txt"
    rp = RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
    except Exception as e:
        logger.warning(f"Could not read robots.txt at {robots_url}: {e}")
        return None
    return rp

def fetch_page(url, headless=True, wait_for=None, timeout=30000, user_agent="MyScraper"):
    """Fetch a page using Playwright browser automation."""
    rp = _get_robots_parser(url)
    if rp and not rp.can_fetch(user_agent, url):
        logger.info(f"URL disallowed by robots.txt: {url}")
        return None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = context.new_page()

        try:
            logger.info(f"Navigating to: {url}")
            response = page.goto(url, wait_until="networkidle", timeout=timeout)
            
            if not response or response.status >= 400:
                status = response.status if response else "unknown"
                logger.error(f"Failed to fetch page. Status code: {status}")
                browser.close()
                return None

            if wait_for:
                logger.info(f"Waiting for selector: {wait_for}")
                page.wait_for_selector(wait_for, timeout=timeout)

            html = page.content()
            browser.close()
            return html

        except Exception as e:
            logger.error(f"Error fetching page: {e}")
            browser.close()
            return None
