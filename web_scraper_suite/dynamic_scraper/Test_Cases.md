# Dynamic Scraper — Manual Test Cases

## Prerequisites
- Run all commands from the `dynamic_scraper/` directory
- Playwright Chromium must be installed (`playwright install chromium`)
- Delete `output.json` / `output.csv` between tests
- Internet connection required for live URL tests

## Shared CLI Tests
See `../static_scraper/TEST_CASES.md` for shared feature tests:
- `--urls`, `--tags`, `--max-pages`, `--output`, `--no-csv`
- `--deduplicate`, `--verbose`
- Interactive mode, invalid URL, invalid tags, loop detection
- Missing tags, max-pages = 0 / -1

Those tests apply identically to this scraper. Below are tests for dynamic-specific features.

---

## Test 1: Headless Mode (Default)
**Command:**
```bash
python main.py --urls https://quotes.toscrape.com/js/ --tags div
```
**Expected:** Browser runs invisibly in the background, page is scraped
**Pass Criteria:** No visible browser window appears; `output.json` contains extracted quotes

---

## Test 2: Headed Mode
**Command:**
```bash
python main.py --urls https://quotes.toscrape.com/js/ --tags div --no-headless
```
**Expected:** A visible Chromium window opens, navigates to the page, then closes
**Pass Criteria:** Chrome window is visible during scraping; same output as Test 1

---

## Test 3: JS-Rendered Content
**Command:**
```bash
python main.py --urls https://quotes.toscrape.com/js/ --tags div
```
**Expected:** JavaScript-rendered quotes are extracted (would be empty with `requests` alone)
**Pass Criteria:** `output.json` has 10+ quotes (the page loads quotes dynamically via JS)

---

## Test 4: Wait for Selector
**Command:**
```bash
python main.py --urls https://quotes.toscrape.com/js/ --tags span --wait-for .text
```
**Expected:** Waits for elements matching `.text` to appear before extracting
**Pass Criteria:** Log shows "Waiting for selector: .text"; data is extracted after the wait

---

## Test 5: Custom Timeout
**Command:**
```bash
python main.py --urls https://quotes.toscrape.com --tags h1 --timeout 5000
```
**Expected:** Page loads within 5 seconds (this site is fast enough)
**Pass Criteria:** Scraping completes successfully within the timeout window

---

## Test 6: Timeout Exceeded
**Command:**
```bash
python main.py --urls https://quotes.toscrape.com --tags h1 --timeout 1
```
**Expected:** 1ms timeout is impossibly short, navigation fails
**Pass Criteria:** Log shows timeout error; "No data was extracted." message appears

---

## Test 7: Infinite Scroll
**Command:**
```bash
python main.py --urls https://quotes.toscrape.com/js/ --tags div --scroll --max-scrolls 5
```
**Expected:** Page loads with `domcontentloaded`, then scrolls up to 5 times
**Pass Criteria:** Log shows "Infinite scroll enabled, scrolling up to 5 times..." and scroll progress messages; content is extracted

---

## Test 8: Max Scrolls Limit
**Command:**
```bash
python main.py --urls https://quotes.toscrape.com/js/ --tags div --scroll --max-scrolls 2
```
**Expected:** Only scrolls 2 times before stopping (even if more content could load)
**Pass Criteria:** Log shows at most 2 scroll attempts; scraper completes

---

## Test 9: Pagination on Static Site
**Command:**
```bash
python main.py --urls https://quotes.toscrape.com --tags div --max-pages 3
```
**Expected:** Follows "Next" links across 3 pages using the browser
**Pass Criteria:** Log shows "Next page found. Moving to Page 2..." and "Page 3"; >20 quotes extracted

---

## Test 10: Retries on Failure
**Command:**
```bash
python main.py --urls https://this-domain-does-not-exist-12345.com --tags h1 --verbose
```
**Expected:** 3 retry attempts with exponential backoff (2s, 4s delays between)
**Pass Criteria:** Log shows "attempt 1/3", "attempt 2/3", "attempt 3/3"; "No data was extracted."

---

## Test 11: Robots.txt Timeout
**Command:**
```bash
python main.py --urls https://192.0.2.1 --tags h1
```
**Expected:** robots.txt fetch uses 10s socket timeout instead of default ~80s
**Pass Criteria:** Log shows "Could not read robots.txt" within ~10 seconds; scraper proceeds or fails fast on navigation

---

## Test 12: Combinatorial — All Dynamic Flags
**Command:**
```bash
python main.py --urls https://quotes.toscrape.com/js/ --tags div --scroll --max-scrolls 3 --no-headless --wait-for .quote --timeout 60000 --verbose
```
**Expected:** Full pipeline with visible browser, scroll, selector wait, long timeout, debug logging
**Pass Criteria:** All flags respected; visible browser scrolls 3 times; debug logs shown; data saved

---

## Test Case Summary

| # | Test | Key Flag(s) | Expected Outcome |
|---|------|-------------|------------------|
| 1 | Headless (default) | _(none)_ | No visible browser |
| 2 | Headed mode | `--no-headless` | Visible browser window |
| 3 | JS rendering | `--urls` on JS site | Extracted JS content |
| 4 | Wait for selector | `--wait-for` | Waits before extracting |
| 5 | Custom timeout | `--timeout 5000` | Loads within 5s |
| 6 | Timeout exceeded | `--timeout 1` | Fails fast with timeout |
| 7 | Infinite scroll | `--scroll` | Scrolls and extracts |
| 8 | Max scrolls limit | `--scroll --max-scrolls 2` | Only 2 scrolls |
| 9 | Pagination | `--max-pages 3` | 3 pages scraped |
| 10 | Retries | invalid URL | 3 retry attempts |
| 11 | robots.txt timeout | unreachable IP | Fails fast (~10s) |
| 12 | All flags | _(all)_ | Full pipeline works |
