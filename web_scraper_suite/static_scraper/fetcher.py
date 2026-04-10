from urllib.robotparser import RobotFileParser
import requests
from fake_useragent import UserAgent
import random
import time

def fetch_page(url, user_agent="MyScraper",referer=None):
    # Check robots.txt
    rp = RobotFileParser()
    rp.set_url(url.rstrip("/") + "/robots.txt")
    rp.read()
    if not rp.can_fetch(user_agent, url):
        print("URL disallowed by robots.txt:", url)
        return None

    # Random User-Agent
    try:
        ua = UserAgent().random
    except:
        ua = "Mozilla/5.0"

    headers = {
        "User-Agent": ua,
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    }

    # Add the Referer logic
    if referer:
        headers["Referer"] = referer

    # Polite delay
    time.sleep(random.uniform(1,3))

    # Fetch page
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch page. Status code: {response.status_code}")
            return None
    except Exception as e:
        print("Error fetching page:", e)
        return None
