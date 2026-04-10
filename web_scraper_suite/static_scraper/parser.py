from bs4 import BeautifulSoup

# Get all unique tags
def get_all_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    tags = set()
    ignore_tags = ["style", "script"]

    for tag in soup.find_all():
      if tag.name not in ignore_tags:
        tags.add(tag.name)

    return sorted(tags)


#Extract selected tags
def extract_tags(html, selected_tags):
    soup = BeautifulSoup(html, "html.parser")
    results = {}

    for tag in selected_tags:
        elements = soup.find_all(tag)

        extracted = []
        for el in elements:
            text = el.get_text(separator="",strip=True)

            if text:  # avoid emptry entries
                extracted.append(text)

        results[tag] = extracted

    return results
