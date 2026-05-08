# Static Scraper — Manual Test Cases

## Prerequisites
- Run all commands from the `static_scraper/` directory
- Delete `output.json` / `output.csv` between tests to avoid confusion
- Internet connection required for live URL tests

---

## Test 1: Interactive Mode (No CLI Arguments)
**Command:**
```bash
python main.py
```
**Steps:**
1. When prompted `Enter starting URLs separated by commas:` → type `https://example.com`
2. When prompted `Enter max pages to scrape per URL (default 1):` → press Enter (accepts default 1)
3. When prompted `Select tags to extract (e.g., h1, p, img, a):` → type `h1, p`
**Expected:** Scrapes 1 page, saves `output.json` + `output.csv`, logs "Scraping Task Complete!"
**Pass Criteria:** `output.json` exists with `h1` and `p` keys; terminal shows progress logs

---

## Test 2: Single URL with Tags
**Command:**
```bash
python main.py --urls https://example.com --tags h1 p
```
**Expected:** Extracts `<h1>` and `<p>` text from one page
**Pass Criteria:** `output.json` contains `"h1"` with "Example Domain" and `"p"` with paragraph text

---

## Test 3: Multiple URLs
**Command:**
```bash
python main.py --urls https://example.com https://example.org --tags h1 p
```
**Expected:** Scrapes both sites sequentially, merges all results into one file
**Pass Criteria:** `output.json` contains data from both sites; log shows both URLs being processed

---

## Test 4: Invalid URL
**Command:**
```bash
python main.py --urls https://this-domain-does-not-exist-12345.com --tags h1
```
**Expected:** Fetch fails gracefully, logs "Failed to fetch" warning
**Pass Criteria:** Script does NOT crash; `output.json` is NOT created; log shows warning

---

## Test 5: Invalid / Non-Existent Tags
**Command:**
```bash
python main.py --urls https://example.com --tags nonexistenttag foobar
```
**Expected:** Script runs, extracts nothing for those tags (empty arrays in JSON)
**Pass Criteria:** `output.json` contains `"nonexistenttag": []` and `"foobar": []`; no crash

---

## Test 6: Max Pages = 0 (Edge Case)
**Command:**
```bash
python main.py --urls https://example.com --tags h1 --max-pages 0
```
**Expected:** No pages are scraped since `pages_count (0) < 0` is False
**Pass Criteria:** Log shows "No data was extracted"; no `output.json` created

---

## Test 7: Max Pages = Negative (Edge Case)
**Command:**
```bash
python main.py --urls https://example.com --tags h1 --max-pages -1
```
**Expected:** Same as max-pages 0 — the while loop never executes
**Pass Criteria:** Log shows "No data was extracted"; no `output.json` created

---

## Test 8: Max Pages = 2 (Pagination)
**Command:**
```bash
python main.py --urls https://quotes.toscrape.com --tags div --max-pages 2
```
**Expected:** Scrapes page 1, finds "Next" link, scrapes page 2, stops
**Pass Criteria:** Log shows "Scraping Page 1", "Next page found", "Scraping Page 2"; JSON has data from both pages; 3+ quotes extracted

---

## Test 9: Max Pages = 5 but only 2 pages exist
**Command:**
```bash
python main.py --urls https://quotes.toscrape.com --tags div --max-pages 5
```
**Expected:** Scrapes all available pages (probably 10), stops when no more "Next" links
**Pass Criteria:** Log shows "Scraping Task Complete!" without errors; reaches last page naturally

---

## Test 10: Custom Output Filename
**Command:**
```bash
python main.py --urls https://example.com --tags h1 --output my_scrape.json
```
**Expected:** Output saved as `my_scrape.json` + `my_scrape.csv`
**Pass Criteria:** Both `my_scrape.json` and `my_scrape.csv` exist with correct content

---

## Test 11: No CSV Output
**Command:**
```bash
python main.py --urls https://example.com --tags h1 --no-csv
```
**Expected:** Only JSON file is created; no CSV file
**Pass Criteria:** `output.json` exists; `output.csv` does NOT exist

---

## Test 12: Deduplication Enabled
**Command:**
```bash
python main.py --urls https://example.com --tags h1 --deduplicate
```
**Expected:** Duplicate entries are removed before saving (for a simple page like example.com, likely no duplicates, but logic runs)
**Pass Criteria:** Log shows "Deduplication applied to extracted data"; JSON has unique entries

---

## Test 13: Deduplication Disabled (Default)
**Command:**
```bash
python main.py --urls https://example.com --tags h1
```
**Expected:** No deduplication applied; raw extraction is saved
**Pass Criteria:** Log does NOT mention deduplication

---

## Test 14: Verbose Logging
**Command:**
```bash
python main.py --urls https://example.com --tags h1 --verbose
```
**Expected:** More detailed log output (DEBUG level from all modules)
**Pass Criteria:** Log shows additional debug messages beyond INFO level (e.g., from fetcher, parser)

---

## Test 15: Tags with Attributes (a and img)
**Command:**
```bash
python main.py --urls https://example.com --tags a img
```
**Expected:** Extracts links (`label` + `url` dicts) and images (`label` from alt + `url` from src)
**Pass Criteria:** JSON entries for `a` and `img` have `label` and `url` keys, not plain text

---

## Test 16: Combinatorial — All Arguments Together
**Command:**
```bash
python main.py --urls https://example.com https://example.org --tags h1 p a img --max-pages 2 --output combined.json --deduplicate --verbose
```
**Expected:** Runs full pipeline with pagination, dedup, detailed logging, custom output name, and no CSV
**Pass Criteria:** `combined.json` exists with all tags from both URLs; log is verbose; no CSV file created

---

## Test 17: Repeat URL (Loop Detection)
**Command:**
```bash
python main.py --urls https://quotes.toscrape.com --tags div --max-pages 10
```
**Expected:** If a page links to itself, the `visited_urls` set prevents infinite loops
**Pass Criteria:** Log does NOT show repeating the same URL endlessly; if loop is detected, log shows "Already visited ... stopping to avoid loop"

---

## Test 18: Tags Not Found on Page
**Command:**
```bash
python main.py --urls https://example.com --tags table form
```
**Expected:** These tags don't exist on the example.com page
**Pass Criteria:** `output.json` contains `"table": []` and `"form": []`; no crash

---

## Test 19: URL Allowed by robots.txt (Control)
**Command:**
```bash
python main.py --urls https://example.com --tags h1
```
**Expected:** robots.txt is fetched from the domain root, `can_fetch()` returns True, page is scraped normally
**Pass Criteria:** Log shows no robots.txt warning; `output.json` created with extracted data; scraper proceeds uninterrupted

---

## Test 20: URL Disallowed by robots.txt
**Command:**
```bash
python main.py --urls https://www.youtube.com/results?search_query=test --tags h1
```
**Expected:** YouTube's robots.txt disallows `/results`. The scraper detects this, logs a warning, and skips the URL
**Pass Criteria:** Log contains "disallowed by robots.txt" message for the URL; script does NOT crash; `output.json` is NOT created (since only 1 URL was provided and it was blocked)

---

## Test 21: Mixed — One Allowed URL + One Disallowed URL
**Command:**
```bash
python main.py --urls https://example.com https://www.youtube.com/results?search_query=test --tags h1
```
**Expected:** The allowed URL is scraped normally; the disallowed URL is skipped with a robots.txt warning
**Pass Criteria:** Log shows data extracted from example.com AND a "disallowed by robots.txt" warning for the YouTube URL; `output.json` contains only data from example.com

---

