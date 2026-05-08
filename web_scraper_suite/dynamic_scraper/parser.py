from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import logging
import time

logger = logging.getLogger(__name__)

def get_all_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    tags = set()
    ignore_tags = ["style", "script", "head", "meta", "link", "noscript"]

    for tag in soup.find_all():
        if tag.name not in ignore_tags:
            tags.add(tag.name)

    return sorted(tags)

def extract_tags(html, selected_tags, base_url=""):
    soup = BeautifulSoup(html, "html.parser")
    results = {}

    for tag in selected_tags:
        elements = soup.find_all(tag)
        extracted = []
        
        for el in elements:
            text = el.get_text(separator=" ", strip=True)
            
            attr_url = None
            if tag == "a":
                attr_url = el.get("href")
            elif tag == "img":
                attr_url = el.get("src")
                if not text:
                    text = el.get("alt", "No description")

            if attr_url and base_url:
                full_url = urljoin(base_url, attr_url)
                extracted.append({"label": text, "url": full_url})
            elif text:
                extracted.append(text)

        results[tag] = extracted

    return results

def find_next_page(html, current_url):
    soup = BeautifulSoup(html, "html.parser")
    
    next_link = soup.find("a", attrs={"rel": re.compile(r"next", re.I)})
    if next_link:
        href = next_link.get("href")
        if href and isinstance(href, str):
            return urljoin(current_url, href)
    
    next_patterns = re.compile(r'next|older|forward|>', re.I)
    
    # Check by text content (use get_text to handle mixed child nodes)
    for a in soup.find_all("a"):
        text = a.get_text(strip=True)
        if text and next_patterns.search(text):
            href = a.get("href")
            if href and isinstance(href, str):
                return urljoin(current_url, href)
    
    # Check by class or id
    # Check <li class="next"> containing <a> (common Bootstrap pagination pattern)
    next_li = soup.find("li", class_=next_patterns)
    if next_li:
        a = next_li.find("a")
        if a:
            href = a.get("href")
            if href and isinstance(href, str):
                return urljoin(current_url, href)

    for a in soup.find_all("a"):
        cls = a.get("class")
        id_attr = a.get("id")
        if cls and any(next_patterns.search(c) for c in cls if isinstance(c, str)):
            href = a.get("href")
            if href and isinstance(href, str):
                return urljoin(current_url, href)
        if id_attr and isinstance(id_attr, str) and next_patterns.search(id_attr):
            href = a.get("href")
            if href and isinstance(href, str):
                return urljoin(current_url, href)
    
    return None

def scroll_and_load(page, max_scrolls=10, scroll_delay=1.5):
    """Scroll to the bottom of a page to trigger infinite scroll loading."""
    last_height = page.evaluate("document.body.scrollHeight")
    
    for scroll in range(max_scrolls):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(scroll_delay)
        
        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == last_height:
            logger.info(f"No new content after {scroll + 1} scrolls")
            break
        last_height = new_height
        logger.info(f"Scrolled {scroll + 1}/{max_scrolls}, new height: {new_height}")
    
    return page.content()
