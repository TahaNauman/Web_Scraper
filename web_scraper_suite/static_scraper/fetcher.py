import logging
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
import requests
import socket
import random
import time

logger = logging.getLogger(__name__)

# Graceful import of fake_useragent
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

def fetch_page(url, user_agent="MyScraper", referer=None, retries=3):
    """Fetch a page with retries and logging."""
    # Check robots.txt using domain root
    rp = _get_robots_parser(url)
    if rp and not rp.can_fetch(user_agent, url):
        logger.info(f"URL disallowed by robots.txt: {url}")
        return None

    # Use the same UA for consistency
    ua_string = _get_user_agent() if user_agent == "MyScraper" else user_agent

    headers = {
        "User-Agent": ua_string,
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    }

    if referer:
        headers["Referer"] = referer

    for attempt in range(retries):
        try:
            time.sleep(random.uniform(1, 3))
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.text
            elif response.status_code in (429, 500, 502, 503, 504):
                logger.warning(f"Server error {response.status_code}, retrying ({attempt+1}/{retries})...")
                time.sleep(2 ** attempt)
                continue
            else:
                logger.error(f"Failed to fetch page. Status code: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error fetching page (attempt {attempt+1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                return None

    return None
