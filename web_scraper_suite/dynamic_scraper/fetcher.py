import logging
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
from parser import scroll_and_load
import socket
import random
import time

logger = logging.getLogger(__name__)

try:
    from fake_useragent import UserAgent
    _ua = UserAgent()
except Exception:
    _ua = None

def _get_user_agent():
    if _ua:
        try:
            return _ua.random
        except Exception:
            pass
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def _get_robots_parser(url, timeout=10):
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    robots_url = f"{base_url}/robots.txt"
    rp = RobotFileParser()
    rp.set_url(robots_url)
    try:
        old_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(timeout)
        rp.read()
        socket.setdefaulttimeout(old_timeout)
    except Exception as e:
        logger.warning(f"Could not read robots.txt at {robots_url}: {e}")
        return None
    return rp

def fetch_page(url, headless=True, wait_for=None, timeout=30000, user_agent="MyScraper", retries=3, scroll=False, max_scrolls=10):
    """Fetch a page using Playwright with retries, rotating UA, and optional infinite scroll."""
    if user_agent == "MyScraper":
        user_agent = _get_user_agent()

    rp = _get_robots_parser(url)
    if rp and not rp.can_fetch(user_agent, url):
        logger.info(f"URL disallowed by robots.txt: {url}")
        return None

    for attempt in range(retries):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=headless)
                context = browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    user_agent=user_agent
                )
                page = context.new_page()

                logger.info(f"Navigating to: {url} (attempt {attempt+1}/{retries})")
                time.sleep(random.uniform(1, 3))
                wait_until = "domcontentloaded" if scroll else "networkidle"
                response = page.goto(url, wait_until=wait_until, timeout=timeout)

                if response and response.status >= 400:
                    status = response.status if response else "unknown"
                    logger.error(f"Failed to fetch page. Status code: {status}")
                    browser.close()
                    if status in (429, 500, 502, 503, 504) and attempt < retries - 1:
                        backoff = 2 ** attempt
                        logger.warning(f"Retrying in {backoff}s...")
                        time.sleep(backoff)
                        continue
                    return None

                if wait_for:
                    logger.info(f"Waiting for selector: {wait_for}")
                    page.wait_for_selector(wait_for, timeout=timeout)

                if scroll:
                    logger.info(f"Infinite scroll enabled, scrolling up to {max_scrolls} times...")
                    html = scroll_and_load(page, max_scrolls=max_scrolls)
                else:
                    html = page.content()
                browser.close()
                return html

        except Exception as e:
            logger.error(f"Error fetching page (attempt {attempt+1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                return None

    return None
