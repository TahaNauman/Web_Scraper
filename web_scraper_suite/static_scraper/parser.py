from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

# Get all unique tags
def get_all_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    tags = set()
    ignore_tags = ["style", "script", "head", "meta", "link", "noscript"]

    for tag in soup.find_all():
      if tag.name not in ignore_tags:
        tags.add(tag.name)

    return sorted(tags)


# Extract selected tags
def extract_tags(html, selected_tags, base_url):
    soup = BeautifulSoup(html, "html.parser")
    results = {}

    for tag in selected_tags:
        elements = soup.find_all(tag)
        extracted = []
        
        for el in elements:
            # Get standard text
            text = el.get_text(separator=" ", strip=True)
            
            # Handle Attributes (Links and Images)
            attr_url = None
            if tag == 'a':
                attr_url = el.get('href')
            elif tag == 'img':
                attr_url = el.get('src')
                # If an image has no text, use the 'alt' description as a label
                if not text:
                    text = el.get('alt', 'No description')

            # Resolve Relative Paths
            if attr_url:
                full_url = urljoin(base_url, attr_url)
                extracted.append({"label": text, "url": full_url})
            elif text:
                # If it's just a normal tag (like <p>), just save the text
                extracted.append(text)

        results[tag] = extracted

    return results

def find_next_page(html, current_url):
    soup = BeautifulSoup(html, "html.parser")
    
    # Common patterns for 'Next' buttons
    next_patterns = re.compile(r'next|older|forward|>', re.I)
    
    # Search for an <a> tag that contains our patterns in text OR class/ID
    next_button = soup.find("a", string=next_patterns) or \
                  soup.find("a", attrs={"class": next_patterns}) or \
                  soup.find("a", attrs={"id": next_patterns})

    if next_button and next_button.get("href"):
        next_url = next_button["href"]
        # Join relative links (e.g. /page/2) with the current URL
        return urljoin(current_url, next_url)
    
    return None
